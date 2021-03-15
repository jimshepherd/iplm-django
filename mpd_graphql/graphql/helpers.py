from typing import TYPE_CHECKING, Optional, Type


if TYPE_CHECKING:
    from django.db.models import Model
    from .base import BaseInput, NamedInput


def get_model_by_id(model_class: 'Type[Model]',
                    graphql_input: 'BaseInput'
                    ) -> Optional['Model']:
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


def get_model_by_id_or_name(model_class: 'Type[Model]',
                            graphql_input: 'NamedInput'
                            ) -> Optional['Model']:
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
