===============================
Python wrapper for the Global Sensor Networks API
===============================

.. contents:: **Table of Contents**

-------------------------
Installation
-------------------------

    > pip install gsn

-------------------------
Usage
-------------------------

The wrapper uses the `sanction`_ Oauth2 library to authenticate against GSN services.
Before starting you must create a "client" on GSN services and get the client_id, client_secret and redirect_uri.
As we will be using client_credentials, the client must be linked to the user from which it will inherit the access rights.
The value of redirect uri is not used, but must nevertheless match.

Then in your python code, you can use it this way::

    > import gsn
    > a = gsn.API(service_url="http://localhost:9000/ws", client_id="client", client_secret="secret", redirect_uri="http://localhost")
    > s = a.get_latest_values("push")
    > s.values = [[1469959498000, 18]]
    > r = a.push_values(s)

.. _sanction: https://github.com/demianbrecht/sanction

Sensor object
===============================

This object abstract the json representation used by GSN for the stream elements.  It has the following fields:

* fields: list of triples representing the name, type and units
* name: name of the sensor
* values: list of lists. The inner lists must have the same size as the fields list and represent the data of a stream element.
* location: (optional) a triple representing the location of the sensor as latitude, longitude, altitude.
