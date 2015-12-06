import json

import arcpy
from sodapy import Socrata
from slugify import slugify

from .base import Base

class Create(Base):
	def map_shape_type(self, shape_type):
		return {
			'Polygon': 'multipolygon',
			'Polyline': 'polyline',
			'Point': 'point',
			'MultiPoint': 'multipoint',
			'MultiPatch': 'multipatch',
		}[shape_type]
	
	def map_field_type(self, field_type, shape_type):
		return {
			'Blob': 'text',
			'Date': 'date',
			'Double': 'number',
			'Geometry': shape_type,
			'Guid': 'text',
			'Integer': 'number',
			'OID': 'number',
			'Raster': 'text',
			'Single': 'number',
			'SmallInteger': 'number',
			'String': 'text',
		}[field_type]
	
	def run(self):
		# Load config file
		with open(self.options['--config']) as config_json:
			config = json.load(config_json)
		
		arcpy.env.workspace = config['workspace']
		
		# Get fields
		desc = arcpy.Describe(self.options['<table>'])
		shape_type = self.map_shape_type(desc.shapeType)
		columns = []
		row_identifier = ''
		for field in desc.fields:
			field_name = slugify(field.name, separator='_')
			
			if(field.type == 'OID'):
				row_identifier = field_name
				
			columns.append({
				'fieldName': field_name,
				'name': field.aliasName,
				'dataTypeName': self.map_field_type(field.type, shape_type),
			})
		
		# Create dataset
		client = Socrata(config['domain'].lstrip('https://'), config['appToken'], 
				username=config['username'], password=config['password'])
		
		print('Creating %s' % desc.name)
		
		response = client.create(desc.name, columns=columns, row_identifier=row_identifier,
			new_backend=True)
		resource = response[u'id']
		if(resource):
			client.publish(resource)
			dataset_permission = 'private'
			
			if(self.options['--public']):
				client.set_permission(resource, 'public')
				dataset_permission = 'PUBLIC'
			
			print('Created %s dataset %s/d/%s' % (dataset_permission, config['domain'], resource))