import requests

jwt_cache = {}
HOST = '127.0.0.1:8000'


def get_jwt(open_id):
    if open_id not in jwt_cache:
        login_url = 'http://%s/api/v1/auth_token/' % HOST
        response = requests.post(login_url, json={'username': 'convert', 'password': 'tsimage666'})
        if response.status_code != 200:
            raise Exception('can not logins', response.json())
        jwt_cache[open_id] = 'JWT {}'.format(response.json()['token'])
    return jwt_cache[open_id]
