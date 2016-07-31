from json import dumps


class Sensor(object):

    def __init__(self, geojson_object=None, name=None, fields=None, location=None):
        """ Instantiates a Sensor object defining its structure
        either from a geojson object or from the related parameters.
        :param geojson_object: A dict loaded from a geojson object.
        :param name: The name of the sensor. Must only by used in
                     conjunction with fields.
        :param fields: A list of triples containing the name, data-type
                       and units of the sensor fields, as strings.
                       See GSN's documentation for a list of data-types.
        :param location: A triple giving the latitude, longitude and
                         altitude of the sensor, not mandatory.
        """
        assert geojson_object is None or (fields is None and name is None)

        if geojson_object:
            self.fields = [(f['name'], f['type'], f['unit'])
                           for f in geojson_object['properties']['fields']]
            self.name = geojson_object['properties']['vs_name']
            self.values = geojson_object['properties']['values']
            self.location = geojson_object['geometry']['coordinates']
        else:
            self.fields = fields
            self.name = name
            self.values = []
            self.location = location

    def to_geojson(self):

        r = {"type": "Feature",
             "properties": {"vs_name": self.name,
                            "values": self.values,
                            "fields": [{"name": f[0], "type": f[1], "unit": f[2]} for f in self.fields],
                            "stats": {},
                            "geographical": "",
                            "description": "Generated from python-gsn client"
                            },
             "geometry": {"type": "Point", "coordinates": self.location},
             "total_size": 1,
             "page_size": 1
             }
        return dumps(r)
