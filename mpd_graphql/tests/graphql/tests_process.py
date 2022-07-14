from mixer.backend.django import mixer

from mpd_graphql.models import \
    Attribute, \
    Equipment, EquipmentType, \
    Identifier, IdentifierType, \
    Organization, \
    Process, ProcessMethod, ProcessType, \
    Property, PropertyType, \
    PropertySpecification, \
    User

from .mpd_graphql import MPDGraphQLTestCase


PROCESSES_QUERY = '''
query processes {
    processes {
        id
        name
        description
        processType {
            id
            name
        }
        method {
            id
            name
        }
        producer {
            id
            name
        }
        equipment {
            id
            name
        }
        operator {
            id
            name
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

PROCESS_METHODS_QUERY = '''
query ProcessMethods {
    processMethods {
        id
        name
        description
        version
        parent {
            id
            name
        }
        processType {
            id
            name
        }
        equipmentType {
            id
            name
        }
        properties {
            id
            intValue
            floatValue
            textValue
            unit
        }
        propertySpecs {
            id
            name
        }
    }
}
'''

UPDATE_PROCESS_MUTATION = '''
mutation updateProcess($process: ProcessInput!) {
    updateProcess(process: $process) {
        process {
            id
            name
            description
            processType {
                id
                name
            }
            method {
                id
                name
            }
            producer {
                id
                name
            }
            equipment {
                id
                name
            }
            operator {
                id
                name
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

UPDATE_PROCESS_METHOD_MUTATION = '''
mutation updateProcessMethod($processMethod: ProcessMethodInput!) {
    updateProcessMethod(processMethod: $processMethod) {
        processMethod {
            id
            name
            description
            version
            parent {
                id
                name
            }
            processType {
                id
                name
            }
            equipmentType {
                id
                name
            }
            properties {
                id
                intValue
                floatValue
                textValue
                unit
            }
            propertySpecs {
                id
                name
            }
        }
    }
}
'''


class ProcessUnitTestCase(MPDGraphQLTestCase):

    def setUp(self):
        super().setUp()
        self.org1 = mixer.blend(Organization)
        self.org2 = mixer.blend(Organization)
        self.equip_type1 = mixer.blend(EquipmentType)
        self.equip_type2 = mixer.blend(EquipmentType)
        self.equip1 = mixer.blend(Equipment,
                                  equipment_type=self.equip_type1)
        self.equip2 = mixer.blend(Equipment,
                                  equipment_type=self.equip_type2)
        self.user1 = mixer.blend(User)
        self.user2 = mixer.blend(User)

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

        self.process_type1 = mixer.blend(ProcessType)
        self.process_type2 = mixer.blend(ProcessType)

        self.method1 = mixer.blend(ProcessMethod,
                                   parent=None,
                                   process_type=self.process_type1,
                                   equipment_type=self.equip_type1,
                                   properties=[self.prop1],
                                   property_specs=[self.prop_spec1])
        self.method2 = mixer.blend(ProcessMethod,
                                   parent=self.method1,
                                   process_type=self.process_type2,
                                   equipment_type=self.equip_type2,
                                   properties=[self.prop2],
                                   property_specs=[self.prop_spec2])
        self.method3 = mixer.blend(ProcessMethod,
                                   parent=None,
                                   process_type=self.process_type2,
                                   equipment_type=self.equip_type2,
                                   properties=[self.prop2],
                                   property_specs=[self.prop_spec2])

        self.process1 = mixer.blend(Process,
                                    process_type=self.process_type1,
                                    method=self.method1,
                                    producer=self.org1,
                                    equipment=self.equip1,
                                    operator=self.user1,
                                    properties=[self.prop1])
        self.process2 = mixer.blend(Process,
                                    process_type=self.process_type2,
                                    method=self.method2,
                                    producer=self.org2,
                                    equipment=self.equip2,
                                    operator=self.user2,
                                    properties=[self.prop2])

    def test_processes(self):

        response = self.client.execute(PROCESSES_QUERY, {})
        if response.errors is not None:
            print('test_processes response', response)
        data = response.data
        # print('test_processes data', data)

        assert len(data['processes']) == 2

    def test_process_methods(self):

        response = self.client.execute(PROCESS_METHODS_QUERY, {})
        if response.errors is not None:
            print('test_process_methods response', response)
        data = response.data
        # print('test_process_methods data', data)

        assert len(data['processMethods']) == 3

    def test_update_process(self):

        name = 'Updated name'
        description = 'Updated description'
        variables = {
            'process': {
                'id': self.process1.id,
                'name': name,
                'description': description,
                'processType': {
                    'id': self.process_type2.id,
                },
                'method': {
                    'id': self.method2.id,
                },
                'producer': {
                    'id': self.org2.id,
                },
                'equipment': {
                    'id': self.equip2.id,
                },
                'operator': {
                    'id': self.user2.id,
                },
                'properties': [
                    {
                        'id': self.prop2.id,
                    }
                ],
            }
        }
        response = self.client.execute(UPDATE_PROCESS_MUTATION, variables)
        if response.errors is not None:
            print('test_update_process response', response)
        data = response.data
        # print('test_update_process data', data)

        process = data['updateProcess']['process']
        self.assertEqual(process['name'], name)
        self.assertEqual(process['description'], description)
        process_type = process['processType']
        self.assertEqual(int(process_type['id']), self.process_type2.id)
        method = process['method']
        self.assertEqual(int(method['id']), self.method2.id)
        producer = process['producer']
        self.assertEqual(int(producer['id']), self.org2.id)
        equipment = process['equipment']
        self.assertEqual(int(equipment['id']), self.equip2.id)
        operator = process['operator']
        self.assertEqual(int(operator['id']), self.user2.id)
        props = process['properties']
        self.assertEqual(len(props), 1)
        self.assertEqual(int(props[0]['id']), self.prop2.id)

        # Make sure the update did not create a new properties
        props = Property.objects.all()
        self.assertEqual(len(props), 2)

    def test_update_process_method(self):

        name = 'Updated Name'
        description = 'Updated description'
        version = 'Updated version'
        variables = {
            'processMethod': {
                'id': self.method1.id,
                'name': name,
                'description': description,
                'version': version,
                'parent': {
                    'id': self.method3.id,
                },
                'processType': {
                    'id': self.process_type2.id,
                },
                'equipmentType': {
                    'id': self.equip_type2.id,
                },
                'properties': [
                    {
                        'id': self.prop2.id,
                    }
                ],
                'propertySpecs': [
                    {
                        'id': self.prop_spec2.id,
                    }
                ],
            }
        }
        response = self.client.execute(UPDATE_PROCESS_METHOD_MUTATION, variables)
        if response.errors is not None:
            print('test_update_process_method response', response)
        data = response.data
        # print('test_update_process_method data', data)

        method = data['updateProcessMethod']['processMethod']
        self.assertEqual(method['name'], name)
        self.assertEqual(method['description'], description)
        self.assertEqual(method['version'], version)
        parent = method['parent']
        self.assertEqual(int(parent['id']), self.method3.id)
        process_type = method['processType']
        self.assertEqual(int(process_type['id']), self.process_type2.id)
        equip_type = method['equipmentType']
        self.assertEqual(int(equip_type['id']), self.equip_type2.id)

        props = method['properties']
        self.assertEqual(len(props), 1)
        self.assertEqual(int(props[0]['id']), self.prop2.id)

        # Make sure the update did not create new properties
        props = Property.objects.all()
        self.assertEqual(len(props), 2)

        prop_specs = method['propertySpecs']
        self.assertEqual(len(prop_specs), 1)
        self.assertEqual(int(prop_specs[0]['id']), self.prop_spec2.id)

        # Make sure the update did not create new property specs
        prop_specs = PropertySpecification.objects.all()
        self.assertEqual(len(prop_specs), 2)
