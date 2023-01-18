import matplotlib.pyplot as plt
import numpy as np
import pickle

from pathlib import Path

from sklearn.decomposition import PCA

from dho_scraper.categories import DhOCategory
from message_db.message_db import MessageDB


def main():

    # Input files
    data_path = Path().resolve().parent.joinpath('data')
    jsonl_path = data_path.joinpath('messages.jsonl')

    # Load messages
    msgs = MessageDB.from_file(jsonl_path=jsonl_path) \
                    .filter_categories(categories={DhOCategory.PracticeLogs}) \
                    .filter_thread_responses(keep_op=True) \
                    .filter_message_length(min_num_words=30) \
                    .filter_threads(min_num_messages=5) \
                    .get_all_messages()

    # Load embeddings
    embeddings_path = data_path.joinpath('embeddings.pkl')
    with open(str(embeddings_path), 'rb') as f:
        all_embeddings = pickle.load(f)

    # Embeddings for messages
    msg_embeddings = np.vstack([all_embeddings[msg.msg_id] for msg in msgs])
    print(f'{msg_embeddings.shape[0]} embeddings, {msg_embeddings.shape[1]} dimensions')

    # Principal Component Analysis (PCA)
    pca = PCA()
    pca.fit(msg_embeddings)

    # Plot explained variance
    plt.plot(pca.explained_variance_ratio_ * 100)
    plt.xlabel('component')
    plt.ylabel('% of variance explained')
    plt.show()

    # Print most extreme sentences (according to PCA)
    for component in range(3):

        print(f'Component {component}\n')

        sorted_msgs = sorted(msgs, key=lambda m: pca.transform(all_embeddings[m.msg_id])[:,component])

        for msg in sorted_msgs[:3]:
            print(f'  {msg.msg}')

        print('\n  ...\n')

        for msg in sorted_msgs[-3:]:
            print(f'  {msg.msg}')

        print('\n')


if __name__ == '__main__':
    main()
