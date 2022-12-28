import graphene
from graphene_django import DjangoObjectType
from typing import List

from ..models import \
    Equipment as EquipmentModel, \
    EquipmentType as EquipmentTypeModel

from .attribute import AttributeInput
from .base import NamedInput
from .helpers import get_model_by_id_or_name, update_model_from_input
from .identifier import IdentifierInput
from .organization import OrganizationInput
from .property import PropertyInput


# noinspection PyMethodParameters
class EquipmentType(DjangoObjectType):
    class Meta:
        model = EquipmentTypeModel


# noinspection PyMethodParameters
class Equipment(DjangoObjectType):
    class Meta:
        model = EquipmentModel


class EquipmentTypeInput(NamedInput):
    description = graphene.String()


class EquipmentInput(NamedInput):
    description = graphene.String()
    equipment_type = graphene.InputField(EquipmentTypeInput)
    organization = graphene.InputField(OrganizationInput)
    attributes = graphene.List(AttributeInput)
    identifiers = graphene.List(IdentifierInput)
    properties = graphene.List(PropertyInput)


# noinspection PyMethodParameters,PyMethodMayBeStatic
class EquipmentQuery(graphene.ObjectType):
    equipment = graphene.List(Equipment)
    equipment_types = graphene.List(EquipmentType)

    def resolve_equipment(root, info) -> List[EquipmentModel]:
        return EquipmentModel.objects.all()

    def resolve_equipment_types(root, info) -> List[EquipmentTypeModel]:
        return EquipmentTypeModel.objects.all()


class UpdateEquipment(graphene.Mutation):
    class Arguments:
        equipment = EquipmentInput(required=True)

    equipment = graphene.Field(Equipment)

    def mutate(root, info, equipment=None):
        equipment_model = get_model_by_id_or_name(EquipmentModel, equipment)
        if equipment_model is None:
            equipment_model = EquipmentModel()
        update_model_from_input(equipment_model, equipment)
        equipment_model.save()
        return UpdateEquipment(equipment=equipment_model)


class UpdateEquipmentType(graphene.Mutation):
    class Arguments:
        equipment_type = EquipmentTypeInput(required=True)

    equipment_type = graphene.Field(EquipmentType)

    def mutate(root, info, equipment_type=None):
        type_model = get_model_by_id_or_name(EquipmentTypeModel, equipment_type)
        if type_model is None:
            type_model = EquipmentTypeModel()
        update_model_from_input(type_model, equipment_type)
        type_model.save()
        return UpdateEquipmentType(equipment_type=type_model)


class EquipmentMutation(graphene.ObjectType):
    update_equipment = UpdateEquipment.Field()
    update_equipment_type = UpdateEquipmentType.Field()
