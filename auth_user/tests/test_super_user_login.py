from rest_framework import test, status

from test_utils import auth
from test_utils.test_client import APITestClient


class SuperAdminAuthTestCase(test.APITestCase):

    @staticmethod
    def success_data():
        return {"username": auth.create_test_user()["email"], "password": "1234"}

    def setUp(self):
        self.client: APITestClient = APITestClient(auth=False)

    def test_login_super_admin(self):
        """
        Test case for super admin login functionality.
        This test verifies that a super admin can successfully log in through the API endpoint.
        """

        response = self.client.post("/api/auth/admin/login", data=self.success_data())

        response_data = response.json()
        self.assertTrue(response_data["is_success"])
        self.assertEqual(
            response_data["messages"]["message"], "Logged in successfully."
        )

        self.assertIn("token", response_data["data"])

        self.assertIn("created_dtm", response_data["data"])
        self.assertIsNone(response_data["errors"])

        self.assertEqual(response_data["status_code"], status.HTTP_201_CREATED)

        return True

    @staticmethod
    def wrong_cred_data():
        return {"username": "wrong.cred.user@gmail.com", "password": "123467"}

    def test_wrong_cred_super_admin(self):
        """
        Test case for super admin login with wrong credentials.
        This test verifies that the login endpoint returns appropriate error response
        when incorrect credentials are provided for super admin login.
        """

        response = self.client.post(
            "/api/auth/admin/login", data=self.wrong_cred_data()
        )

        response_data = response.json()

        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

        self.assertIsNone(response_data["data"])
        self.assertIsNone(response_data["messages"])
        self.assertFalse(response_data["is_success"])
        self.assertEqual(response_data["errors"]["code"], "WRONG_CREDENTIALS")
        self.assertEqual(response_data["errors"]["message"], "Wrong Credentials.")

        return True

    @staticmethod
    def wrong_password_data():
        return {"username": auth.create_test_user()["email"], "password": "12345"}

    def test_wrong_password_only_super_admin(self):
        """Test super admin login with wrong password.
        This test case verifies that attempting to login as super admin with wrong password returns
        appropriate error response with 401 unauthorized status code.
        """

        response = self.client.post(
            "/api/auth/admin/login", data=self.wrong_password_data()
        )

        response_data = response.json()

        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

        self.assertIsNone(response_data["data"])
        self.assertIsNone(response_data["messages"])
        self.assertFalse(response_data["is_success"])
        self.assertEqual(response_data["errors"]["code"], "WRONG_CREDENTIALS")
        self.assertEqual(response_data["errors"]["message"], "Wrong Credentials.")

        return True

    @staticmethod
    def wrong_data_format_data():
        return {"username": "eml", "password": ""}

    def test_wrong_email_format_super_admin(self):
        """Test super admin login with invalid email format and blank password."""

        response = self.client.post(
            "/api/auth/admin/login", data=self.wrong_data_format_data()
        )

        response_data = response.json()

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertFalse(response_data["is_success"])
        self.assertEqual(response_data["status_code"], status.HTTP_400_BAD_REQUEST)
        self.assertIsNone(response_data["data"])
        self.assertIsNone(response_data["messages"])

        self.assertEqual(len(response_data["errors"]), 2)

        self.assertEqual(response_data["errors"][0]["field"], "username")
        self.assertEqual(response_data["errors"][0]["code"], "INVALID")
        self.assertEqual(
            response_data["errors"][0]["message"], "Enter a valid email address."
        )

        self.assertEqual(response_data["errors"][1]["field"], "password")
        self.assertEqual(response_data["errors"][1]["code"], "BLANK")
        self.assertEqual(
            response_data["errors"][1]["message"], "This field may not be blank."
        )

        return True
