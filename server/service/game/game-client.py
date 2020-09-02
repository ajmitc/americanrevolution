from service.common.consul_util import resolve_service
import requests


class GameClient:
    def __init__(self):
        self.address, self.port = resolve_service("game-service")

    def get_game_users(self):
        """ Returns [{'id': 'userid...', 'name': 'my name', ...}] """
        resp = requests.get("{}:{}/games".format(self.address, self.port))
        return resp.json()

    def get_game_user(self, uuid):
        """ Returns [{'id': 'userid...', 'name': 'my name', ...}] """
        resp = requests.get("{}:{}/games".format(self.address, self.port), {"id": uuid})
        return resp.json()

    def update_game_user(self, gamedict):
        """ Returns {'success': True|False, 'message': 'my message'} """
        resp = requests.post("{}:{}/game".format(self.address, self.port), json=gamedict)
        return resp.json()
