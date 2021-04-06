from mixer.backend.django import mixer

from mpd_graphql.models import Identifier, IdentifierType

from .mpd_graphql import MPDGraphQLTestCase


IDENTIFIERS_QUERY = '''
query identifiers {
    identifiers {
        id
        identifierType {
            id
            name
        }
        value
    }
}
'''

IDENTIFIER_TYPES_QUERY = '''
query identifierTypes {
    identifierTypes {
        id
        name
        description
    }
}
'''

UPDATE_IDENTIFIER_MUTATION = '''
mutation updateIdentifier($identifier: IdentifierInput!) {
    updateIdentifier(identifier: $identifier) {
        identifier {
            id
            identifierType {
                id
                name
            }
            value
        }
    }
}
'''

UPDATE_IDENTIFIER_TYPE_MUTATION = '''
mutation updateIdentifierType($identifierType: IdentifierTypeInput!) {
    updateIdentifierType(identifierType: $identifierType) {
        identifierType {
            id
            name
            description
        }
    }
}
'''


class IdentifierUnitTestCase(MPDGraphQLTestCase):

    def setUp(self):
        super().setUp()
        self.identifier_type1 = mixer.blend(IdentifierType)
        self.identifier_type2 = mixer.blend(IdentifierType)
        self.identifier1 = mixer.blend(Identifier,
                                       identifier_type=self.identifier_type1)
        self.identifier2 = mixer.blend(Identifier,
                                       identifier_type=self.identifier_type2)

    def test_identifiers(self):

        response = self.client.execute(IDENTIFIERS_QUERY, {})
        data = response.data
        # print('identifiers data', data)

        assert len(data['identifiers']) == 2

    def test_identifier_types(self):

        response = self.client.execute(IDENTIFIER_TYPES_QUERY, {})
        data = response.data
        # print('identifier_types data', data)

        assert len(data['identifierTypes']) == 2

    def test_update_identifier(self):

        value = 'Updated Value'
        variables = {
            'identifier': {
                'id': self.identifier1.id,
                'identifierType': {
                    'id': self.identifier_type2.id,
                },
                'value': value,
            }
        }
        response = self.client.execute(UPDATE_IDENTIFIER_MUTATION, variables)
        data = response.data
        print('data', data)

        identifier = data['updateIdentifier']['identifier']
        self.assertEqual(identifier['value'], value)
        self.assertEqual(int(identifier['identifierType']['id']), self.identifier_type2.id)

    def test_update_identifier_type(self):

        name = 'Updated Name'
        description = 'Updated description'
        variables = {
            'identifierType': {
                'id': self.identifier_type1.id,
                'name': name,
                'description': description,
            }
        }
        response = self.client.execute(UPDATE_IDENTIFIER_TYPE_MUTATION, variables)
        data = response.data
        print('update_identifier_type data', data)

        identifier_type = data['updateIdentifierType']['identifierType']
        self.assertEqual(identifier_type['name'], name)
        self.assertEqual(identifier_type['description'], description)
