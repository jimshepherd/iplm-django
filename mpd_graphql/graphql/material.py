import graphene
from graphene_django import DjangoObjectType
from graphql_jwt.decorators import login_required
from typing import List

from ..models import \
    Material as MaterialModel, \
    MaterialSpecification as MaterialSpecificationModel, \
    MaterialType as MaterialTypeModel

from .attribute import AttributeInput
from .base import NamedInput
from .helpers import get_model_by_id_or_name, update_model_from_input
from .identifier import IdentifierInput
from .organization import OrganizationInput
from .process import ProcessInput
from .property import PropertyInput


# noinspection PyMethodParameters
class MaterialType(DjangoObjectType):
    class Meta:
        model = MaterialTypeModel


# noinspection PyMethodParameters
class MaterialSpecification(DjangoObjectType):
    class Meta:
        model = MaterialSpecificationModel


# noinspection PyMethodParameters
class Material(DjangoObjectType):
    class Meta:
        model = MaterialModel


class MaterialTypeInput(NamedInput):
    description = graphene.String()


class MaterialSpecificationInput(NamedInput):
    description = graphene.String()
    version = graphene.String()
    parent = graphene.Field(lambda: MaterialSpecificationInput)
    material_type = graphene.Field(MaterialTypeInput)
    attributes = graphene.List(AttributeInput)
    identifiers = graphene.List(IdentifierInput)
    properties = graphene.List(PropertyInput)
    supplier = graphene.Field(OrganizationInput)


class MaterialInput(NamedInput):
    description = graphene.String()
    specification = graphene.Field(MaterialSpecificationInput)
    process = graphene.Field(ProcessInput)
    process_step = graphene.Field(ProcessInput)
    attributes = graphene.List(AttributeInput)
    identifiers = graphene.List(IdentifierInput)
    properties = graphene.List(PropertyInput)
    producer = graphene.InputField(OrganizationInput)


# noinspection PyMethodParameters,PyMethodMayBeStatic
class MaterialQuery(graphene.ObjectType):
    materials = graphene.List(Material)
    material_specs = graphene.List(MaterialSpecification)
    material_types = graphene.List(MaterialType)

    def resolve_materials(root, info) -> List[MaterialModel]:
        return MaterialModel.objects.all()

    def resolve_material_specs(root, info) -> List[MaterialSpecificationModel]:
        return MaterialSpecificationModel.objects.all()

    def resolve_material_types(root, info) -> List[MaterialTypeModel]:
        return MaterialTypeModel.objects.all()


class UpdateMaterialType(graphene.Mutation):
    class Arguments:
        material_type = MaterialTypeInput(required=True)

    material_type = graphene.Field(MaterialType)

    @login_required
    def mutate(root, info, material_type=None):
        type_model = get_model_by_id_or_name(MaterialTypeModel, material_type)
        if type_model is None:
            type_model = MaterialTypeModel()
        update_model_from_input(type_model, material_type)
        type_model.save()
        return UpdateMaterialType(material_type=type_model)


class UpdateMaterial(graphene.Mutation):
    class Arguments:
        material = MaterialInput(required=True)

    material = graphene.Field(Material)

    def mutate(root, info, material=None):
        mat_model = get_model_by_id_or_name(MaterialModel, material)
        if mat_model is None:
            mat_model = MaterialModel()
        update_model_from_input(mat_model, material)
        mat_model.save()
        return UpdateMaterial(material=mat_model)


class UpdateMaterialSpecification(graphene.Mutation):
    class Arguments:
        material_spec = MaterialSpecificationInput(required=True)

    material_spec = graphene.Field(MaterialSpecification)

    def mutate(root, info, material_spec=None):
        spec_model = get_model_by_id_or_name(MaterialSpecificationModel, material_spec)
        if spec_model is None:
            spec_model = MaterialSpecificationModel()
        update_model_from_input(spec_model, material_spec)
        spec_model.save()
        return UpdateMaterialSpecification(material_spec=spec_model)


class MaterialMutation(graphene.ObjectType):
    update_material = UpdateMaterial.Field()
    update_material_spec = UpdateMaterialSpecification.Field()
    update_material_type = UpdateMaterialType.Field()
