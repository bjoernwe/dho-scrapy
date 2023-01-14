from pathlib import Path

from message_db.message_db import MessageDB


if __name__ == '__main__':

    data_path = Path(__file__).parent.parent.joinpath('data')
    jsonl_path = data_path.joinpath('messages.jsonl')
    output_path = data_path.joinpath('messages.txt')

    msgs = MessageDB.from_file(jsonl_path=jsonl_path).get_all_messages()
    msg_bodies = [msg.msg for msg in msgs]

    with open(str(output_path), 'w') as f:
        f.writelines('\n'.join(msg_bodies))

    print(f'Wrote {len(msg_bodies)} messages to {output_path}')
