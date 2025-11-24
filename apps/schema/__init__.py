import graphene
from apps.subscription.schema.queries import SubscriptionPlanQuery 

# Combine all query classes
class Query(SubscriptionPlanQuery, graphene.ObjectType):
    pass 


schema = graphene.Schema(query=Query )
