from pathlib import Path

from bertopic import BERTopic

from utils.utils import read_strings


def main():

    data_path = Path(__file__).parent.parent.joinpath('data')
    messages_path = data_path.joinpath('messages.txt')

    messages = read_strings(file=str(messages_path))

    topic_model = BERTopic(language="english", calculate_probabilities=True, verbose=True)
    topics, probs = topic_model.fit_transform(messages)

    print(topic_model.get_topic_info())


if __name__ == '__main__':
    main()
