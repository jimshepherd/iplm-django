import graphene
from graphene_django import DjangoObjectType
from graphql_jwt.decorators import login_required
from typing import List

from ..models import \
    Material as MaterialModel, \
    MaterialSpecification as MaterialSpecificationModel, \
    MaterialType as MaterialTypeModel

from .attribute import AttributeInput
from .base import NamedInput, FixResolutionMixin
from .helpers import filter_by_id_or_name, get_model_by_id_or_name, update_model_from_input
from .identifier import IdentifierInput
from .organization import OrganizationInput
from .process import Process, ProcessInput, ProcessStep
from .property import Property, PropertyInput


# noinspection PyMethodParameters
class MaterialType(FixResolutionMixin, DjangoObjectType):
    class Meta:
        model = MaterialTypeModel


# noinspection PyMethodParameters
class MaterialSpecification(FixResolutionMixin, DjangoObjectType):
    class Meta:
        model = MaterialSpecificationModel


# noinspection PyMethodParameters
class Material(FixResolutionMixin, DjangoObjectType):
    class Meta:
        model = MaterialModel

    # Specifying props that are overridden with different GraphQL types in
    # other GraphQL types that use the same Django model
    process = graphene.Field(Process)
    process_step = graphene.Field(ProcessStep)
    properties = graphene.List(Property)
    specification = graphene.Field(MaterialSpecification)

    def resolve_properties(self, info):
        return self.properties.all()


class MaterialTypeInput(NamedInput):
    description = graphene.String()
    parent = graphene.Field(lambda: MaterialTypeInput)


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
    materials = graphene.List(Material,
                              material_type=graphene.Argument(MaterialTypeInput),
                              include_subtypes=graphene.Argument(graphene.Boolean))
    material_specifications = graphene.List(MaterialSpecification,
                                            parent=graphene.Argument(MaterialSpecificationInput))
    material_types = graphene.List(MaterialType,
                                   ancestor=graphene.Argument(MaterialTypeInput))

    def resolve_materials(root, info, material_type=None, include_subtypes=False) -> List[MaterialModel]:
        q = MaterialModel.objects
        if material_type is not None:
            material_type_model = get_model_by_id_or_name(MaterialTypeModel,
                                                          material_type)
            if material_type_model is None:
                return []
            if include_subtypes:
                material_types = material_type_model.descendants(include_self=True).all()
                q = q.filter(specification__material_type__in=material_types)
            else:
                q = q.filter(specification__material_type=material_type_model)
        return q.all()

    def resolve_material_specifications(root, info, parent=None) -> List[MaterialSpecificationModel]:
        q = MaterialSpecificationModel.objects
        if parent is not None:
            if parent.id is not None:
                q = q.filter(parent__id=parent.id)
        return q.all()

    def resolve_material_types(root, info, ancestor=None) -> List[MaterialTypeModel]:
        if ancestor:
            material_type_model = get_model_by_id_or_name(MaterialTypeModel,
                                                          ancestor)
            if material_type_model is None:
                return []
            return material_type_model.descendants(include_self=True).all()
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
        material_specification = MaterialSpecificationInput(required=True)

    material_specification = graphene.Field(MaterialSpecification)

    def mutate(root, info, material_specification=None):
        spec_model = get_model_by_id_or_name(MaterialSpecificationModel, material_specification)
        if spec_model is None:
            spec_model = MaterialSpecificationModel()
        update_model_from_input(spec_model, material_specification)
        spec_model.save()
        return UpdateMaterialSpecification(material_specification=spec_model)


class MaterialMutation(graphene.ObjectType):
    update_material = UpdateMaterial.Field()
    update_material_specification = UpdateMaterialSpecification.Field()
    update_material_type = UpdateMaterialType.Field()
