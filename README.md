# DhO Scrapy

A [Scrapy](https://scrapy.org/) spider to crawl messages from 
[Dharma Overground](https://www.dharmaoverground.org/).

### Setup Runtime Environment

- `pip install poetry` to install `poetry`
- `poetry install` to prepare environment incl. all dependencies
- `poetry shell` to activate virtual environment
- `cd src`
- `python -m pytest` to run tests

### Quickstart

- `cd src`
- `poetry shell` to activate virtual environment
- `python 1_crawl_messages.py` to crawl messages from DhO (to be stored in `./data/`)
- `python 2_convert_to_plain_text.py` to convert messages to simple txt (in `./data/`)
- `python 2_calc_embeddings.py` to calculate vector embeddings for all messages (slow!)


### Development

- `./install_git_hooks.sh` to automatically run the tests before every commit
