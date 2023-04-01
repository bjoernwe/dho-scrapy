# DhO Scrapy

A [Scrapy](https://scrapy.org/) spider to crawl messages from
[Dharma Overground](https://www.dharmaoverground.org/).

### Setup Runtime Environment

- `pip install poetry` to install `poetry`
- `poetry install` to prepare environment incl. all dependencies
  - Or alternatively: `poetry install --without experiments` to skip large dependencies like `torch` and `cudas` that are only needed for the experiments
- `poetry shell` to activate virtual environment
- `python -m pytest` to run tests

### Quickstart

- `poetry shell` to activate virtual environment
- `python -m scraper.1_crawl_messages` to crawl messages from DhO (to be stored in `./data/`)
- `python -m scraper.2_convert_to_plain_text` to convert messages to simple txt (in `./data/`)

### Examples & Experiments

See `examples` and `experiments` for how to use the crawled messages

### Development

- `./install-pre-commit.sh` to automatically run tests before every commit
