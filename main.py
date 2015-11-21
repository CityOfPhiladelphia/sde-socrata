import json
import subprocess

import yaml
import unicodecsv as csv

from sde_to_wkt import SDEtoWKT

# Load config file
with open('config/config.json') as config_json:
	config = json.load(config_json)

spatial_reference = arcpy.SpatialReference(config['spatialReference'])

extractor = SDEtoWKT(config['workspace'], spatial_reference=spatial_reference,
					rename_geometry='the_geom') # socrata name for geom fields

# Load control file template
with open('config/control.template.json') as control_json:
	control_template = json.load(control_json)

# Fetch datasets config
with open('config/datasets.yaml') as datasets_yaml:
	datasets = yaml.load(datasets_yaml)
	
# For each table in datasets config
for table in datasets:
	table_contents = extractor.get_table(table)

	# Write dataset to CSV in WKT format
	with open('tmp/' + table + '.csv', 'wb') as f:
		writer = csv.writer(f)
		writer.writerow(table_contents.fields)
		writer.writerows(table_contents.rows)
		
	# Put clean headers into control file template
	control_file = control_template.copy()
	control_file['csv']['columns'] = table_contents.fields

	# Write control file to disk
	with open('tmp/' + table + '.control.json', 'w') as f:
		json.dump(control_file, f, indent=4)
		
	print('Pushing %s to %s/d/%s' % (table, config['domain'], datasets[table]))
	
	# Call DataSync w/csv and control file
	subprocess.call([
		'java',
		'-jar', config['datasyncPath'],
		'-c', 'config/config.json',
		'-f', 'tmp/' + table + '.csv',
		'-i', datasets[table],
		'-m', 'replace',
		'-ph', 'true',
		'-cf', 'tmp/' + table + '.control.json'
	])