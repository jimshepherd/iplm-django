import graphene
from graphene_django import DjangoObjectType
from typing import List

from ..models import \
    Process as ProcessModel, \
    ProcessStep as ProcessStepModel, \
    ProcessMethod as ProcessMethodModel, \
    ProcessMethodStep as ProcessMethodStepModel

from .base import NamedInput
from .helpers import get_model_by_id_or_name, update_model_from_input
from .organization import OrganizationInput
from .property import PropertyInput


# noinspection PyMethodParameters
class ProcessMethod(DjangoObjectType):
    class Meta:
        model = ProcessMethodModel


# noinspection PyMethodParameters
class ProcessMethodStep(DjangoObjectType):
    class Meta:
        model = ProcessMethodStepModel


# noinspection PyMethodParameters
class Process(DjangoObjectType):
    class Meta:
        model = ProcessModel


# noinspection PyMethodParameters
class ProcessStep(DjangoObjectType):
    class Meta:
        model = ProcessStepModel


class ProcessMethodInput(NamedInput):
    description = graphene.String()
    version = graphene.String()
    parent = graphene.InputField(lambda: ProcessMethodInput)


class ProcessMethodStepInput(NamedInput):
    description = graphene.String()
    version = graphene.String()
    method = graphene.InputField(ProcessMethodInput)
    parent = graphene.InputField(lambda: ProcessMethodStepInput)
    order = graphene.Int()
    properties = graphene.List(PropertyInput)


class ProcessInput(NamedInput):
    description = graphene.String()
    method = graphene.InputField(ProcessMethodInput)
    producer = graphene.InputField(OrganizationInput)
    # process_steps
    # materials_in
    # materials_out


class ProcessStepInput(NamedInput):
    description = graphene.String()
    process = graphene.InputField(ProcessInput)
    method_step = graphene.InputField(ProcessMethodStepInput)
    parent = graphene.InputField(lambda: ProcessStepInput)
    order = graphene.Int()
    properties = graphene.List(PropertyInput)


# noinspection PyMethodParameters,PyMethodMayBeStatic
class ProcessQuery(graphene.ObjectType):
    processes = graphene.List(Process)
    process_methods = graphene.List(ProcessMethod)

    def resolve_processes(root, info) -> List[ProcessModel]:
        return ProcessModel.objects.all()

    def resolve_process_methods(root, info) -> List[ProcessMethodModel]:
        return ProcessMethodModel.objects.all()


class UpdateProcess(graphene.Mutation):
    class Arguments:
        process = ProcessInput(required=True)

    process = graphene.Field(Process)

    def mutate(root, info, process=None):
        process_model = get_model_by_id_or_name(ProcessModel, process)
        if process_model is None:
            process_model = ProcessModel()
        update_model_from_input(process_model, process)
        process_model.save()
        return UpdateProcess(process=process_model)


class UpdateProcessMethod(graphene.Mutation):
    class Arguments:
        process_method = ProcessMethodInput(required=True)

    process_method = graphene.Field(ProcessMethod)

    def mutate(root, info, process_method=None):
        method_model = get_model_by_id_or_name(ProcessMethodModel, process_method)
        if method_model is None:
            method_model = ProcessMethodModel()
        update_model_from_input(method_model, process_method)
        method_model.save()
        return UpdateProcessMethod(process_method=method_model)


class ProcessMutation(graphene.ObjectType):
    update_process = UpdateProcess.Field()
    update_process_method = UpdateProcessMethod.Field()
