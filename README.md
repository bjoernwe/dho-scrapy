# DhO Scrapy

A [Scrapy](https://scrapy.org/) spider to crawl messages from
[Dharma Overground](https://www.dharmaoverground.org/).

## Quick Start

### Setup Runtime Environment

- `pip install poetry` to install `poetry`
- `poetry install` to prepare environment incl. all dependencies
  - Or alternatively: `poetry install --without experiments` to skip large dependencies like `torch` and `cudas` that are only needed for the experiments
- `poetry shell` to activate virtual environment

### Scrape Data

- `poetry shell` to activate virtual environment
- `python -m scraper.1_crawl_messages` to crawl messages from DhO (to be stored in `./data/`)
- `python -m scraper.2_convert_to_plain_text` to convert messages to simple txt (in `./data/`)

### Examples & Experiments

See `examples` and `experiments` for how to use the crawled messages. For instance

- `poetry shell`
- `python -m examples.example_message_filtering`
- `python -m experiments.bjoern.experiment_count_practice_logs`

## Project Structure

### Crawling

Crawling and initial data processing (like redaction of usernames) is implemented in the [Scrapy](https://scrapy.org/)
framework. Everything Scrapy-related can be found in package `scraper`.

### Data

Per default, crawled data can be found in the `data` directory. You can either access it directly or use the tools from
`data_tools`. In particular, `MessageDB` is a convenient way to access the raw data through a convenient interface that
allows for querying and filtering (see `examples` package).

Another important tool is the `TransformerEmbedder` in `data_tools.embedders`. It's a convenient way of doing text
embeddings, which is used in many experiments. Since it can be very slow to calculate embeddings for tens or even
hundreds of thousands of messages, the embedder can cache results on disk (see `experiments` for examples).

Since both, setting up a `MessageDB` and setting up an `Embedder` with cache, is a common step for many experiments,
there's also the `ExperimentHelper` in `experiments.experiment_helpe` to make the setup more convenient.

### Experiments

`experiments` is the place where people are going to try out stuff.

## Development

- `poetry run python -m pytest`
- `./install-pre-commit.sh` to automatically run tests before every commit
