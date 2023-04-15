from pathlib import Path


project_path = Path(__file__).parent.parent
data_path = project_path.joinpath("data")
default_cache_path = data_path.joinpath("cache")
default_jsonl_path = data_path.joinpath("messages.jsonl")


def get_default_cache_path(sentences_per_snippet: int, model_name: str) -> Path:
    return default_cache_path.joinpath(
        f"emb_snt_{sentences_per_snippet}_{model_name}.shelf"
    )
