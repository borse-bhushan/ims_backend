# from rest_framework import test

import django
import os

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "ims.settings")  # adjust accordingly
django.setup()

from django.test import TestCase



class AuditLogTest(TestCase):

    def test_data(self):
        print("Sad")
        return
