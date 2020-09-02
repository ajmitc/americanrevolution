from service.common.consul_util import resolve_service
import requests


class LocationClient:
    def __init__(self):
        self.address, self.port = resolve_service("location-service")

    def get_locations(self):
        """ Returns [{'id': 'userid...', 'name': 'my name', ...}] """
        resp = requests.get("{}:{}/locations".format(self.address, self.port))
        return resp.json()

    def get_location(self, uuid):
        """ Returns [{'id': 'userid...', 'name': 'my name', ...}] """
        resp = requests.get("{}:{}/locations".format(self.address, self.port), {"id": uuid})
        return resp.json()

    def update_location(self, locdict):
        """ Returns {'success': True|False, 'message': 'my message'} """
        resp = requests.post("{}:{}/location".format(self.address, self.port), json=locdict)
        return resp.json()
