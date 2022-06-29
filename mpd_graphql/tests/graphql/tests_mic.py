import json

from mixer.backend.django import mixer

from mpd_graphql.models import Property, PropertySpecification, PropertyType

from .mpd_graphql import MPDGraphQLTestCase


MICS_QUERY = '''
query mics {
    mics {
        id
        name
        description
        micType {
            id
            name
        }
        values
        unit
    }
}
'''

MIC_VALUES_QUERY = '''
query micValues {
    micValues {
        id
        mic {
            id
            name
            micType {
                id
                name
            }
        }
        intValue
        floatValue
        textValue
        unit
    }
}
'''

MIC_TYPES_QUERY = '''
query micTypes {
    micTypes {
        id
        name
        description
    }
}
'''

UPDATE_MIC_MUTATION = '''
mutation updateMic($mic: MICInput!) {
    updateMic(mic: $mic) {
        mic {
            id
            micType {
                id
                name
            }
            values
            unit
        }
    }
}
'''

UPDATE_MIC_VALUE_MUTATION = '''
mutation updateMicValue($micValue: MICValueInput!) {
    updateMicValue(micValue: $micValue) {
        micValue {
            id
            mic {
                id
                name
                micType {
                    id
                    name
                }
            }
            intValue
            floatValue
            textValue
            unit
        }
    }
}
'''

UPDATE_MIC_TYPE_MUTATION = '''
mutation updateMicType($micType: MICTypeInput!) {
    updateMicType(micType: $micType) {
        micType {
            id
            name
            description
        }
    }
}
'''


class MICUnitTestCase(MPDGraphQLTestCase):

    def setUp(self):
        super().setUp()
        self.mic_type1 = mixer.blend(PropertyType,
                                     name='MIC Bidirectional',
                                     description='Quantitative Bidirectional MIC type')
        self.mic_type2 = mixer.blend(PropertyType,
                                     name='MIC Drop Down',
                                     description='Qualitative Drop Down MIC type')
        self.mic_type3 = mixer.blend(PropertyType,
                                     name='MIC Lower Bound',
                                     description='Quantitative Lower Bound MIC type')
        self.mic1 = mixer.blend(PropertySpecification,
                                name='Bottle Weight',
                                description='Measurement of the weight of an empty bottle',
                                property_type=self.mic_type1,
                                values={'LPL': 4.4, 'LSL': 36.0, 'LCL': 38.0, 'Target': 40.0, 'UCL': 42.0, 'USL': 44.0, 'UPL': 360.0, 'Tolerance': 4.0},
                                unit='g')
        self.mic2 = mixer.blend(PropertySpecification,
                                name='Short Shot',
                                description='Whether the mold was completely filled',
                                property_type=self.mic_type2,
                                values={'Acceptable': ['Acceptable', 'Target', 'Marginal'], 'Unacceptable': ['Unacceptable']})
        self.mic3 = mixer.blend(PropertySpecification,
                                name='Wall Balance 1 (1-36)',
                                description='Difference in wall thickness',
                                property_type=self.mic_type3,
                                values={'Target': 0.0, 'UCL': 0.175, 'USL': 0.35, 'UPL': 3.5, 'Tolerance': 0.35},
                                unit='mm')
        self.mic_value1 = mixer.blend(Property,
                                      property_type=None,
                                      specification=self.mic1,
                                      int_value=None,
                                      float_value=45.2,
                                      text_value=None,
                                      unit='g')
        self.mic_value2 = mixer.blend(Property,
                                      property_type=None,
                                      specification=self.mic2,
                                      int_value=None,
                                      float_value=None,
                                      text_value='Acceptable',
                                      unit=None)
        self.mic_value3 = mixer.blend(Property,
                                      property_type=None,
                                      specification=self.mic3,
                                      int_value=None,
                                      float_value=0.05,
                                      text_value=None,
                                      unit='mm')

    def test_mic_types(self):

        response = self.client.execute(MIC_TYPES_QUERY, {})
        data = response.data
        # print('test_mic_types data', data)

        assert len(data['micTypes']) == 3

    def test_mic_values(self):

        response = self.client.execute(MIC_VALUES_QUERY, {})
        print('test_mic_values response', response)
        data = response.data
        print('test_mic_values data', data)

        assert len(data['micValues']) == 3

    def test_mics(self):

        response = self.client.execute(MICS_QUERY, {})
        # print('test_mics response', response)
        data = response.data
        print('test_mics data', data)

        assert len(data['mics']) == 3

    def test_update_mic(self):

        values = {'Target': 0.1, 'UCL': 0.275, 'USL': 0.45, 'UPL': 4.5, 'Tolerance': 0.45}
        unit = 'cm'
        variables = {
            'mic': {
                'id': self.mic3.id,
                'micType': {
                    'id': self.mic_type2.id,
                },
                'values': json.dumps(values),
                'unit': unit,
            }
        }
        print('variables', variables)
        response = self.client.execute(UPDATE_MIC_MUTATION, variables)
        print('test_update_mic response', response)
        data = response.data
        print('test_update_mic data', data)

        prop = data['updateMic']['mic']
        self.assertEqual(json.loads(prop['values']), values)
        self.assertEqual(prop['unit'], unit)
        self.assertEqual(int(prop['micType']['id']), self.mic_type2.id)

    def test_update_mic_type(self):

        name = 'Updated Name'
        description = 'Updated description'
        variables = {
            'micType': {
                'id': self.mic_type1.id,
                'name': name,
                'description': description,
            }
        }
        response = self.client.execute(UPDATE_MIC_TYPE_MUTATION, variables)
        print('test_update_mic_type response', response)
        data = response.data
        print('test_update_mic_type data', data)

        mic_type = data['updateMicType']['micType']
        self.assertEqual(mic_type['name'], name)
        self.assertEqual(mic_type['description'], description)

    def test_update_mic_value(self):

        int_value = 123
        float_value = 4.56
        text_value = '789'
        unit = 'mm'
        variables = {
            'micValue': {
                'id': self.mic_value1.id,
                'mic': {
                    'id': self.mic2.id,
                },
                'intValue': int_value,
                'floatValue': float_value,
                'textValue': text_value,
                'unit': unit,
            }
        }
        response = self.client.execute(UPDATE_MIC_VALUE_MUTATION, variables)
        print('test_update_mic_value response', response)
        data = response.data
        print('test_update_mic_value data', data)

        prop = data['updateMicValue']['micValue']
        self.assertEqual(prop['intValue'], int_value)
        self.assertEqual(prop['floatValue'], float_value)
        self.assertEqual(prop['textValue'], text_value)
        self.assertEqual(prop['unit'], unit)
        # self.assertEqual(int(prop['micType']['id']), self.mic_type2.id)
        self.assertEqual(int(prop['mic']['id']), self.mic2.id)
