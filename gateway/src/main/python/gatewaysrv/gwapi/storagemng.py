import os
from threading import Timer

import roundrobin
import storage_client
from storage_client.api import default_api
from storage_client.model.status_response import StatusResponse
from urllib3.exceptions import MaxRetryError


class RepeatTimer(Timer):
    def run(self):
        while not self.finished.wait(self.interval):
            self.function(*self.args, **self.kwargs)


def process_servers():
    return set(os.getenv('STORAGE_SERVERS', '').split(';'))


def get_api_client(server: str):
    configuration = storage_client.Configuration(
        host=server
    )
    return default_api.DefaultApi(storage_client.ApiClient(configuration))


def get_server_clients(srvrs: set[str]) -> dict[str, default_api.DefaultApi]:
    srvrs_ac = dict()
    for srv in srvrs:
        srvrs_ac[srv] = get_api_client(srv)
    return srvrs_ac


servers: set[str] = process_servers()

server_clients: dict[str, default_api.DefaultApi] = get_server_clients(servers)

live_servers: set[str] = set()
live_servers_cycle: roundrobin.basic = roundrobin.basic(set())


def update_live_servers():
    new_live_servers: set[str] = set()
    global live_servers
    for srv in servers:
        try:
            resp: StatusResponse = server_clients[srv].storageapi_api_status_get(_request_timeout=1)
            if resp.status == "UP":
                new_live_servers.add(srv)
        except (storage_client.ApiException, MaxRetryError):
            pass
    if len(new_live_servers) == len(live_servers) and len(new_live_servers.difference(live_servers)) == 0:
        pass
    else:
        live_servers = new_live_servers
        global live_servers_cycle
        live_servers_cycle = roundrobin.basic(live_servers)


live_servers_updater = RepeatTimer(5, update_live_servers)
live_servers_updater.start()


def get_status():
    if len(live_servers) > 0:
        return {
            'status': 'UP'
        }
    else:
        return {
            'status': 'DOWN'
        }, 503


def get_data():
    if len(live_servers) > 0:
        try:
            return server_clients[live_servers_cycle()].storageapi_api_data_get(_request_timeout=5)
        except (storage_client.ApiException, MaxRetryError):
            return {}, 503
    return {}, 503
