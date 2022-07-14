from django.contrib.auth.models import User
import json

from mixer.backend.django import mixer

from mpd_graphql.models import \
    Identifier, IdentifierType, \
    Material, MaterialSpecification, MaterialType, \
    Process, ProcessMethod, ProcessType, \
    Property, PropertySpecification, PropertyType

from .mpd_graphql import MPDGraphQLTestCase


PRODUCTS_QUERY = '''
query products {
    products {
        id
        name
        description
        version
        productType {
            id
            name
        }
    }
}
'''

PRODUCED_PRODUCTS_QUERY = '''
query producedProducts {
    producedProducts {
        id
        name
        description
        product {
            id
            name
            productType {
                id
                name
            }
        }
        process {
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
    }
}
'''

PRODUCT_TYPES_QUERY = '''
query productTypes {
    productTypes {
        id
        name
        description
    }
}
'''


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

PRODUCT_SPECIFICATIONS_QUERY = '''
query productSpecifications {
    productSpecifications {
        id
        name
        description
        version
        mics {
            id
            name
        }
    }
}
'''

PRODUCT_MEASUREMENTS_QUERY = '''
query productMeasurements {
    productMeasurements {
        id
        name
        description
        specification {
            id
            name
        }
        operator {
            id
            name
        }
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
}
'''

UPDATE_PRODUCT_MUTATION = '''
mutation updateProduct($product: ProductInput!) {
    updateProduct(product: $product) {
        product {
            id
            name
            description
            version
            productType {
                id
                name
            }
        }
    }
}
'''

UPDATE_PRODUCED_PRODUCT_MUTATION = '''
mutation updateProducedProduct($producedProduct: ProducedProductInput!) {
    updateProducedProduct(producedProduct: $producedProduct) {
        producedProduct {
            id
            name
            description
            product {
                id
                name
                productType {
                    id
                    name
                }
            }
            process {
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
        }
    }
}
'''

UPDATE_PRODUCT_TYPE_MUTATION = '''
mutation updateProductType($productType: ProductTypeInput!) {
    updateProductType(productType: $productType) {
        productType {
            id
            name
            description
        }
    }
}
'''

