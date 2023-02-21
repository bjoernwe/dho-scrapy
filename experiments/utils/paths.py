from pathlib import Path


data_path = Path(__file__).parent.parent.parent.joinpath("data")
jsonl_path = data_path.joinpath("messages.jsonl")
embeddings_path = data_path.joinpath("embeddings")
