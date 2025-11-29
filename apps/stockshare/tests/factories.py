import factory
from apps.stockshare.models import ShareWith
from apps.users.tests.factories import UserFactory
from factory import fuzzy

class ShareWithFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = ShareWith
    owner = factory.SubFactory(UserFactory)
    shared_user = factory.SubFactory(UserFactory)
    