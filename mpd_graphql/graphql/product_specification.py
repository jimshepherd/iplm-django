from argparse import Namespace
import graphene
from graphene_django import DjangoObjectType
from typing import List

from ..models import \
    MaterialSpecification as MaterialSpecificationModel, \
    Material as MaterialModel, \
    MaterialType as MaterialTypeModel, \
    ProcessMethod as ProcessMethodModel, \
    Process as ProcessModel, \
    ProcessMethodMaterialSpecification as ProcessMethodMaterialSpecificationModel, \
    Property as PropertyModel, \
    PropertySpecification as PropertySpecificationModel, \
    PropertyType as PropertyTypeModel

from .base import NamedInput
from .helpers import get_model_by_id_or_name, update_model_from_input
from .identifier import IdentifierInput
from .process import ProcessInput
from .user import UserInput


# noinspection PyMethodParameters
class ProductType(DjangoObjectType):
    class Meta:
        model = MaterialTypeModel


# noinspection PyMethodParameters
class Product(DjangoObjectType):
    class Meta:
        model = MaterialSpecificationModel


# noinspection PyMethodParameters
class ProducedProduct(DjangoObjectType):
    class Meta:
        model = MaterialModel

    product = graphene.Field(Product)

    def resolve_product(self, info):
        return self.specification


# noinspection PyMethodParameters
class MICType(DjangoObjectType):
    class Meta:
        model = PropertyTypeModel


# noinspection PyMethodParameters
class MIC(DjangoObjectType):
    class Meta:
        model = PropertySpecificationModel

    mic_type = graphene.Field(MICType)

    def resolve_mic_type(self, info):
        return self.property_type


# noinspection PyMethodParameters
class MICValue(DjangoObjectType):
    class Meta:
        model = PropertyModel

    mic = graphene.Field(MIC)

    def resolve_mic(self, info):
        return self.specification


class ProductTypeInput(NamedInput):
    description = graphene.String()


class ProductInput(NamedInput):
    description = graphene.String()
    version = graphene.String()

    process = graphene.Field(ProcessInput)

    # Hack to allow product_type to be copied to material_type in update_model_from_input()
    material_type = graphene.Field(ProductTypeInput)


class ProducedProductInput(NamedInput):
    description = graphene.String()
    product = graphene.Field(ProductInput)
    process = graphene.Field(ProcessInput)

    identifiers = graphene.List(IdentifierInput)

    # Hack to allow product to be copied to material in update_model_from_input()
    specification = product
    material_type = graphene.Field(ProductTypeInput)


class MICTypeInput(NamedInput):
    description = graphene.String()


class MICInput(NamedInput):
    description = graphene.String()
    mic_type = graphene.Field(MICTypeInput)
    values = graphene.JSONString()
    unit = graphene.String()

    # Hack to allow mic_type to be copied to property_type in update_model_from_input()
    property_type = mic_type


class MICValueInput(NamedInput):
    mic = graphene.Field(MICInput)
    # mic_type = graphene.Field(MICTypeInput)
    int_value = graphene.Int()
    float_value = graphene.Float()
    text_value = graphene.String()
    unit = graphene.String()

    # Hack to allow mic to be copied to specification in update_model_from_input()
    # property_type = mic_type
    specification = mic


# noinspection PyMethodParameters
class ProductSpecification(DjangoObjectType):
    class Meta:
        model = ProcessMethodModel

    product = graphene.Field(Product)
    mics = graphene.List(MIC)

    def resolve_product(self, info):
        proc_meth_mat_spec = self.material_specifications_in.first()
        if proc_meth_mat_spec is not None:
            return proc_meth_mat_spec.material_specification
        return None

    def resolve_mics(self, info):
        return self.property_specs.all()


# noinspection PyMethodParameters
class ProductMeasurement(DjangoObjectType):
    class Meta:
        model = ProcessModel

    specification = graphene.Field(ProductSpecification)
    mic_values = graphene.List(MICValue)

    def resolve_specification(self, info):
        return self.method

    def resolve_mic_values(self, info):
        return self.properties.all()