UPDATE_MIC_MUTATION = '''
mutation updateMic($mic: MICInput!) {
    updateMic(mic: $mic) {
        mic {
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

UPDATE_PRODUCT_SPECIFICATION_MUTATION = '''
mutation updateProductSpecification($productSpecification: ProductSpecificationInput!) {
    updateProductSpecification(productSpecification: $productSpecification) {
        productSpecification {
            id
            name
            description
            version
            mics {
                id
                name
            }
        }
    }
}
'''

UPDATE_PRODUCT_MEASUREMENT_MUTATION = '''
mutation updateProductMeasurement($productMeasurement: ProductMeasurementInput!) {
    updateProductMeasurement(productMeasurement: $productMeasurement) {
        productMeasurement {
            id
            name
            description
            specification {
                id
                name
            }
            operator {
                id
                name
            }
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
    }
}
'''


class ProductSpecificationUnitTestCase(MPDGraphQLTestCase):

    def setUp(self):
        super().setUp()
        self.user1 = mixer.blend(User)
        self.user2 = mixer.blend(User)
        self.process1 = mixer.blend(Process)
        self.process2 = mixer.blend(Process)
        self.prod_type = mixer.blend(MaterialType,
                                     name='Product',
                                     description='Product type')
        self.prod1 = mixer.blend(MaterialSpecification,
                                 name='20oz Water Bottle',
                                 description='20oz Boston Round with 38mm neck',
                                 version='1.0',
                                 material_type=self.prod_type,
                                 attributes=[],
                                 identifiers=[],
                                 properties=[],
                                 supplier=None)
        self.prod2 = mixer.blend(MaterialSpecification,
                                 name='38mm Closure',
                                 description='38mm twist-off closure',
                                 version='2.0',
                                 material_type=self.prod_type,
                                 attributes=[],
                                 identifiers=[],
                                 properties=[],
                                 supplier=None)
        self.ident_type1 = mixer.blend(IdentifierType,
                                       name='Lot',
                                       description='Lot identifier')
        self.ident_type2 = mixer.blend(IdentifierType,
                                       name='Batch',
                                       description='Batch identifier')
        self.ident1 = mixer.blend(Identifier,
                                  identifier_type=self.ident_type1,
                                  value='123')
        self.ident2 = mixer.blend(Identifier,
                                  identifier_type=self.ident_type2,
                                  value='456')
        self.produced_prod1 = mixer.blend(Material,
                                          description='20oz Water Bottle, Lot 1234',
                                          specification=self.prod1,
                                          process=self.process1,
                                          process_step=None,
                                          attributes=[],
                                          identifiers=[self.ident1],
                                          properties=[])
        self.produced_prod2 = mixer.blend(Material,
                                          description='38mm Closure, Lot 2345',
                                          specification=self.prod2,
                                          process=self.process2,
                                          process_step=None,
                                          attributes=[],
                                          identifiers=[self.ident2],
                                          properties=[])

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
        self.spec_type = mixer.blend(ProcessType,
                                     name='Product Specification',
                                     description='Product specification process type')
        self.prod_spec1 = mixer.blend(ProcessMethod,
                                      name='20oz Bottle Release Criteria',
                                      description='Release criteria for 20oz water bottle',
                                      version='1.0',
                                      parent=None,
                                      process_type=self.spec_type,
                                      properties=[],
                                      property_specs=[self.mic1, self.mic2],
                                      # steps=[],
                                      )
        self.prod_spec2 = mixer.blend(ProcessMethod,
                                      name='38mm Closure Release Criteria',
                                      description='Release criteria for 38mm closure',
                                      version='1.1',
                                      parent=None,
                                      process_type=self.spec_type,
                                      properties=[],
                                      property_specs=[self.mic2, self.mic3],
                                      # steps=[],
                                      )

        self.prod_meas1 = mixer.blend(Process,
                                      name='20oz Bottle Measurements 20220620',
                                      description='Measurements made on bottle batch 20220620',
                                      process_type=self.spec_type,
                                      method=self.prod_spec1,
                                      operator=self.user1,
                                      producer=None,
                                      properties=[self.mic_value1, self.mic_value2],
                                      # materials_in=[],
                                      # materials_out=[],
                                      # process_steps=[],
                                      )
        self.prod_meas2 = mixer.blend(Process,
                                      name='38mm Closure Measurements 20220620',
                                      description='Measurements made on closure batch 20220620',
                                      process_type=self.spec_type,
                                      method=self.prod_spec2,
                                      operator=self.user2,
                                      producer=None,
                                      properties=[self.mic_value2, self.mic_value3])


    def test_product_types(self):

        response = self.client.execute(PRODUCT_TYPES_QUERY, {})
        if response.errors is not None:
            print('test_product_types response', response)
        data = response.data
        # print('test_product_types data', data)

        assert len(data['productTypes']) == 1

    def test_products(self):

        response = self.client.execute(PRODUCTS_QUERY, {})
        if response.errors is not None:
            print('test_products response', response)
        data = response.data
        # print('test_products data', data)

        assert len(data['products']) == 2

    def test_produced_products(self):

        response = self.client.execute(PRODUCED_PRODUCTS_QUERY, {})
        if response.errors is not None:
            print('test_produced_products response', response)
        data = response.data
        # print('test_produced_products data', data)

        assert len(data['producedProducts']) == 2

    def test_mic_types(self):

        response = self.client.execute(MIC_TYPES_QUERY, {})
        if response.errors is not None:
            print('test_mic_types response', response)
        data = response.data
        # print('test_mic_types data', data)

        assert len(data['micTypes']) == 3

    def test_mic_values(self):

        response = self.client.execute(MIC_VALUES_QUERY, {})
        if response.errors is not None:
            print('test_mic_values response', response)
        data = response.data
        # print('test_mic_values data', data)

        assert len(data['micValues']) == 3

    def test_mics(self):

        response = self.client.execute(MICS_QUERY, {})
        if response.errors is not None:
            print('test_mics response', response)
        data = response.data
        # print('test_mics data', data)

        assert len(data['mics']) == 3

    def test_product_specifications(self):

        response = self.client.execute(PRODUCT_SPECIFICATIONS_QUERY, {})
        if response.errors is not None:
            print('test_product_specifications response', response)
        data = response.data
        # print('test_product_specifications data', data)

        assert len(data['productSpecifications']) == 2

    def test_product_measurements(self):

        response = self.client.execute(PRODUCT_MEASUREMENTS_QUERY, {})
        if response.errors is not None:
            print('test_product_measurements response', response)
        data = response.data
        # print('test_product_measurements data', data)

        assert len(data['productMeasurements']) == 2


    def test_update_product(self):

        name = 'New name'
        description = 'New description'
        variables = {
            'product': {
                'id': self.prod1.id,
                'name': name,
                'description': description,
                'productType': {
                    'id': self.prod_type.id,
                },
            }
        }
        response = self.client.execute(UPDATE_PRODUCT_MUTATION, variables)
        if response.errors is not None:
            print('variables', variables)
            print('test_update_product response', response)
        data = response.data
        # print('test_update_product data', data)

        prod = data['updateProduct']['product']
        self.assertEqual(prod['name'], name)
        self.assertEqual(prod['description'], description)
        self.assertEqual(int(prod['productType']['id']), self.prod_type.id)

    def test_update_product_type(self):

        name = 'Updated Name'
        description = 'Updated description'
        variables = {
            'productType': {
                'id': self.prod_type.id,
                'name': name,
                'description': description,
            }
        }
        response = self.client.execute(UPDATE_PRODUCT_TYPE_MUTATION, variables)
        if response.errors is not None:
            print('test_update_product_type response', response)
        data = response.data
        # print('test_update_product_type data', data)

        product_type = data['updateProductType']['productType']
        self.assertEqual(product_type['name'], name)
        self.assertEqual(product_type['description'], description)

    def test_update_produced_product(self):

        name = 'Updated Name'
        description = 'Updated description'
        variables = {
            'producedProduct': {
                'id': self.produced_prod1.id,
                'name': name,
                'description': description,
                'product': {
                    'id': self.prod2.id,
                },
                'process': {
                    'id': self.process2.id,
                },
                'identifiers': [{
                    'id': self.ident2.id,
                }],
            }
        }
        response = self.client.execute(UPDATE_PRODUCED_PRODUCT_MUTATION, variables)
        if response.errors is not None:
            print('test_update_produced_product response', response)
        data = response.data
        # print('test_update_produced_product data', data)

        prod = data['updateProducedProduct']['producedProduct']
        self.assertEqual(prod['name'], name)
        self.assertEqual(prod['description'], description)
        self.assertEqual(int(prod['product']['id']), self.prod2.id)
        self.assertEqual(int(prod['process']['id']), self.process2.id)
        ident1 = prod['identifiers'][0]
        self.assertEqual(int(ident1['id']), self.ident2.id)

    def test_update_mic(self):

        name = 'New name'
        description = 'New description'
        values = {'Target': 0.1, 'UCL': 0.275, 'USL': 0.45, 'UPL': 4.5, 'Tolerance': 0.45}
        unit = 'cm'
        variables = {
            'mic': {
                'name': name,
                'description': description,
                'id': self.mic3.id,
                'micType': {
                    'id': self.mic_type2.id,
                },
                'values': json.dumps(values),
                'unit': unit,
            }
        }
        response = self.client.execute(UPDATE_MIC_MUTATION, variables)
        if response.errors is not None:
            print('variables', variables)
            print('test_update_mic response', response)
        data = response.data
        # print('test_update_mic data', data)

        prop = data['updateMic']['mic']
        self.assertEqual(prop['name'], name)
        self.assertEqual(prop['description'], description)
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
        if response.errors is not None:
            print('test_update_mic_type response', response)
        data = response.data
        # print('test_update_mic_type data', data)

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
        if response.errors is not None:
            print('test_update_mic_value response', response)
        data = response.data
        # print('test_update_mic_value data', data)

        prop = data['updateMicValue']['micValue']
        self.assertEqual(prop['intValue'], int_value)
        self.assertEqual(prop['floatValue'], float_value)
        self.assertEqual(prop['textValue'], text_value)
        self.assertEqual(prop['unit'], unit)
        # self.assertEqual(int(prop['micType']['id']), self.mic_type2.id)
        self.assertEqual(int(prop['mic']['id']), self.mic2.id)

    def test_update_product_specification(self):

        name = 'New name'
        description = 'New description'
        version = 'New version'
        variables = {
            'productSpecification': {
                'id': self.prod_spec1.id,
                'name': name,
                'description': description,
                'version': version,
                'mics': [{
                    'id': self.mic2.id,
                },{
                    'id': self.mic3.id,
                }],
                'propertySpecs': [],
            }
        }
        response = self.client.execute(UPDATE_PRODUCT_SPECIFICATION_MUTATION, variables)
        if response.errors is not None:
            print('test_update_product_specification response', response)
        data = response.data
        # print('test_update_product_specification data', data)

        prop = data['updateProductSpecification']['productSpecification']
        self.assertEqual(prop['name'], name)
        self.assertEqual(prop['description'], description)
        self.assertEqual(prop['version'], version)
        mic1 = prop['mics'][0]
        mic2 = prop['mics'][1]
        self.assertEqual(int(mic1['id']), self.mic2.id)
        self.assertEqual(int(mic2['id']), self.mic3.id)

    def test_update_product_measurement(self):

        name = 'New name'
        description = 'New description'
        specification = self.prod_spec2
        operator = self.user2
        variables = {
            'productMeasurement': {
                'id': self.prod_meas1.id,
                'name': name,
                'description': description,
                'specification': {
                    'id': specification.id,
                },
                'operator': {
                    'id': operator.id,
                },
                'micValues': [{
                    'id': self.mic_value2.id,
                },{
                    'id': self.mic_value3.id,
                }],
                # 'properties': [], # hack to add properties to input def
            }
        }
        response = self.client.execute(UPDATE_PRODUCT_MEASUREMENT_MUTATION, variables)
        if response.errors is not None:
            print('test_update_product_measurement response', response)
        data = response.data
        # print('test_update_product_measurement data', data)

        prop = data['updateProductMeasurement']['productMeasurement']
        self.assertEqual(prop['name'], name)
        self.assertEqual(prop['description'], description)
        self.assertEqual(int(prop['specification']['id']), self.prod_spec2.id)
        self.assertEqual(int(prop['operator']['id']), operator.id)
        mic_value1 = prop['micValues'][0]
        mic_value2 = prop['micValues'][1]
        self.assertEqual(int(mic_value1['id']), self.mic_value2.id)
        self.assertEqual(int(mic_value2['id']), self.mic_value3.id)
