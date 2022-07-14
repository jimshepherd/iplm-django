from mixer.backend.django import mixer

from mpd_graphql.models import \
    Attribute, Identifier, IdentifierType, Property, PropertyType, \
    Organization, \
    Equipment, EquipmentType

from .mpd_graphql import MPDGraphQLTestCase


EQUIPMENT_QUERY = '''
query equipment {
    equipment {
        id
        name
        description
        equipmentType {
            id
            name
        }
        organization {
            id
            name
        }
        attributes {
            id
            name
        }
        identifiers {
            id
            identifierType {
                id
                name
            }
            value
        }
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
}
'''

MATERIAL_TYPES_QUERY = '''
query EquipmentTypes {
    equipmentTypes {
        id
        name
        description
    }
}
'''

UPDATE_EQUIPMENT_MUTATION = '''
mutation updateEquipment($equipment: EquipmentInput!) {
    updateEquipment(equipment: $equipment) {
        equipment {
            id
            name
            description
            equipmentType {
                id
                name
            }
            organization {
                id
                name
            }
            attributes {
                id
                name
            }
            identifiers {
                id
                identifierType {
                    id
                    name
                }
                value
            }
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
    }
}
'''

UPDATE_EQUIPMENT_TYPE_MUTATION = '''
mutation updateEquipmentType($equipmentType: EquipmentTypeInput!) {
    updateMaterialType(equipmentType: $equipmentType) {
        equipmentType {
            id
            name
            description
        }
    }
}
'''


class EquipmentUnitTestCase(MPDGraphQLTestCase):

    def setUp(self):
        super().setUp()
        self.attr1 = mixer.blend(Attribute)
        self.attr2 = mixer.blend(Attribute)
        self.ident_type1 = mixer.blend(IdentifierType)
        self.ident1 = mixer.blend(Identifier,
                                  identifier_type=self.ident_type1)
        self.ident_type2 = mixer.blend(IdentifierType)
        self.ident2 = mixer.blend(Identifier,
                                  identifier_type=self.ident_type2)
        self.prop_type1 = mixer.blend(PropertyType)
        self.prop_spec1 = mixer.blend(PropertySpecification,
                                      property_type=self.prop_type1,
                                      values={})
        self.prop1 = mixer.blend(Property,
                                 property_type=self.prop_type1,
                                 specification=self.prop_spec1)
        self.prop_type2 = mixer.blend(PropertyType)
        self.prop_spec2 = mixer.blend(PropertySpecification,
                                      property_type=self.prop_type2,
                                      values={})
        self.prop2 = mixer.blend(Property,
                                 property_type=self.prop_type2,
                                 specification=self.prop_spec2)

        self.org1 = mixer.blend(Organization)
        self.org2 = mixer.blend(Organization)

        self.equip_type1 = mixer.blend(EquipmentType)
        self.equip_type2 = mixer.blend(EquipmentType)

        self.equip1 = mixer.blend(Equipment,
                                equipment_type=self.equip_type1,
                                organization=self.org1,
                                attributes=[self.attr1],
                                identifiers=[self.ident1],
                                properties=[self.prop1])
        self.equip2 = mixer.blend(Equipment,
                                equipment_type=self.equip_type2,
                                organization=self.org2,
                                attributes=[self.attr2],
                                identifiers=[self.ident2],
                                properties=[self.prop2])

    def test_equipment(self):

        response = self.client.execute(EQUIPMENT_QUERY, {})
        if response.errors is not None:
            print('test_equipment response', response)
        data = response.data
        # print('test_equipment data', data)

        assert len(data['equipment']) == 2

    def test_equipment_types(self):

        response = self.client.execute(EQUIPMENT_TYPES_QUERY, {})
        if response.errors is not None:
            print('test_equipment_types response', response)
        data = response.data
        # print('test_equipment_types data', data)

        assert len(data['equipmentTypes']) == 2

    def test_update_equipment(self):

        name = 'Updated name'
        description = 'Updated description'
        variables = {
            'equipment': {
                'id': self.equip1.id,
                'name': name,
                'description': description,
                'equipmentType': {
                    'id': self.equip_type2.id,
                },
                'organization': {
                    'id': self.org2.id,
                },
                'attributes': [
                    {
                        'id': self.attr2.id,
                    }
                ],
                'identifiers': [
                    {
                        'id': self.ident2.id,
                    }
                ],
                'properties': [
                    {
                        'id': self.prop2.id,
                    }
                ],
            }
        }
        response = self.client.execute(UPDATE_EQUIPMENT_MUTATION, variables)
        if response.errors is not None:
            print('test_update_equipment response', response)
        data = response.data
        # print('test_update_equipment data', data)

        equip = data['updateEquipment']['equipment']
        self.assertEqual(equip['name'], name)
        self.assertEqual(equip['description'], description)
        equip_type = equip['materialType']
        self.assertEqual(int(equip_type['id']), self.equip_type2.id)
        org = equip['organization']
        self.assertEqual(int(org['id']), self.org2.id)
        attrs = equip['attributes']
        self.assertEqual(len(attrs), 1)
        self.assertEqual(int(attrs[0]['id']), self.attr2.id)
        idents = equip['identifiers']
        self.assertEqual(len(idents), 1)
        self.assertEqual(int(idents[0]['id']), self.ident2.id)
        props = equip['properties']
        self.assertEqual(len(props), 1)
        self.assertEqual(int(props[0]['id']), self.prop2.id)

        # Make sure the update did not create a new properties
        props = Property.objects.all()
        self.assertEqual(len(props), 2)

    def test_update_equipment_type(self):

        name = 'Updated Name'
        description = 'Updated description'
        variables = {
            'equipmentType': {
                'id': self.mat_spec1.id,
                'name': name,
                'description': description,
            }
        }
        response = self.client.execute(UPDATE_EQUIPMENT_TYPE_MUTATION, variables)
        if response.errors is not None:
            print('test_update_equipment_type response', response)
        data = response.data
        # print('test_update_equipment_type data', data)

        equip_type = data['updateEquipmentType']['equipmentType']
        self.assertEqual(equip_type['name'], name)
        self.assertEqual(equip_type['description'], description)
