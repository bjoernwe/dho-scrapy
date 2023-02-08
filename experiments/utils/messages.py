from experiments.utils.paths import jsonl_path
from message_db.message_db import MessageDB

message_db = MessageDB.from_file(jsonl_path=jsonl_path)
