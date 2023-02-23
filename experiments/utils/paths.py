from pathlib import Path


project_path = Path(__file__).parent.parent.parent
data_path = project_path.joinpath("data")
jsonl_path = data_path.joinpath("messages.jsonl")
embeddings_path = data_path.joinpath("embeddings")
