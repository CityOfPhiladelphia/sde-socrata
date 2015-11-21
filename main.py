import arcpy
import yaml
import json
import subprocess
import unicodecsv as csv
from slugify import slugify

arcpy.env.workspace = 'C:/Users/tim/Desktop/ArcGIS/GIS_SDE_VIEWER.gdb'

def get_fields(table):
	select = []
	headers = []
	desc = arcpy.Describe(table)
	fields = desc.fields
	for field in fields:
		if field.Type == 'Geometry':
			select.append(field.Name + '@WKT')
			headers.append('the_geom')
		else:
			select.append(field.Name)
			headers.append(slugify(field.Name, separator='_'))
					
	return select, headers

# Load control file template
with open('control.template.json') as control_json:
	control_template = json.load(control_json)

# Fetch datasets config
with open('datasets.yaml') as datasets_yaml:
	datasets = yaml.load(datasets_yaml)
	
# For each dataset in datasets config
for dataset in datasets:
	control_file = control_template.copy()
	
	select, headers = get_fields(dataset['table'])

	with open('tmp/' + dataset['table'] + '.csv', 'wb') as f:
		writer = csv.writer(f)
		writer.writerow(headers)
		writer.writerows(arcpy.da.SearchCursor(dataset['table'], select))
		
		# Put clean headers into control file template
		control_file['csv']['columns'] = headers
	
		# Write control file to disk
		with open('tmp/control.' + dataset['table'] + '.json', 'w') as f:
			json.dump(control_file, f)
		
	print('Pushing %s to %s' % (dataset['table'], dataset['socrata_id']))
	
	# Call DataSync w/csv and control file
	subprocess.call([
		'java',
		'-jar', './bin/DataSync-1.6.jar',
		'-c', 'config.json',
		'-f', 'tmp/' + dataset['table'] + '.csv',
		'-i', dataset['socrata_id'],
		'-m', 'replace',
		'-ph', 'true',
		'-cf', 'tmp/control.' + dataset['table'] + '.json'
	])