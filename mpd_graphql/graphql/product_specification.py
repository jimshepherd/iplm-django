
import graphene
from graphene_django import DjangoObjectType
from typing import List

from ..models import \
    ProcessMethod as ProcessMethodModel, \
    Process as ProcessModel, \
    Property as PropertyModel, \
    PropertySpecification as PropertySpecificationModel, \
    PropertyType as PropertyTypeModel

from .base import NamedInput
from .helpers import get_model_by_id_or_name, update_model_from_input
from .property import PropertySpecification, PropertyType
from .user import UserInput


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
    # mic_type = graphene.Field(PropertyType)

    def resolve_mic(self, info):
        return self.specification

    # def resolve_mic_type(self, info):
    #     return self.property_type


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

    mics = graphene.List(MIC)

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
    mic_types = graphene.List(MICType)
    mic_values = graphene.List(MICValue)
    mics = graphene.List(MIC)
    product_specifications = graphene.List(ProductSpecification)
    product_measurements = graphene.List(ProductMeasurement)

    def resolve_mic_values(root, info) -> List[PropertyModel]:
        # Add filters for MIC Property Types
        return PropertyModel.objects.all()

    def resolve_mics(root, info) -> List[PropertySpecificationModel]:
        # Add filters for MIC Property Types
        return PropertySpecificationModel.objects.all()

    def resolve_mic_types(root, info) -> List[PropertyTypeModel]:
        # Add filters for MIC Property Types
        return PropertyTypeModel.objects.all()

    def resolve_product_specifications(root, info) -> List[ProcessMethodModel]:
        # Add filters for Product Specification Process Types
        return ProcessMethodModel.objects.all()

    def resolve_product_measurements(root, info) -> List[ProcessModel]:
        # Add filters for Product Specification Process Types
        return ProcessModel.objects.all()


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
            type_model = PropertyTypeModel()
        update_model_from_input(type_model, mic_type)
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

        update_model_from_input(product_spec_model, product_specification)
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
    update_mic = UpdateMIC.Field()
    update_mic_type = UpdateMICType.Field()
    update_mic_value = UpdateMICValue.Field()
    update_product_specification = UpdateProductSpecification.Field()
    update_product_measurement = UpdateProductMeasurement.Field()
