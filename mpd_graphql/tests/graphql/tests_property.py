from mixer.backend.django import mixer

from mpd_graphql.models import Property, PropertyType

from .mpd_graphql import MPDGraphQLTestCase


PROPERTIES_QUERY = '''
query properties {
    properties {
        id
        propertyType {
            id
            name
        }
        intValue
        floatValue
        textValue
        unit
    }
}
'''

PROPERTY_TYPES_QUERY = '''
query propertyTypes {
    propertyTypes {
        id
        name
        description
    }
}
'''

UPDATE_PROPERTY_MUTATION = '''
mutation updateProperty($property: PropertyInput!) {
    updateProperty(property: $property) {
        property {
            id
            propertyType {
                id
                name
            }
            intValue
            floatValue
            textValue
            unit
        }
    }
}
'''

UPDATE_PROPERTY_TYPE_MUTATION = '''
mutation updatePropertyType($propertyType: PropertyTypeInput!) {
    updatePropertyType(propertyType: $propertyType) {
        propertyType {
            id
            name
            description
        }
    }
}
'''


class PropertyUnitTestCase(MPDGraphQLTestCase):

    def setUp(self):
        super().setUp()
        self.property_type1 = mixer.blend(PropertyType)
        self.property_type2 = mixer.blend(PropertyType)
        self.property1 = mixer.blend(Property,
                                     property_type=self.property_type1)
        self.property2 = mixer.blend(Property,
                                     property_type=self.property_type2)

    def test_properties(self):

        response = self.client.execute(PROPERTIES_QUERY, {})
        # print('test_properties response', response)
        data = response.data
        # print('test_properties data', data)

        assert len(data['properties']) == 2

    def test_property_types(self):

        response = self.client.execute(PROPERTY_TYPES_QUERY, {})
        data = response.data
        # print('test_property_types data', data)

        assert len(data['propertyTypes']) == 2

    def test_update_property(self):

        int_value = 123
        float_value = 4.56
        text_value = '789'
        unit = 'mm'
        variables = {
            'property': {
                'id': self.property1.id,
                'propertyType': {
                    'id': self.property_type2.id,
                },
                'intValue': int_value,
                'floatValue': float_value,
                'textValue': text_value,
                'unit': unit,
            }
        }
        response = self.client.execute(UPDATE_PROPERTY_MUTATION, variables)
        print('test_update_property response', response)
        data = response.data
        print('test_update_property data', data)

        prop = data['updateProperty']['property']
        self.assertEqual(prop['intValue'], int_value)
        self.assertEqual(prop['floatValue'], float_value)
        self.assertEqual(prop['textValue'], text_value)
        self.assertEqual(prop['unit'], unit)
        self.assertEqual(int(prop['propertyType']['id']), self.property_type2.id)

    def test_update_property_type(self):

        name = 'Updated Name'
        description = 'Updated description'
        variables = {
            'propertyType': {
                'id': self.property_type1.id,
                'name': name,
                'description': description,
            }
        }
        response = self.client.execute(UPDATE_PROPERTY_TYPE_MUTATION, variables)
        data = response.data
        # print('test_update_property_type data', data)

        property_type = data['updatePropertyType']['propertyType']
        self.assertEqual(property_type['name'], name)
        self.assertEqual(property_type['description'], description)
