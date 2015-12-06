#!/usr/bin/env python
import argparse
import json

import yaml

from ..sde_to_wkt import SDEtoWKT
from ..wkt_to_socrata import WKTtoSocrata

parser = argparse.ArgumentParser(description='Push dataset')
parser.add_argument('-d', '--dataset', nargs=2, action='append', help='table and dataset id')
args = parser.parse_args()
datasets = {}

# If dataset args provided, use those
if args.dataset and len(args.dataset):
	for dataset in args.dataset:
		datasets[dataset[0]] = dataset[1]

# Otherwise, fetch datasets config
else:
	with open('config/datasets.yaml') as datasets_yaml:
		datasets = yaml.load(datasets_yaml)

print(datasets)

# Load config file
with open('config/config.json') as config_json:
	config = json.load(config_json)

spatial_reference = arcpy.SpatialReference(config['spatialReference'])

extractor = SDEtoWKT(config['workspace'], spatial_reference=spatial_reference)
pusher = WKTtoSocrata('config/config.json', config['controlTemplatePath'],
					config['datasyncPath'], temp_path=config['tempPath'])
	
# For each table in datasets config
for table in datasets:
	table_contents = extractor.get_table(table)
		
	print('Pushing %s to %s/d/%s' % (table, config['domain'], datasets[table]))
	
	pusher.push(table_contents.fields, table_contents.rows, datasets[table], 
				table_name=table)