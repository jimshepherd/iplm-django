from mixer.backend.django import mixer

from iplm_graphql.models import Property, PropertySpecification, PropertyType

from .iplm_graphql import IPLMGraphQLTestCase


PROPERTY_SPECIFICATIONS_QUERY = '''
query propertySpecifications {
    propertySpecifications {
        id
        name
        description
        propertyType {
            id
            name
        }
        values
        unit
    }
}
'''

PROPERTIES_QUERY = '''
query properties {
    properties {
        id
        propertyType {
            id
            name
        }
        specification {
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
            specification {
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


class PropertyUnitTestCase(IPLMGraphQLTestCase):

    def setUp(self):
        super().setUp()
        self.prop_type1 = mixer.blend(PropertyType)
        self.prop_type2 = mixer.blend(PropertyType)
        self.prop_spec1 = mixer.blend(PropertySpecification,
                                      property_type=self.prop_type1,
                                      values={'UL': 10, 'LL': 0})
        self.prop_spec2 = mixer.blend(PropertySpecification,
                                      property_type=self.prop_type2,
                                      values={'UL': 40, 'LL': 5})
        self.prop1 = mixer.blend(Property,
                                 property_type=self.prop_type1,
                                 specification=self.prop_spec1)
        self.prop2 = mixer.blend(Property,
                                 property_type=self.prop_type2,
                                 specification=self.prop_spec2)

    def test_properties(self):

        response = self.client.execute(PROPERTIES_QUERY, {})
        # print('test_properties response', response)
        data = response.data
        # print('test_properties data', data)

        assert len(data['properties']) == 2

    def test_property_specifications(self):

        response = self.client.execute(PROPERTY_SPECIFICATIONS_QUERY, {})
        print('test_property_specifications response', response)
        data = response.data
        print('test_property_specifications data', data)
        # print('test_property_specifications data', data)

        assert len(data['propertySpecifications']) == 2

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
                'id': self.prop1.id,
                'propertyType': {
                    'id': self.prop_type2.id,
                },
                'specification': {
                    'id': self.prop_spec2.id,
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
        self.assertEqual(int(prop['propertyType']['id']), self.prop_type2.id)
        self.assertEqual(int(prop['specification']['id']), self.prop_spec2.id)

    def test_update_property_type(self):

        name = 'Updated Name'
        description = 'Updated description'
        variables = {
            'propertyType': {
                'id': self.prop_type1.id,
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
