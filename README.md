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

### Examples & Experiments

See `examples` and `experiments` for how to use the crawled messages.

### Development

- `./install-pre-commit.sh` to automatically run tests before every commit

#### Reddit Spider

If you want to run `RedditSpider`, copy `src/.env.template` to `src/.env` and fill out the missing values for
`SCRAPY_REDDIT_SECRET` and `SCRAPY_REDDIT_PASSWORD`.
