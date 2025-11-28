import graphene
from apps.subscription.schema.queries import SubscriptionPlanQuery,UserSubscriptionQuery,TransactionQuery
from apps.subscription.schema.mutations import AuthMutations,TransactionMutation

# Combine all query classes
class Query(SubscriptionPlanQuery,UserSubscriptionQuery, TransactionQuery, graphene.ObjectType):
    pass 

# Combine all mutation classes
class Mutation(AuthMutations,TransactionMutation, graphene.ObjectType):
    pass

schema = graphene.Schema(query=Query,mutation=Mutation)
