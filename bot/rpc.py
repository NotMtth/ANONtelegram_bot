import json

import settings
import requests


class JsonRPC:
    def __init__(self, host, port):
        self.endpoint = f'http://{host}:{port}/json_rpc'

    def query_rpc(self, method, params):
        r = requests.get(self.endpoint, data=json.dumps({'method': method, 'params': params}))
        if error := r.json().get('error'):
            return error
        return r.json().get('result')


class Wallet(JsonRPC):

    def create_account(self):
        r = self.query_rpc('create_account', '')
        return r

    def balance(self, account_index, address_indices):
        r = self.query_rpc('get_balance', {'account_index': account_index, 'address_indices': address_indices})
        return r

    def new_address(self, account_index):
        r = self.query_rpc('create_address', {'account_index': account_index})
        return r

    def get_address(self, account_index):
        r = self.query_rpc('get_address', {'account_index': account_index})
        return r

    def transfer(self, account_index, amount, address):
        param = {'account_index': account_index, 'destinations': [{'amount': amount, 'address': address}],
                 'priority': 0, 'unlock_time': 0, 'get_tx_key': True, 'do_not_relay': False,
                 'ring_size': 22}
        r = self.query_rpc('transfer', param)
        return r

    def get_transfers(self, account_index):
        param = {'account_index': account_index, 'in': True, 'out': True, 'pending': True, 'failed': True, 'pool': True}
        r = self.query_rpc('get_transfers', param)
        return r

    def send_all(self, account_index, address):
        param = {'account_index': account_index, 'address': address,
                 'priority': 0, 'unlock_time': 0, 'get_tx_key': True, 'do_not_relay': False,
                 'ring_size': 22}
        r = self.query_rpc('sweep_all', param)
        return r


wallet = Wallet(settings.RPC, settings.RPC_PORT)
