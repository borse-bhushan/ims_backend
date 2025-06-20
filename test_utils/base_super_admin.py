from test_utils.test_client import APITestClient
from test_utils.comm_assert import CommonTestCaseAssertsBase


class TestCaseBase(CommonTestCaseAssertsBase):

    def setUp(self, auth=True):

        if auth:
            self.client = self.get_client(auth)

        return self

    def get_client(self, auth):
        client = APITestClient()

        if auth:
            from auth_user.tests.test_super_user_login import SuperAdminAuthTestCase

            admin = SuperAdminAuthTestCase()
            admin.setUp()
            admin_token = admin.test_login_super_admin()
            client = client.set_auth_header(admin_token)

        return client
