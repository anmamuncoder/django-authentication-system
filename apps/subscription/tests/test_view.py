import pytest
from django.urls import reverse
from rest_framework.test import APIClient
from rest_framework import status

# Models
from apps.stockshare.models import ShareWith
# Fixture
from apps.users.tests.factories import UserFactory
from apps.stockshare.tests.factories import ShareWithFactory
# Create your tests here.
import json
from rest_framework_simplejwt.tokens import RefreshToken
from .factories import SubscriptionPlanFactory,UserSubscriptionFactory,TransactionFactory

pytestmark = pytest.mark.django_db

# ------------------------------
# Test Fixture
# ------------------------------
 
@pytest.fixture
def client():
    return APIClient()

@pytest.fixture
def user():
    return UserFactory()

@pytest.fixture
def auth_client(client,user):
    user.is_email_verify = True
    user.save()
    client.force_authenticate(user=user)
    return client

@pytest.fixture
def auth_graphql(client,user):
    user.is_email_verify = True
    user.save()

    refresh = RefreshToken.for_user(user)
    access_token = str(refresh.access_token)
    client.credentials(HTTP_AUTHORIZATION=f"JWT {access_token}")
    return client

@pytest.fixture
def url():
    return reverse("graphql_endpoint")

# -------------------------------
# ALl Subscription Plans
# -------------------------------

def test_graphql_subscription_plans_get(client,url):
    query = {
        "query": """
            query {
                subscriptionPlans {
                    id
                    updatedAt
                    type
                    price
                    name
                }
            }
        """
    } 
    response = client.get(url,query)
    assert response.status_code == status.HTTP_200_OK  # GraphQL always returns 200 for resolver errors
    data = response.json()
    assert 'subscriptionPlans' in data["data"]
    assert 'errors' not in data

# -------------------------------
# User Subscription Paid Plans
# -------------------------------
def test_graphql_user_subscription_get_requires_auth(auth_graphql, url):
    query = {
        "query": """
            query {
                userSubscriptions {
                    id
                }
            }
        """
    }
    response = auth_graphql.post(url, data=json.dumps(query), content_type="application/json")
    assert response.status_code == status.HTTP_200_OK  
    data = response.json()
    assert "errors" not in data
    assert "userSubscriptions" in data["data"]  
 
# -------------------------------
# ALl Transaction List
# -------------------------------
def test_graphql_auth_user_transactions_list(auth_graphql,url):
    query = {
        "query": """
            query {
              transaction {
                edges {
                  node {
                    updatedAt
                    success
                    status
                    routingNumber
                    createdAt
                    id
                    bankName
                    amount
                    accountNumber
                  }
                }
              }
            }
        """
    }
    response = auth_graphql.get(url,query)
    assert response.status_code == status.HTTP_200_OK
    data = response.json() 
    assert "errors" not in data 
    assert "transaction" in data["data"] 




def test_create_transaction_mutation(auth_graphql, url, user):
    """
    Test that an authenticated user can create a transaction via GraphQL mutation.
    """ 
    plan = SubscriptionPlanFactory()

    mutation = {
        "query": f"""
            mutation MyMutation {{
            createTransaction(
                input: {{
                planId: "{plan.id}"
                bankName: "Demo Bank"
                accountNumber: "1234567890"
                routingNumber: "987654321"
                }}
                ) {{
                    transaction {{
                    id
                    accountNumber
                    amount
                    bankName
                    routingNumber
                    status
                    success
                    createdAt
                    updatedAt
                    }}
            }}
        }}
        """
    }

    response = auth_graphql.post(url, mutation, format="json")
    assert response.status_code == 200

    data = response.json() 
    assert "errors" not in data

    # Validate the transaction data is returned
    transaction_data = data["data"]["createTransaction"]["transaction"]
    assert transaction_data["accountNumber"] == "1234567890"
    assert transaction_data["bankName"] == "Demo Bank"
    assert transaction_data["routingNumber"] == "987654321"
    assert transaction_data["id"] is not None
    assert transaction_data["createdAt"] is not None
    assert transaction_data["updatedAt"] is not None


# -------------------------------
# Test for Unauthenticated user
# -------------------------------

def test_graphql_user_subscription_get_requires_auth(client, url):
    query = {
        "query": """
            query {
                userSubscriptions {
                    id
                }
            }
        """
    }
    response = client.post(url, data=json.dumps(query), content_type="application/json")
    assert response.status_code == status.HTTP_200_OK  
    data = response.json()
    assert "errors" in data
    assert data["errors"][0]["message"] == "Authentication required"
    assert data["data"]["userSubscriptions"] is None



def test_graphql_unauth_user_transactions_list(client,url):
    """
    Test the trandsaction cant view for un authenticated user
    """
    query = {
        "query": """
            query {
              transaction {
                edges {
                  node {
                    updatedAt
                    success
                    status
                    routingNumber
                    createdAt
                    id
                    bankName
                    amount
                    accountNumber
                  }
                }
              }
            }
        """
    }
    response = client.get(url,query)
    assert response.status_code == status.HTTP_200_OK
    data = response.json() 
    assert data["data"]["transaction"] is None 
    assert data["errors"][0]["message"] == "Authentication required"