class ProductSpecificationInput(NamedInput):
    description = graphene.String()
    version = graphene.String()
    # parent = graphene.InputField(lambda: ProductSpecificationInput)
    # properties = graphene.List(PropertyInput)
    product = graphene.Field(ProductInput)
    mics = graphene.List(MICInput)

    # Hack to allow mics to be copied to property_specs in update_model_from_input()
    property_specs = mics


class ProductMeasurementInput(NamedInput):
    description = graphene.String()
    specification = graphene.Field(ProductSpecificationInput)
    operator = graphene.Field(UserInput)
    # producer = graphene.Field(OrganizationInput)
    mic_values = graphene.List(MICValueInput)

    # Hack to allow mic_values to be copied to properties in update_model_from_input()
    method = specification
    properties = mic_values


# noinspection PyMethodParameters,PyMethodMayBeStatic
class MICQuery(graphene.ObjectType):
    product_types = graphene.List(ProductType)
    products = graphene.List(Product)
    produced_products = graphene.List(ProducedProduct)
    mic_types = graphene.List(MICType)
    mic_values = graphene.List(MICValue)
    mics = graphene.List(MIC)
    product_specifications = graphene.List(ProductSpecification)
    product_measurements = graphene.List(ProductMeasurement)

    def resolve_product_types(root, info) -> List[MaterialTypeModel]:
        # TODO: Add filters for Product Material Types
        return MaterialTypeModel.objects.all()

    def resolve_products(root, info) -> List[MaterialSpecificationModel]:
        q = MaterialSpecificationModel.objects.filter(material_type__name='Product')
        return q.all()

    def resolve_produced_products(root, info) -> List[MaterialModel]:
        q = MaterialModel.objects.filter(specification__material_type__name='Product')
        return q.all()

    def resolve_mic_values(root, info) -> List[PropertyModel]:
        # TODO: Add filters for MIC Property Types
        return PropertyModel.objects.all()

    def resolve_mics(root, info) -> List[PropertySpecificationModel]:
        # TODO: Add filters for MIC Property Types
        return PropertySpecificationModel.objects.all()

    def resolve_mic_types(root, info) -> List[PropertyTypeModel]:
        # TODO: Add filters for MIC Property Types
        return PropertyTypeModel.objects.all()

    def resolve_product_specifications(root, info) -> List[ProcessMethodModel]:
        q = ProcessMethodModel.objects.filter(process_type__name='Product Specification')
        return q.all()

    def resolve_product_measurements(root, info) -> List[ProcessModel]:
        q = ProcessModel.objects.filter(process_type__name='Product Specification')
        return q.all()


class UpdateProduct(graphene.Mutation):
    class Arguments:
        product = ProductInput(required=True)

    product = graphene.Field(Product)

    def mutate(root, info, product=None):
        product_model = get_model_by_id_or_name(MaterialSpecificationModel, product)
        if product_model is None:
            product_model = MaterialSpecificationModel()
        material_type = get_model_by_id_or_name(MaterialTypeModel,
                                                Namespace(name='Product'))
        product.material_type = Namespace(id=material_type.id)
        update_model_from_input(product_model, product)

        product_model.save()
        return UpdateProduct(product=product_model)


class UpdateProducedProduct(graphene.Mutation):
    class Arguments:
        produced_product = ProducedProductInput(required=True)

    produced_product = graphene.Field(ProducedProduct)

    def mutate(root, info, produced_product=None):
        product_model = get_model_by_id_or_name(MaterialModel, produced_product)
        if product_model is None:
            product_model = MaterialModel()

        produced_product.specification = produced_product.product
        material_type = get_model_by_id_or_name(MaterialTypeModel,
                                                Namespace(name='Product'))
        produced_product.material_type = Namespace(id=material_type.id)
        update_model_from_input(product_model, produced_product)
        product_model.save()
        return UpdateProducedProduct(produced_product=product_model)


class UpdateProductType(graphene.Mutation):
    class Arguments:
        product_type = ProductTypeInput(required=True)

    product_type = graphene.Field(ProductType)

    def mutate(root, info, product_type=None):
        type_model = get_model_by_id_or_name(MaterialTypeModel, product_type)
        if type_model is None:
            type_model = MaterialTypeModel()
        update_model_from_input(type_model, product_type)
        type_model.save()
        return UpdateProductType(product_type=type_model)


