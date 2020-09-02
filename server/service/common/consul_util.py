from flask_consulate import Consul
import requests


def apply_consul_config(app, service_name, port, tags=[]):
    @app.route('/healthcheck')
    def health_check():
        """
        This function is used to say current status to the Consul.
        Format: https://www.consul.io/docs/agent/checks.html
        :return: Empty response with status 200, 429 or 500
        """
        # TODO: implement any other checking logic.
        return '', 200

    # Consul
    # This extension should be the first one if enabled:
    consul = Consul(app=app)
    # Fetch the configuration:
    consul.apply_remote_config(namespace='amrev/')
    # Register Consul service:
    if service_name not in tags:
        tags.append(service_name)
    consul.register_service(
        name=service_name,
        interval='10s',
        tags=tags,
        port=port,
        httpcheck='http://localhost:{}/healthcheck'.format(port)
    )
    return consul


def resolve_service(service_name):
    url = "http://localhost:8500/v1/catalog/service/{}".format(service_name)
    resp = requests.get(url)
    r = resp.json()
    return r["Address"], r['ServicePort']
