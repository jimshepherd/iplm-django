import graphene
from graphene_django import DjangoObjectType
from typing import List

from ..models import \
    Property as PropertyModel, \
    PropertySpecification as PropertySpecificationModel, \
    PropertyType as PropertyTypeModel

from .base import NamedInput
from .helpers import get_model_by_id_or_name, update_model_from_input
from .property import PropertySpecification, PropertyType


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

    # Hack to allow mic_type to be copied to property_type in update_model_from_input()
    # property_type = mic_type
    specification = mic


# noinspection PyMethodParameters,PyMethodMayBeStatic
class MICQuery(graphene.ObjectType):
    mic_types = graphene.List(MICType)
    mic_values = graphene.List(MICValue)
    mics = graphene.List(MIC)

    def resolve_mic_values(root, info) -> List[PropertyModel]:
        # Add filters for MIC Property Types
        return PropertyModel.objects.all()

    def resolve_mics(root, info) -> List[PropertySpecificationModel]:
        # Add filters for MIC Property Types
        return PropertySpecificationModel.objects.all()

    def resolve_mic_types(root, info) -> List[PropertyTypeModel]:
        # Add filters for MIC Property Types
        return PropertyTypeModel.objects.all()


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
        print('mutating')
        value_model = get_model_by_id_or_name(PropertyModel, mic_value)
        if value_model is None:
            value_model = PropertyModel()

        print('model exists')
        # mic_value.property_type = mic_value.mic_type
        mic_value.specification = mic_value.mic

        update_model_from_input(value_model, mic_value)
        print('Done!')
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


class MICMutation(graphene.ObjectType):
    update_mic = UpdateMIC.Field()
    update_mic_type = UpdateMICType.Field()
    update_mic_value = UpdateMICValue.Field()
