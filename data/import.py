import django
import json
import os
import sys

# Make sure we can see the parent directory to import
sys.path.append('../')
os.environ['DJANGO_SETTINGS_MODULE'] = 'shipwrecks.settings'

# Make sure Django is set up
django.setup()

# Now we can import our Django model(s)
from wrecks.models import Wreck
from wrecks.models import WreckType
from wrecks.models import SOURCE_CHOICES

# Import the GEOS library needed to create points
from django.contrib.gis.geos import Point
from django.contrib.gis.geos import GEOSGeometry

if __name__ == '__main__':
    
    # Make sure we have specified a file to import
    if len(sys.argv) < 2:
        print 'You must specify a geojson file to import.'
        print 'Usage: $ python import.py <geojson file>'
        sys.exit()
    
    # Open the GeoJSON file
    json_filepath = sys.argv[-1]
    try:
        with open(json_filepath, 'r') as f:
            data = json.loads(f.read())
    except IOError:
        sys.exit("Error opening GeoJSON file")
    except ValueError:
        sys.exit('Error: the file does not appear to be valid JSON.')

    # Turn each feature into a Wreck model instance
    for feature_dict in data['features']:

        wreck = Wreck()
        properties = feature_dict['properties']

        # Figure out the source type
        source_name = properties['source']
        if source_name == 'enc_wrecks':
            source = SOURCE_CHOICES[1][0]
        else:
            source = SOURCE_CHOICES[0][0]

        # Figure out if the wreck type exists (and normalize the values)
        wreck_type_value = properties['feature_type']

        if not wreck_type_value:
            wreck_type_value = 'Unknown'
        else:
            if wreck_type_value.startswith('Wrecks -'):
                wreck_type_value = wreck_type_value.replace('Wrecks -', 'Wreck -')

        wreck_type, created = WreckType.objects.get_or_create(name=wreck_type_value)

        # Figure out the depth
        if source_name == 'enc_wrecks': 
            # ENC Wrecks are always in meters
            try:
                depth_meters = float(properties['depth'])
            except ValueError:
                depth_meters = None
        else:
            if not properties['depth']:
                depth_meters = None
            else:
                depth_value = properties['depth']
                sounding = properties['sounding']
                if 'meters' in sounding:
                    depth_meters = depth_value
                elif 'feet' in sounding:
                    # Convert feet and tenths to meters
                    depth_meters = depth_value * 0.3048
                elif 'fathoms' in sounding:
                    # Convert fathoms to meters
                    depth_meters = depth_value * 1.8288
                else:
                    depth_meters = None
        
        # Create the Point object from the lat and long
        lat = feature_dict['geometry']['coordinates'][1]
        lng = feature_dict['geometry']['coordinates'][0]
        location_point = GEOSGeometry('POINT(%f %f)' % (lng, lat), srid='NADS83')

        # Get the name or assign 'unknown'
        vessel_name = properties['vessel_name']
        if not vessel_name:
            vessel_name = 'Unknown'

        # Cast the year sunk into an integer
        try:
            year_sunk = int(properties['yearsunk'])
        except ValueError:
            year_sunk = None
        
        wreck.name = vessel_name
        wreck.history = properties['history']
        wreck.wreck_type = wreck_type
        wreck.year_sunk = year_sunk
        wreck.source = source
        wreck.source_identifier = feature_dict['id']
        wreck.depth_meters = depth_meters
        wreck.location = location_point
        
        # Save the new wreck
        wreck.save()
