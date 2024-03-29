from django.contrib.auth import get_user_model
from graphql_jwt.testcases import JSONWebTokenTestCase

from iplm.schema import schema


class IPLMGraphQLTestCase(JSONWebTokenTestCase):
    GRAPHQL_SCHEMA = schema

    def setUp(self):
        super().setUp()
        self.user = get_user_model().objects.create(username='test')
        self.client.authenticate(self.user)
