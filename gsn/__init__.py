from sanction import Client, transport_headers
from .sensor import Sensor
try:
    from urllib2 import HTTPError
except:
    from urllib.error import HTTPError


class API(object):
    """ Global Sensor Networks api client object
    """

    def __init__(self, service_url=None, client_id=None, client_secret=None, redirect_uri=None):
        """ Instantiates a GSN API client to authorize and authenticate a user
        :param service_url: The authorization endpoint provided by GSN
                            services.
        :param client_id: The client ID.
        :param client_secret: The client secret.
        """
        assert service_url is not None
        assert client_id is not None and client_secret is not None

        self.client = Client(token_endpoint="{}/oauth2/token".format(service_url),
                             resource_endpoint="{}/api".format(service_url),
                             client_id=client_id, client_secret=client_secret,
                             token_transport=transport_headers
                             )
        self.client.request_token(grant_type='client_credentials', redirect_uri=redirect_uri)

    def get_latest_values(self, vs_name=None):
        """ Query the API to get the latest values of a given virtual sensor.
        :param vs_name: The name of the virtual sensor.
        :returns: A Sensor object.
        """
        assert vs_name is not None

        data = self.client.request("/sensors/{}?latestValues=True".format(vs_name))
        return Sensor(geojson_object=data)

    def push_values(self, sensor_data=None):
        """ Push sensor data into GSN's API. The corresponding virtual sensor
         must be of type zeromq-push.
        :param sensor_data: A Sensor object containing the sensor values.
        :returns: The server response.
        """

        assert sensor_data is not None

        try:
            res = self.client.request("/sensors/{}/data".format(sensor_data.name),
                                      data=sensor_data.to_geojson().encode('utf_8'),
                                      headers={'Content-type': 'application/json'})
        except HTTPError as e:
            return e.readlines()
        return res
