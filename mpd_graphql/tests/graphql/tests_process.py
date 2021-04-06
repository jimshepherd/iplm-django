from mixer.backend.django import mixer

from mpd_graphql.models import \
    Attribute, Identifier, IdentifierType, Property, PropertyType, \
    Organization, \
    Process, ProcessMethod

from .mpd_graphql import MPDGraphQLTestCase


PROCESSES_QUERY = '''
query processes {
    processes {
        id
        name
        description
        method {
            id
            name
        }
        producer {
            id
            name
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
            method {
                id
                name
            }
            producer {
                id
                name
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
        }
    }
}
'''


class ProcessUnitTestCase(MPDGraphQLTestCase):

    def setUp(self):
        super().setUp()
        self.org1 = mixer.blend(Organization)
        self.org2 = mixer.blend(Organization)

        self.method1 = mixer.blend(ProcessMethod,
                                   parent=None)
        self.method2 = mixer.blend(ProcessMethod,
                                   parent=self.method1)
        self.method3 = mixer.blend(ProcessMethod,
                                   parent=None)

        self.process1 = mixer.blend(Process,
                                    method=self.method1,
                                    producer=self.org1)
        self.process2 = mixer.blend(Process,
                                    method=self.method2,
                                    producer=self.org2)

    def test_processes(self):

        response = self.client.execute(PROCESSES_QUERY, {})
        # print('test_processes response', response)
        data = response.data
        # print('test_processes data', data)

        assert len(data['processes']) == 2

    def test_process_methods(self):

        response = self.client.execute(PROCESS_METHODS_QUERY, {})
        #print('test_process_methods response', response)
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
                'method': {
                    'id': self.method2.id,
                },
                'producer': {
                    'id': self.org2.id,
                },
            }
        }
        response = self.client.execute(UPDATE_PROCESS_MUTATION, variables)
        # print('test_update_process response', response)
        data = response.data
        # print('test_update_process data', data)

        process = data['updateProcess']['process']
        self.assertEqual(process['name'], name)
        self.assertEqual(process['description'], description)
        method = process['method']
        self.assertEqual(int(method['id']), self.method2.id)
        producer = process['producer']
        self.assertEqual(int(producer['id']), self.org2.id)

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
            }
        }
        response = self.client.execute(UPDATE_PROCESS_METHOD_MUTATION, variables)
        data = response.data
        # print('test_update_process_method data', data)

        method = data['updateProcessMethod']['processMethod']
        self.assertEqual(method['name'], name)
        self.assertEqual(method['description'], description)
        self.assertEqual(method['version'], version)
        parent = method['parent']
        self.assertEqual(int(parent['id']), self.method3.id)
