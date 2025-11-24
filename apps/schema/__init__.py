import graphene
from apps.subscription.schema.queries import SubscriptionPlanQuery 
from apps.subscription.schema.mutations import AuthMutations

# Combine all query classes
class Query(SubscriptionPlanQuery, graphene.ObjectType):
    pass 

# Combine all mutation classes
class Mutation(AuthMutations, graphene.ObjectType):
    pass

schema = graphene.Schema(query=Query,mutation=Mutation)
