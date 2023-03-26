import sys
sys.path.append('../../../')

import json
import openai
from data_models.categories import DhOCategory
from data_models.message_db import MessageDB
from experiments.utils.paths import jsonl_path

attributes = {
    'concentration': "Level of concentration",
    'pleasure': "Level of pleasure",
    'pain': "Level of pain or discomfort",
    'peak_experience': "Presence of peak experiences, like euphoria",
    'visual_phenomena': "Presence of visual phenomena, like colors and light",
    'auditory_phenomena': "Presence of auditory phenomena, like sounds, voices, humming, or ringing",
    'tactile_phenomena': "Presence of tactile phenomena, like tingling or warmth",
    'energetic_phenomena': "Presence of energetic phenomena, like vibrations, pulsations, or energy movement",
    'gratitude': "Level of gratitude, like a sense of appreciation or thankfulness",
    'compassion': "Level of compassion, like a sense of love or kindness",
    'bitterness': "Level of bitterness, like a sense of anger or resentment",
    'fear': "Level of fear, like a sense of anxiety or worry",
    'equanimity': "Level of equanimity",
    'insight': "Level of insight, like a sense of understanding or clarity",
}

AUTHOR_ID = "curious-frame"
def main():
    message_db = MessageDB.from_file(jsonl_path=jsonl_path)
    data = analyze_messages(message_db=message_db)
    json_object = json.dumps(data, indent=4)
    with open("data.json", "w") as outfile:
        outfile.write(json_object)


def analyze_messages(message_db: MessageDB, author_id=AUTHOR_ID):
    practice_logs = (
        message_db.filter_categories(categories={DhOCategory.PracticeLogs})
        .filter_threads(authors={author_id})
        .filter_thread_responses(keep_op=True)
        .sorted_by_date()
        .get_all_messages()
    )

    print(f'Found {len(practice_logs)} practice logs from user "{author_id}":\n')
    all_data = []
    for idx in range(len(practice_logs)):
        if idx % 20 == 0:
            print(f'Analyzed {len(all_data)} / {idx} practice logs')
        log = practice_logs[idx]
        if len(log.msg) < 50:
            continue
        data = analyze_practice_log(log.msg)
        if data is None:
            continue
        data['msg'] = log.msg
        data['msg_id'] = log.msg_id
        data['date'] = log.date.isoformat()
        all_data.append(data)
    return all_data

def analyze_practice_log(log):
    system_msg = "You are a skilled meditation instructor helping to coach a student."
    prompt = "Here is the student's practice log for today:\n\n%s" % (log)
    question = """
Please rate the student on the following attributes. The name of the attribute is followed
by a colon, and then a description of that attribute.

%s

For each attribute, rate on a scale of 1-5, with 1 being low and 5 being high. Only use whole numbers.

Please respond with the name of each attribute on a new line, followed by a colon, then the number.
Include no other text in your response.

If this does not look like a meditation practice log, respond only with the text "N/A".
    """ % "\n".join(["* %s: %s" % (key, attributes[key]) for key in attributes])

    resp = openai.ChatCompletion.create(
      model="gpt-3.5-turbo",
      messages=[
            {"role": "system", "content": system_msg},
            {"role": "user", "content": prompt},
            {"role": "user", "content": question},
        ]
    )
    answer = resp['choices'][0]['message']['content']
    data = {}
    if "N/A" in answer:
        return None
    lines = answer.splitlines()
    for line in lines:
        parts = line.split(':')
        if len(parts) != 2:
            print("bad response", answer)
            return None

        attribute = parts[0].strip()
        value = parts[1].strip().removesuffix('.')
        if attribute not in attributes:
            print("bad attribute", attribute, answer)
            return None
        try:
            data[attribute] = int(value)
        except ValueError:
            print("bad value", value, answer)
            return None
    return data

if __name__ == "__main__":
    main()
