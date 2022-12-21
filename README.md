# DhO Scrapy

A [Scrapy](https://scrapy.org/) spider to crawl messages from 
[Dharma Overground](https://www.dharmaoverground.org/).

### Quickstart

- `poetry install` to prepare environment incl. all dependencies
- `poetry shell` to activate virtual environment
- `cd src`
- `python -m pytest` to run tests
- `python 1_crawl_messages.py` to crawl messages (to be stored in `./data/`)
- `python 2_convert_data.py` to extract messages to simple txt


### Development

- `./install_git_hooks.sh`
