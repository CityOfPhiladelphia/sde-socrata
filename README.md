# SDE to Socrata
Create and push Socrata datasets from Arc SDE feature classes

This program provides a command-line utility to create Socrata datasets
from Arc SDE feature classes and push their contents in using an efficient
transfer process provided by Socrata's DataSync utility. Optionally, you 
can use a [list of pushes](config/datasets.yaml) to create a recurring
sync job that can run on a cron tab / Windows task.

Supports proxy servers, logging, and email alerts (via DataSync's out-of-the-box 
functionality).

## Requirements
- Java Runtime JDK
- [DataSync](https://socrata.github.io/datasync/)
- ArcGIS Desktop with Python and ArcPy

## Installation
1. Clone this repository
2. Put the DataSync `.jar` file inside the directory
3. Optionally, create a virtual environment using `virtualenv --system-site-packages venv`
and activate using `. venv/bin/activate` (unix) or `venv/Scripts/activate` (windows)
4. Install dependencies via `pip install -I -r requirements.txt`
5. Install the command-line utility via `python setup.py install`

## Configuration
1. Register a [Socrata app token](http://dev.socrata.com/register)
2. Copy `config/config.sample.json` to `config/config.json` and fill it in ([help](http://socrata.github.io/datasync/resources/preferences-config.html))
3. Optionally, fill in table and dataset ID information in `config/datasets.yaml`

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