import json
import requests
import xlrd

SOURCES = (
    ('awois_wrecks', 'http://wrecks.nauticalcharts.noaa.gov/downloads/AWOIS_Wrecks.xls'),
    ('enc_wrecks', 'http://wrecks.nauticalcharts.noaa.gov/downloads/ENC_Wrecks.xls'),
)

if __name__ == '__main__':

    for source_item in SOURCES:

        # Source and URL
        source_name = source_item[0]
        source_url = source_item[1]

        # Request the Excel spreadsheet from the URL
        request = requests.get(source_url)
        data = request.content
    
        # Open the data as an Excel Workbook and get the first sheet
        workbook = xlrd.open_workbook(file_contents=data)
        worksheet = workbook.sheets()[0]

        # We are going to create a GeoJSON Point feature for each row
        features = []

        # Iterate over all the rows in the worksheet
        for row_index in range(1, worksheet.nrows):

            # The row will be returned as an array of cell objects
            cells = worksheet.row(row_index)
        
            # Construct a GeoJSON Feature dictionary stub that we can fill in
            feature = {
                'type': 'Feature',
                'id': None,
                'geometry': {
                    'type': 'Point',
                    'coordinates': None,
                },
                'properties': {},
            }
        
            # The column layouts/values are different between the two sources
            if source_name == 'awois_wrecks':
                source_id = '%.0f' % cells[0].value
                vessel_name = cells[1].value
                feature_type = cells[2].value
                lat = float(cells[3].value)
                lng = float(cells[4].value)
                chart = None
                gp_quality = cells[5].value
                depth = cells[6].value
                sounding = cells[7].value
                year_sunk = cells[8].value
                history = cells[9].value
                sounding_quality = None
                water_level_effect = None
            else:
                source_id = None
                vessel_name = cells[1].value
                feature_type = cells[2].value
                chart = cells[3].value # Not Used
                lat = float(cells[4].value)
                lng = float(cells[5].value)
                gp_quality = cells[6].value
                depth = cells[7].value
                sounding = cells[8].value
                year_sunk = cells[9].value
                history = cells[10].value
                sounding_quality = cells[11].value
                water_level_effect = cells[12].value
        
            # Get the lat and lng from the cell values
            feature['geometry']['coordinates'] = (lng, lat)

            # Get the unique ID
            feature['id'] = source_id

            # Get the properties from the cell values
            feature['properties']['vessel_name'] = vessel_name
            feature['properties']['feature_type'] = feature_type
            feature['properties']['gp_quality'] = gp_quality
            feature['properties']['depth'] = depth
            feature['properties']['chart'] = chart
            feature['properties']['sounding'] = sounding
            feature['properties']['yearsunk'] = year_sunk
            feature['properties']['history'] = history
            feature['properties']['sounding_quality'] = sounding_quality
            feature['properties']['water_level_effect'] = water_level_effect
        
            # Add the source to the properties
            feature['properties']['source'] = source_name

            # Add the feature to our array
            features.append(feature)

        # Output the GeoJSON Feature Collection
        output = {
            "type": "FeatureCollection",
            "features": features
        }
    
        # Output to a GeoJSON file
        with open('%s.geojson' % source_name, 'w') as f:
            f.write(json.dumps(output, indent=4))

        print 'Done.'
