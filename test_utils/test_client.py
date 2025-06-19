from rest_framework import test
from test_utils.auth import create_test_token


class APITestClient:

    def __init__(self, headers=None, auth=True, role_id=None):
        self.client = test.APIClient()

        self.headers = headers or {}

        if auth:
            self.set_auth_header(role_id)

    def set_auth_header(self, role_id):

        token = create_test_token(role_id)

        self.set_header(HTTP_AUTHORIZATION=f"Bearer {token['token']}")

    def set_header(self, key, value):
        self.headers[key] = value

    def get(self, path):
        return self.client.get(path, **self.headers)

    def post(self, path, data=None):
        return self.client.post(path, data=data, **self.headers)
