import sys
sys.path.append('../../../')

import openai
from data_models.categories import DhOCategory
from data_models.message_db import MessageDB
from experiments.utils.paths import jsonl_path

attributes = {
    'concentration': "Level of concentration",
    'pleasure': "Level of pleasure",
    'pain': "Level of pain or discomfort",
    'peak_experience': "Presence of peak experiences",
}

AUTHOR_ID = "curious-frame"
def main():
    message_db = MessageDB.from_file(jsonl_path=jsonl_path)
    analyze_messages(message_db=message_db)


def analyze_messages(message_db: MessageDB, author_id=AUTHOR_ID):
    practice_logs = (
        message_db.filter_categories(categories={DhOCategory.PracticeLogs})
        .filter_threads(authors={author_id})
        .filter_thread_responses(keep_op=True)
        .sorted_by_date()
        .get_all_messages()
    )

    # Print first practice logs
    print(f'Found {len(practice_logs)} practice logs from user "{author_id}":\n')
    for log in practice_logs[0:3]:
        data = analyze_practice_log(log.msg)
        print(log.msg)
        print(data)


def analyze_practice_log(log):
    system_msg = "You are a skilled meditation instructor helping to coach a student."
    prompt = "Here is the student's practice log for today:\n\n%s" % (log)
    question = """
Please rate the student on the following attributes:

%s

For each attribute, rate on a scale of 1-5, with 1 being low and 5 being high. Only use whole numbers.

Please respond with each attribute on a new line, followed by a colon, then the number.
Include no other text in your response.
    """ % ("* " + "\n* ".join(attributes.values()))

    print(question)
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
    lines = answer.splitlines()
    for line in lines:
        parts = line.split(':')
        attribute = parts[0].strip()
        value = parts[1].strip()
        for key in attributes:
            if attributes[key] == attribute:
                data[key] = int(value)
    return data

if __name__ == "__main__":
    main()
