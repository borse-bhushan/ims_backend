import os

from utils import settings
from utils.functions import get_uuid

from test_utils.test_case_base import TestCaseBase


class TenantConfigurationTestCase(TestCaseBase):

    def setUp(self):
        from tenant.tests.test_tenant import TenantTestCase

        self.path = "/api/tenant/{tenant_id}/configuration"
        self.tenant = TenantTestCase().setUp()

        return super().setUp()

    @staticmethod
    def valid_tenant_conf_data():
        return {"authentication_type": "JWT_TOKEN", "database_strategy": "SHARED"}

    def test_create_tenant_configuration(self):
        data = self.valid_tenant_conf_data()
        tenant = self.tenant.test_tenant_create()
        response = self.client.post(
            self.path.format(tenant_id=tenant["data"]["tenant_id"]), data=data
        )
        response_data = response.json()

        self.created_successfully_201(response_data)

        self.assertEqual(
            response_data["data"]["database_strategy"], data["database_strategy"]
        )
        self.assertEqual(
            response_data["data"]["authentication_type"], data["authentication_type"]
        )

        return response_data

    @staticmethod
    def valid_tenant_conf_data_with_auth_token():
        return {"authentication_type": "TOKEN", "database_strategy": "SHARED"}

    def test_create_tenant_configuration_with_auth_token(self):
        data = self.valid_tenant_conf_data_with_auth_token()
        tenant = self.tenant.test_tenant_create()
        response = self.client.post(
            self.path.format(tenant_id=tenant["data"]["tenant_id"]), data=data
        )
        response_data = response.json()

        self.created_successfully_201(response_data)

        self.assertEqual(
            response_data["data"]["database_strategy"], data["database_strategy"]
        )
        self.assertEqual(
            response_data["data"]["authentication_type"], data["authentication_type"]
        )

        return response_data

    @staticmethod
    def valid_tenant_conf_data_with_separate_db():
        return {"authentication_type": "JWT_TOKEN", "database_strategy": "SEPARATE"}

    def test_create_tenant_configuration_with_separate_db(self):
        data = self.valid_tenant_conf_data_with_separate_db()
        tenant = self.tenant.test_tenant_create()

        response = self.client.post(
            self.path.format(tenant_id=tenant["data"]["tenant_id"]), data=data
        )
        response_data = response.json()

        self.created_successfully_201(response_data)

        self.assertEqual(
            response_data["data"]["database_strategy"], data["database_strategy"]
        )
        self.assertEqual(
            response_data["data"]["authentication_type"], data["authentication_type"]
        )

        self.remove_extra_created_db()

        return response_data

    def remove_extra_created_db(self):
        DATABASES = settings.read("DATABASES")

        del_dbs = []
        for db in DATABASES:
            if db == "default":
                continue

            del_dbs.append(db)
            database = DATABASES[db]

            os.remove(settings.read("BASE_DIR") / database["NAME"])

        for del_db in del_dbs:
            del DATABASES[del_db]

    @staticmethod
    def invalid_data():
        return {}

    def test_create_tenant_conf_invalid_data(self):
        data = self.invalid_data()
        tenant = self.tenant.test_tenant_create()
        response = self.client.post(
            self.path.format(tenant_id=tenant["data"]["tenant_id"]), data=data
        )
        response_data = response.json()
        self.bad_request_404(response_data)

        self.assertEqual(len(response_data["errors"]), 1)
        self.assertEqual(response_data["errors"][0]["field"], "authentication_type")
        self.assertEqual(response_data["errors"][0]["code"], "REQUIRED")
        self.assertEqual(
            response_data["errors"][0]["message"], "This field is required."
        )

        return True

    @staticmethod
    def tenant_cong_none_or_blank_data():
        return {"authentication_type": None, "database_strategy": ""}

    def test_create_tenant_conf_none_or_blank_data(self):
        data = self.tenant_cong_none_or_blank_data()
        tenant = self.tenant.test_tenant_create()
        response = self.client.post(
            self.path.format(tenant_id=tenant["data"]["tenant_id"]), data=data
        )
        response_data = response.json()
        self.bad_request_404(response_data)

        self.assertEqual(len(response_data["errors"]), 2)

        self.assertEqual(response_data["errors"][0]["field"], "authentication_type")
        self.assertEqual(response_data["errors"][0]["code"], "NULL")
        self.assertEqual(
            response_data["errors"][0]["message"], "This field may not be null."
        )

        self.assertEqual(response_data["errors"][1]["field"], "database_strategy")
        self.assertEqual(response_data["errors"][1]["code"], "INVALID_CHOICE")
        self.assertEqual(
            response_data["errors"][1]["message"], '"" is not a valid choice.'
        )

        return True
