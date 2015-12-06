import json

import yaml

from .base import Base
from ..sde_to_wkt import SDEtoWKT
from ..wkt_to_socrata import WKTtoSocrata

class Push(Base):
	def run(self):
		datasets = {}
		
		# If dataset args provided, use those
		if self.options['<table>'] and self.options['<id>']:
			datasets[self.options['<table>']] = self.options['<id>']
		
		# Otherwise, fetch datasets config
		elif self.options['--list']:
			with open(self.options['--list']) as datasets_yaml:
				datasets = yaml.load(datasets_yaml)
		
		# Load config file
		with open(self.options['--config']) as config_json:
			config = json.load(config_json)
		
		extractor = SDEtoWKT(config['workspace'], spatial_reference=config['spatialReference'])
		pusher = WKTtoSocrata(self.options['--config'], config['controlTemplatePath'],
							config['datasyncPath'], temp_path=config['tempPath'])
			
		# For each table in datasets config
		for table in datasets:
			table_contents = extractor.get_table(table)
				
			print('Pushing %s to %s/d/%s' % (table, config['domain'], datasets[table]))
			
			pusher.push(table_contents.fields, table_contents.rows, datasets[table], 
						table_name=table)