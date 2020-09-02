from service.common.consul_util import resolve_service
import requests


class GameUserClient:
    def __init__(self):
        self.address, self.port = resolve_service("game-user-service")

    def get_game_users(self):
        """ Returns [{'id': 'userid...', 'name': 'my name', ...}] """
        resp = requests.get("{}:{}/gameusers".format(self.address, self.port))
        return resp.json()

    def get_game_user(self, uuid):
        """ Returns [{'id': 'userid...', 'name': 'my name', ...}] """
        resp = requests.get("{}:{}/gameusers".format(self.address, self.port), {"id": uuid})
        return resp.json()

    def update_game_user(self, gameuserdict):
        """ Returns {'success': True|False, 'message': 'my message'} """
        resp = requests.post("{}:{}/gameuser".format(self.address, self.port), json=gameuserdict)
        return resp.json()
