from pathlib import Path

from message_db.message_db import MessageDB


def convert_messages_to_text(path_in_jsonl: Path, path_out_txt: Path):
    """
    Reads JSON-line messages and stores their message bodies in plain text (one message per line).
    """

    msgs = MessageDB.from_file(jsonl_path=path_in_jsonl).get_all_message_bodies()

    with open(str(path_out_txt), 'w') as f:
        f.writelines('\n'.join(msgs))

    print(f'Wrote {len(msgs)} messages to {path_out_txt}')


if __name__ == '__main__':

    data_path = Path(__file__).parent.parent.joinpath('data')
    path_in_jsonl = data_path.joinpath('messages.jsonl')
    path_out_txt = data_path.joinpath('messages.txt')

    convert_messages_to_text(path_in_jsonl=path_in_jsonl, path_out_txt=path_out_txt)
