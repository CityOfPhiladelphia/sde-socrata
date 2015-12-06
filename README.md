# SDE to Socrata
Create and push Socrata datasets from Arc SDE feature classes

This program loops through a [list of tables](config/datasets.yaml)
and pushes their contents to their corresponding Socrata dataset IDs
using an efficient transfer process provided by Socrata's DataSync utility.

Supports proxy servers, logging, and email alerts.

## Requirements
- Java Runtime JDK
- [DataSync](https://socrata.github.io/datasync/)
- ArcGIS Desktop with Python and ArcPy

## Installation
1. Clone this repository
2. Optionally, activate using `virtualenv --system-site-packages venv`
3. Install dependencies via `pip install -r -I requirements.txt`
4. Put the DataSync `.jar` file in the `/bin` directory
5. Install via `python setup.py install`

## Configuration
1. Register a [Socrata app token](http://dev.socrata.com/register)
2. Copy `config/config.sample.json` to `config/config.json` and fill it in ([help](http://socrata.github.io/datasync/resources/preferences-config.html))
3. Fill in table and dataset ID information in `config/datasets.yaml`

## Usage
```bash
Usage:
  sdesocrata create <table> [--public] [--config=<config_path>]
  sdesocrata push <table> <id>
  sdesocrata push --list=<list_path>
  sdesocrata -h | --help
  sdesocrata --version

Options:
  --public                          Set dataset permissions to public
  --config=<config_path>            Path to config file [default: ./config/config.json]
  -h --help                         Show this screen.
  --version                         Show version.

Examples:
  sdesocrata create Council_Districts_2016
  sdesocrata push Council_Districts_2016 jo21-8sz0
  sdesocrata push --list=config/datasets.yaml
```

Command-line setup followed [this helpful tutorial](https://stormpath.com/blog/building-simple-cli-interfaces-in-python/).