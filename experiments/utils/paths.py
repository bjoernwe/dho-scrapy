from pathlib import Path


data_path = Path(__file__).parent.parent.parent.joinpath("data")
jsonl_path = data_path.joinpath("messages.jsonl")
model_path = data_path.joinpath("models")
