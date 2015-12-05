import json
import subprocess

import unicodecsv as csv

class WKTtoSocrata(object):
	def __init__(self, config_file_path, control_template_path, 
					datasync_path, temp_path='tmp'):
		self.config_file_path = config_file_path
		self.datasync_path = datasync_path
		self.temp_path = temp_path.rstrip('/')  # trim trailing slash
		
		# Load control file template
		with open(control_template_path) as control_json:
			self.control_template = json.load(control_json)
	
	def push(self, fields, rows, dataset_id, table_name=None):
		if table_name is None:
			table_name = dataset_id  # default table_name
		
		# Write dataset to CSV
		with open('%s/%s.csv' % (self.temp_path, table_name), 'wb') as f:
			writer = csv.writer(f)
			writer.writerow(fields)
			writer.writerows(rows)
		
		# Put clean headers into control file template
		control_file = self.control_template.copy()
		control_file['csv']['columns'] = fields
		
		# Write control file to disk
		with open('%s/%s.control.json' % (self.temp_path, table_name), 'w') as f:
			json.dump(control_file, f, indent=4)
		
		# Call DataSync w/csv and control file
		return subprocess.call([
			'java',
			'-jar', self.datasync_path,
			'-c', self.config_file_path,
			'-f', '%s/%s.csv' % (self.temp_path, table_name),
			'-i', dataset_id,
			'-m', 'replace',
			'-ph', 'true',
			'-cf', '%s/%s.control.json' % (self.temp_path, table_name)
		])