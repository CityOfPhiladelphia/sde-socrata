from collections import namedtuple

import arcpy
from slugify import slugify

class SDEtoWKT(object):
	Table = namedtuple('Results', ['fields', 'rows'])
	
	def __init__(self, workspace, spatial_reference=None, rename_geometry=None):
		"""
		workspace : path to the workspace
		spatial_reference : an arcpy.SpatialReference object
		rename_geometry : optionally, rename the geometry field to this
		"""
		arcpy.env.workspace = workspace
		self.spatial_reference = spatial_reference
		self.rename_geometry = rename_geometry
	
	def get_fields(self, table):
		"""
		Get fields formatted for query (w/WKT suffix)
		and formatted for databases (slugified)
		"""
		query = []
		slugs = []
		
		fields = arcpy.Describe(table).fields
		for field in fields:
			slug = slugify(field.Name, separator='_')
			
			if field.Type == 'Geometry':
				query.append(field.Name + '@WKT')
				slugs.append(self.rename_geometry or slug)
			else:
				query.append(field.Name)
				slugs.append(slug)
				
		return query, slugs
		
	def get_rows(self, table, fields=['*']):
		return arcpy.da.SearchCursor(table, fields, spatial_reference=self.spatial_reference)
		
	def get_table(self, table):
		"""
		Returns a Table object with 2 properties: fields, rows
		"""
		query, slugs = self.get_fields(table)
		rows = self.get_rows(table, query)
		return self.Table(slugs, rows)