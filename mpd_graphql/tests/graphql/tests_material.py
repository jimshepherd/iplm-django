from mixer.backend.django import mixer

from mpd_graphql.models import \
    Attribute, Identifier, IdentifierType, Property, PropertyType, \
    Organization, \
    Material, MaterialSpecification

from .mpd_graphql import MPDGraphQLTestCase


MATERIALS_QUERY = '''
query materials {
    materials {
        id
        name
        description
        specification {
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

MATERIAL_SPECS_QUERY = '''
query MaterialSpecs {
    materialSpecs {
        id
        name
        description
        version
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
        supplier {
            id
            name
        }
    }
}
'''

UPDATE_MATERIAL_MUTATION = '''
mutation updateMaterial($material: MaterialInput!) {
    updateMaterial(material: $material) {
        material {
            id
            name
            description
            specification {
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

UPDATE_MATERIAL_SPEC_MUTATION = '''
mutation updateMaterialSpec($materialSpec: MaterialSpecificationInput!) {
    updateMaterialSpec(materialSpec: $materialSpec) {
        materialSpec {
            id
            name
            description
            version
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
            supplier {
                id
                name
            }
        }
    }
}
'''


class MaterialUnitTestCase(MPDGraphQLTestCase):

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
        self.prop1 = mixer.blend(Property,
                                 property_type=self.prop_type1)
        self.prop_type2 = mixer.blend(PropertyType)
        self.prop2 = mixer.blend(Property,
                                 property_type=self.prop_type2)

        self.org1 = mixer.blend(Organization)
        self.org2 = mixer.blend(Organization)

        self.mat_spec1 = mixer.blend(MaterialSpecification,
                                     attributes=[self.attr1],
                                     identifiers=[self.ident1],
                                     properties=[self.prop1],
                                     supplier=self.org1)
        self.mat_spec2 = mixer.blend(MaterialSpecification,
                                     attributes=[self.attr2],
                                     identifiers=[self.ident2],
                                     properties=[self.prop2],
                                     supplier=self.org2)

        self.mat1 = mixer.blend(Material,
                                specification=self.mat_spec1,
                                process=None,
                                process_step=None,
                                attributes=[self.attr1],
                                identifiers=[self.ident1],
                                properties=[self.prop1])
        self.mat2 = mixer.blend(Material,
                                specification=self.mat_spec2,
                                process=None,
                                process_step=None,
                                attributes=[self.attr2],
                                identifiers=[self.ident2],
                                properties=[self.prop2])

    def test_materials(self):

        response = self.client.execute(MATERIALS_QUERY, {})
        # print('test_materials response', response)
        data = response.data
        # print('test_materials data', data)

        assert len(data['materials']) == 2

    def test_material_specs(self):

        response = self.client.execute(MATERIAL_SPECS_QUERY, {})
        data = response.data
        # print('test_material_specs data', data)

        assert len(data['materialSpecs']) == 2

    def test_update_material(self):

        name = 'Updated name'
        description = 'Updated description'
        variables = {
            'material': {
                'id': self.mat1.id,
                'name': name,
                'description': description,
                'specification': {
                    'id': self.mat_spec2.id,
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
        response = self.client.execute(UPDATE_MATERIAL_MUTATION, variables)
        # print('test_update_material response', response)
        data = response.data
        # print('test_update_material data', data)

        mat = data['updateMaterial']['material']
        self.assertEqual(mat['name'], name)
        self.assertEqual(mat['description'], description)
        spec = mat['specification']
        self.assertEqual(int(spec['id']), self.mat_spec2.id)
        attrs = mat['attributes']
        self.assertEqual(len(attrs), 1)
        self.assertEqual(int(attrs[0]['id']), self.attr2.id)
        idents = mat['identifiers']
        self.assertEqual(len(idents), 1)
        self.assertEqual(int(idents[0]['id']), self.ident2.id)
        props = mat['properties']
        self.assertEqual(len(props), 1)
        self.assertEqual(int(props[0]['id']), self.prop2.id)

        # Make sure the update did not create a new properties
        props = Property.objects.all()
        self.assertEqual(len(props), 2)

    def test_update_material_spec(self):

        name = 'Updated Name'
        description = 'Updated description'
        version = 'Updated version'
        variables = {
            'materialSpec': {
                'id': self.mat_spec1.id,
                'name': name,
                'description': description,
                'version': version,
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
                'supplier': {
                    'id': self.org2.id,
                },
            }
        }
        response = self.client.execute(UPDATE_MATERIAL_SPEC_MUTATION, variables)
        data = response.data
        # print('test_update_material_spec data', data)

        mat_spec = data['updateMaterialSpec']['materialSpec']
        self.assertEqual(mat_spec['name'], name)
        self.assertEqual(mat_spec['description'], description)
        self.assertEqual(mat_spec['version'], version)
        attrs = mat_spec['attributes']
        self.assertEqual(len(attrs), 1)
        self.assertEqual(int(attrs[0]['id']), self.attr2.id)
        idents = mat_spec['identifiers']
        self.assertEqual(len(idents), 1)
        self.assertEqual(int(idents[0]['id']), self.ident2.id)
        props = mat_spec['properties']
        self.assertEqual(len(props), 1)
        self.assertEqual(int(props[0]['id']), self.prop2.id)
        supplier = mat_spec['supplier']
        self.assertEqual(int(supplier['id']), self.org2.id)
