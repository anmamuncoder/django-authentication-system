import graphene
import graphql_jwt
from graphene import relay
from graphql_relay import from_global_id
from .types import TransactionType
from apps.subscription.models import Transaction, SubscriptionPlan
from apps.users.models import User

class AuthMutations(graphene.ObjectType):
    token_auth = graphql_jwt.ObtainJSONWebToken.Field()
    verify_token = graphql_jwt.Verify.Field()
    refresh_token = graphql_jwt.Refresh.Field()
 
# ------------------------------
# Relay Input Types
# ------------------------------
class CreateTransactionInput(graphene.InputObjectType):
    plan_id = graphene.ID(required=True)
    bank_name = graphene.String(required=True)
    account_number = graphene.String(required=True)
    routing_number = graphene.String(required=True)

# ------------------------------
# Create Transaction Mutation
# ------------------------------
class CreateTransactionMutation(graphene.Mutation):
    class Arguments:
        input = CreateTransactionInput(required=True)

    transaction = graphene.Field(TransactionType)

    @classmethod
    def mutate(cls, root, info, input):
        user = info.context.user
        if user.is_anonymous:
            return Exception("Authentication credantical invalid!")
        
        # Use RAW UUID in mutation, Relay Global ID.
        # plan_pk = from_global_id(input.plan_id)[1]
        # plan = SubscriptionPlan.objects.get(pk=plan_pk)

        plan = SubscriptionPlan.objects.get(pk=input.plan_id)

        transaction = Transaction.objects.create(
            user=user, plan=plan,
            amount=plan.price,
            bank_name=input.bank_name,
            account_number=input.account_number,
            routing_number=input.routing_number,
        )
        return CreateTransactionMutation(transaction=transaction)

# ------------------------------
# Root Mutation
# ------------------------------
class TransactionMutation(graphene.ObjectType):
    create_transaction = CreateTransactionMutation.Field()
    # update_transaction_status = UpdateTransactionStatusMutation.Field()
    # delete_transaction = DeleteTransactionMutation.Field()


