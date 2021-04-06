from mixer.backend.django import mixer

from mpd_graphql.models import Attribute

from .mpd_graphql import MPDGraphQLTestCase


ATTRIBUTES_QUERY = '''
query attributes($parent: AttributeInput) {
    attributes(parent: $parent) {
        id
        name
        description
        parent {
            id
            name
        }
    }
}
'''

UPDATE_ATTRIBUTE_MUTATION = '''
mutation updateAttribute($attribute: AttributeInput!) {
    updateAttribute(attribute: $attribute) {
        attribute {
            id
            name
            description
            parent {
                id
                name
            }
        }
    }
}
'''


class AttributeUnitTestCase(MPDGraphQLTestCase):

    def setUp(self):
        super().setUp()
        self.attribute1 = mixer.blend(Attribute)
        self.parent_attribute = mixer.blend(Attribute)
        self.child_attribute = mixer.blend(Attribute, parent=self.parent_attribute)

    def test_attributes(self):

        response = self.client.execute(ATTRIBUTES_QUERY, {})
        data = response.data
        # print('attributes data', data)

        assert len(data['attributes']) == 3

    def test_attributes_with_parent(self):

        variables = {'parent': {'id': self.parent_attribute.id}}
        response = self.client.execute(ATTRIBUTES_QUERY, variables)
        data = response.data
        #print('data', data)

        attributes = data['attributes']
        self.assertEqual(len(attributes), 1)
        attribute1 = attributes[0]
        self.assertEqual(int(attribute1['id']), self.child_attribute.id)

    def test_update_attribute(self):

        name = 'Updated Name'
        description = 'Updated description'
        variables = {
            'attribute': {
                'id': self.attribute1.id,
                'name': name,
                'description': description,
                'parent': {
                    'id': self.parent_attribute.id,
                }
            }
        }
        response = self.client.execute(UPDATE_ATTRIBUTE_MUTATION, variables)
        data = response.data
        print('data', data)

        attribute = data['updateAttribute']['attribute']
        self.assertEqual(attribute['name'], name)
        self.assertEqual(attribute['description'], description)
        self.assertEqual(int(attribute['parent']['id']), self.parent_attribute.id)
