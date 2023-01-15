from pathlib import Path

from message_db.message_db import MessageDB


if __name__ == '__main__':

    data_path = Path(__file__).parent.parent.joinpath('data')
    jsonl_path = data_path.joinpath('messages.jsonl')
    output_path = data_path.joinpath('messages.txt')

    msgs = MessageDB.from_file(jsonl_path=jsonl_path).get_all_message_bodies()

    with open(str(output_path), 'w') as f:
        f.writelines('\n'.join(msgs))

    print(f'Wrote {len(msgs)} messages to {output_path}')
