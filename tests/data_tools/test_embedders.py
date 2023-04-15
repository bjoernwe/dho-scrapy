from pathlib import Path

from data_tools.embedders.embedder_mock import EmbedderMock
from data_tools.textsnippet import TextSnippet


def test_hash_function_is_not_random():

    # GIVEN an Embedder object and a string
    embedder = EmbedderMock()
    text = "FOO"

    # WHEN the string's hash is calculated
    text_hash = embedder._calc_hash(text="")

    # THEN it is always the same (in contrast to Python's hash() which depends on a seed)
    assert text_hash == "d41d8cd98f00b204e9800998ecf8427e"


def test_embedding_is_stored_persistently(tmp_path: Path):

    # GIVEN an Embedder and a text snippet
    cache_path = tmp_path.joinpath("cache.shelf")
    embedder = EmbedderMock(cache_path=cache_path)
    snippet = TextSnippet(source_msg_id=123, text="foo bar")

    # WHEN the embedding is calculated
    assert embedder.calls_to_calc == 0
    embedder.get_embedding(text=snippet.text)
    assert embedder.calls_to_calc == 1

    # THEN it is permanently found in cache afterwards
    reloaded_embedder = EmbedderMock(cache_path=cache_path)
    reloaded_embedder.get_embedding(text=snippet.text)
    assert reloaded_embedder.calls_to_calc == 0


def test_embeddings_are_stored_persistently(tmp_path: Path):

    # GIVEN an Embedder and a text snippet
    cache_path = tmp_path.joinpath("cache.shelf")
    embedder = EmbedderMock(cache_path=cache_path)
    snippet = TextSnippet(source_msg_id=123, text="foo bar")

    # WHEN the embedding is calculated
    assert embedder.calls_to_calc == 0
    embedder.get_embeddings(texts=[snippet.text] * 3)
    assert embedder.calls_to_calc == 1

    # THEN it is permanently found in cache afterwards
    reloaded_embedder = EmbedderMock(cache_path=cache_path)
    reloaded_embedder.get_embeddings(texts=[snippet.text] * 3)
    assert reloaded_embedder.calls_to_calc == 0


def test_embeddings_have_correct_dimensionality(tmp_path: Path):

    # GIVEN an Embedder and a text snippet
    cache_path = tmp_path.joinpath("cache.shelf")
    embedder = EmbedderMock(cache_path=cache_path, dims=32)
    snippet = TextSnippet(source_msg_id=123, text="foo bar")

    # WHEN the embedding is calculated
    embedding = embedder.get_embeddings(texts=[snippet.text] * 3)

    # THEN it is permanently found in cache afterwards
    assert embedding.shape == (3, 32)