class UpdateMIC(graphene.Mutation):
    class Arguments:
        mic = MICInput(required=True)

    mic = graphene.Field(MIC)

    def mutate(root, info, mic=None):
        mic_model = get_model_by_id_or_name(PropertySpecificationModel, mic)
        if mic_model is None:
            mic_model = PropertySpecificationModel()

        mic.property_type = mic.mic_type

        update_model_from_input(mic_model, mic)
        mic_model.save()
        return UpdateMIC(mic=mic_model)


class UpdateMICValue(graphene.Mutation):
    class Arguments:
        mic_value = MICValueInput(required=True)

    mic_value = graphene.Field(MICValue)

    def mutate(root, info, mic_value=None):
        value_model = get_model_by_id_or_name(PropertyModel, mic_value)
        if value_model is None:
            value_model = PropertyModel()

        # mic_value.property_type = mic_value.mic_type
        mic_value.specification = mic_value.mic

        update_model_from_input(value_model, mic_value)
        value_model.save()
        return UpdateMICValue(mic_value=value_model)


class UpdateMICType(graphene.Mutation):
    class Arguments:
        mic_type = MICTypeInput(required=True)

    mic_type = graphene.Field(MICType)

    def mutate(root, info, mic_type=None):

        type_model = get_model_by_id_or_name(PropertyTypeModel, mic_type)
        if type_model is None:
            parent_type = get_model_by_id_or_name(PropertyTypeModel, Namespace(name='MIC'))
            if parent_type is None:
                parent_type = PropertyTypeModel(name='MIC',
                                                description='MIC property type')
                parent_type.save()
            type_model = PropertyTypeModel(parent=parent_type)

        update_model_from_input(type_model, mic_type, exclude_attrs=['parent'])
        type_model.save()
        return UpdateMICType(mic_type=type_model)


class UpdateProductSpecification(graphene.Mutation):
    class Arguments:
        product_specification = ProductSpecificationInput(required=True)

    product_specification = graphene.Field(ProductSpecification)

    def mutate(root, info, product_specification=None):
        product_spec_model = get_model_by_id_or_name(ProcessMethodModel, product_specification)
        if product_spec_model is None:
            product_spec_model = ProcessMethodModel()

        product_specification.property_specs = product_specification.mics

        update_model_from_input(product_spec_model, product_specification, exclude_attrs=['product'])

        product_model = get_model_by_id_or_name(MaterialSpecificationModel, product_specification.product)
        if product_model is not None:
            try:
                prod_spec_prod_model = ProcessMethodMaterialSpecificationModel.objects\
                    .get(process_method=product_spec_model)
            except ProcessMethodMaterialSpecificationModel.DoesNotExist:
                prod_spec_prod_model = None
            if prod_spec_prod_model is None:
                ProcessMethodMaterialSpecificationModel.objects\
                    .create(process_method=product_spec_model,
                            material_specification=product_model)
            else:
                prod_spec_prod_model.material_specification=product_model
                prod_spec_prod_model.save()

        product_spec_model.save()
        return UpdateProductSpecification(product_specification=product_spec_model)


class UpdateProductMeasurement(graphene.Mutation):
    class Arguments:
        product_measurement = ProductMeasurementInput(required=True)

    product_measurement = graphene.Field(ProductMeasurement)

    def mutate(root, info, product_measurement=None):
        measurement_model = get_model_by_id_or_name(ProcessModel, product_measurement)
        if measurement_model is None:
            measurement_model = ProcessModel()

        product_measurement.method = product_measurement.specification
        product_measurement.properties = product_measurement.mic_values

        update_model_from_input(measurement_model, product_measurement)
        measurement_model.save()
        return UpdateProductMeasurement(product_measurement=measurement_model)


class MICMutation(graphene.ObjectType):
    update_product = UpdateProduct.Field()
    update_product_type = UpdateProductType.Field()
    update_produced_product = UpdateProducedProduct.Field()
    update_mic = UpdateMIC.Field()
    update_mic_type = UpdateMICType.Field()
    update_mic_value = UpdateMICValue.Field()
    update_product_specification = UpdateProductSpecification.Field()
    update_product_measurement = UpdateProductMeasurement.Field()
