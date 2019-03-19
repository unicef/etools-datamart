from graphene_django import DjangoObjectType
import graphene

from etools_datamart.apps.data.models import PMPIndicators


class PMPIndicatorsSchema(DjangoObjectType):
    class Meta:
        model = PMPIndicators


class Query(graphene.ObjectType):
    pmp = graphene.List(PMPIndicatorsSchema)

    def resolve_pmp(self, info):
        return PMPIndicators.objects.all()


schema = graphene.Schema(query=Query)
