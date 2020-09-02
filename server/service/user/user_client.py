from service.common.consul_util import resolve_service
import requests


class UserClient:
    def __init__(self):
        self.address, self.port = resolve_service("user-service")

    def get_users(self, filter=None):
        """ Returns [{'id': 'userid...', 'name': 'my name', ...}] """
        resp = requests.get("{}:{}/users".format(self.address, self.port), filter)
        return resp.json()

    def get_user(self, uuid):
        """ Returns [{'id': 'userid...', 'name': 'my name', ...}] """
        resp = requests.get("{}:{}/users".format(self.address, self.port), {"id": uuid})
        return resp.json()

    def update_user(self, userdict):
        """ Returns {'success': True|False, 'message': 'my message'} """
        resp = requests.post("{}:{}/user".format(self.address, self.port), json=userdict)
        return resp.json()

    def validate_user(self, username, access_token):
        data = {
            "username": username,
            "access_token": access_token
        }
        resp = requests.post("{}:{}/validate".format(self.address, self.port), json=data)
        return resp.json()

    def login(self, username, password):
        data = {
            "username": username,
            "password": password
        }
        resp = requests.post("{}:{}/login".format(self.address, self.port), json=data)
        return resp.json()
