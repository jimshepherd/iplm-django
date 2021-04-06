from typing import TYPE_CHECKING, List, Optional, Type, TypeVar

from django.db.models import Model

if TYPE_CHECKING:
    from .base import BaseInput, NamedInput
    ModelType = TypeVar('ModelType', bound=Model)


def get_model_by_id(model_class: Type['ModelType'],
                    graphql_input: 'BaseInput'
                    ) -> Optional['ModelType']:
    """
    Return a model instance given a GraphQL input object containing an id
    attribute

    Args:
        model_class: The model class to search for the model instance
        graphql_input: A GraphQL input object that contains an id attribute

    Returns:
        Model instance that matches the provided input attributes
    """
    if graphql_input is None:
        return None
    model = None
    if 'id' in graphql_input:
        input_id = graphql_input.id
        model = model_class.objects.get(pk=input_id)
    return model


def get_model_by_id_or_name(model_class: 'Type[ModelType]',
                            graphql_input: 'NamedInput'
                            ) -> Optional['ModelType']:
    """
    Return a model instance given a GraphQL input object containing an id or
    name attribute

    Args:
        model_class: The model class to search for the model instance
        graphql_input: A GraphQL input object that contains an id or name attribute

    Returns:
        Model instance that matches the provided input attributes
    """
    if graphql_input is None:
        return None
    model = get_model_by_id(model_class, graphql_input)
    if model is not None:
        return model
    if 'name' in graphql_input:
        name = graphql_input.name
        model = model_class.objects.get(name=name)
    return model


def update_model_from_input(model: 'ModelType',
                            graphql_input: 'BaseInput',
                            save_attr_models: bool = False,
                            save_only_attrs: List[str] = None) -> None:
    """
    Update the provided model instance with values from the GraphQL input

    Args:
        model: A Django Model instance
        graphql_input: A graphene input class instance
        save_attr_models: Boolean whether to save any model instances included as
            attributes to the provided model
        save_only_attrs: A list of names of the attributes that should have their
            model instances updated updated and saved as well

    Returns:
        None
    """
    print('graphql_input', graphql_input)
    print('dict', graphql_input.__dict__)
    print('args', list(graphql_input.keys()))
    for key in graphql_input.keys():
        print('key', key)
        try:
            print('model._meta.get_field', model._meta.get_field(key))
            print('type model._meta.get_field', type(model._meta.get_field(key)))
            model_attr_type = model._meta.get_field(key).remote_field.model
        except AttributeError:
            model_attr_type = model._meta.get_field(key).get_internal_type()
        print('model_attr_type', model_attr_type)
        input_attr = getattr(graphql_input, key)
        print('input attr', input_attr)
        print('type input attr', type(input_attr))
        try:
            ismodel = issubclass(model_attr_type, Model)
        except TypeError:
            ismodel = False
        if ismodel:
            print('isModelInstance')
            if isinstance(input_attr, list):
                print('input_attr is a list')
                attr_models = []
                for input_item in input_attr:
                    attr_model = get_model_by_id_or_name(model_attr_type, input_item)
                    print('attr_model', attr_model)
                    if save_attr_models or (save_only_attrs is not None and key in save_only_attrs):
                        if attr_model is None:
                            attr_model = model_attr_type()
                        update_model_from_input(attr_model, input_item, True)
                        attr_model.save()
                    else:
                        attr_model = get_model_by_id_or_name(model_attr_type, input_item)
                    if attr_model is None:
                        print(f'Error: Could not find model for {input_item} of type {model_attr_type}')
                    else:
                        attr_models.append(attr_model)
                getattr(model, key).set(attr_models, clear=True)
            else:
                if save_attr_models:
                    attr_model = get_model_by_id_or_name(model_attr_type, input_attr)
                    print('attr_model', attr_model)
                    update_model_from_input(attr_model, input_attr, True)
                    attr_model.save()
                    setattr(model, key, attr_model)
                else:
                    if 'id' in input_attr:
                        print('Adding id as foreign_key directly')
                        input_attr_id = input_attr.id
                    else:
                        print('id not included, finding..')
                        attr_model = get_model_by_id_or_name(model_attr_type, input_attr)
                        input_attr_id = attr_model.id
                    setattr(model, key+'_id', input_attr_id)
        else:
            print('isNotModelInstance')
            setattr(model, key, input_attr)

        print('new model attr', getattr(model, key))
