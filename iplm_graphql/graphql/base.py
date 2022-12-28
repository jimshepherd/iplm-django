import graphene


class BaseInput(graphene.InputObjectType):
    id = graphene.ID()


class NamedInput(BaseInput):
    name = graphene.String()


# Mixin to fix multiple GraphQL types using the same Django model all defaulting
# to a single GraphQL type in the schema
# https://github.com/graphql-python/graphene-django/issues/1291
class FixResolutionMixin:
    @classmethod
    def get_node(cls, info, pk):
        instance = super(FixResolutionMixin, cls).get_node(info, pk)
        setattr(instance, 'graphql_type', cls.__name__)
        return instance

    @classmethod
    def is_type_of(cls, root, info):
        if hasattr(root, 'graphql_type'):
            return getattr(root, 'graphql_type') == cls.__name__
        return super(FixResolutionMixin, cls).is_type_of(root, info)
