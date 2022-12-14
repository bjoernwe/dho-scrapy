from pathlib import Path

from utils.utils import read_dho_messages, save_strings


def convert_to_message_bodies(in_path: Path, out_path: Path):
    messages = [msg.msg for msg in read_dho_messages(jsonl_path=in_path)]
    save_strings(strings=messages, output_file=str(out_path))


if __name__ == '__main__':

    data_path = Path(__file__).parent.parent.joinpath('data')

    jsonl_path = data_path.joinpath('messages.jsonl')
    messages_path = data_path.joinpath('messages.txt')

    convert_to_message_bodies(
        in_path=jsonl_path,
        out_path=messages_path,
    )
