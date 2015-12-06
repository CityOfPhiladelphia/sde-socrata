# SDE to Socrata Pusher
Push Arc SDE tables to Socrata via DataSync

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

## Configuration
1. Register a [Socrata app token](http://dev.socrata.com/register)
2. Copy `config/config.sample.json` to `config/config.json` and fill it in ([help](http://socrata.github.io/datasync/resources/preferences-config.html))
3. Fill in table and dataset ID information in `config/datasets.yaml`

## Usage
```bash
$ python main.py
```

Command-line setup followed [this helpful tutorial](https://stormpath.com/blog/building-simple-cli-interfaces-in-python/).