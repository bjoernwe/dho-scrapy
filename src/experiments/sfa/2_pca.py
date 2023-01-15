import numpy as np

from pathlib import Path

import matplotlib.pyplot as plt

from sklearn.decomposition import PCA


def main():

    embedding_path = Path(__file__).parent.joinpath('1_embeddings.npy')
    embeddings = np.load(str(embedding_path))

    pca = PCA()
    pca.fit(embeddings)

    plt.plot(pca.explained_variance_ratio_ * 100)
    plt.show()


if __name__ == '__main__':
    main()
