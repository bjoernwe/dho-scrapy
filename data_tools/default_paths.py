from pathlib import Path


project_path = Path(__file__).parent.parent
data_path = project_path.joinpath("data")
default_cache_path = data_path.joinpath("cache")
default_jsonl_path = data_path.joinpath("messages.jsonl")
