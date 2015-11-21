import arcpy
import unicodecsv as csv
from slugify import slugify

arcpy.env.workspace = 'C:/Users/tim/Desktop/ArcGIS/GIS_SDE_VIEWER.gdb'

# Create SELECT statement
def get_fields(table):
	select = []
	headers = []
	desc = arcpy.Describe(table)
	fields = desc.fields
	for field in fields:
		if field.Type == 'Geometry':
			select.append(field.Name + '@WKT')
		else:
			select.append(field.Name)
			
		headers.append(slugify(field.Name, separator='_'))
		
	return select, headers


table = 'Healthy_corner_stores'
select, headers = get_fields(table)

with open('tmp/' + table + '.csv', 'wb') as f:
	writer = csv.writer(f)
	writer.writerow(headers)
	writer.writerows(arcpy.da.SearchCursor(table, select))
