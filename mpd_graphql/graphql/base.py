import graphene


class BaseInput(graphene.InputObjectType):
    id = graphene.ID()


class NamedInput(BaseInput):
    name = graphene.String()

