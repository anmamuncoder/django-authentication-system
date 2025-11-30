import factory
from factory import fuzzy
# Data Model
from apps.stockshare.models import ShareWith
# Factory Model
from apps.users.tests.factories import UserFactory

class ShareWithFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = ShareWith
    owner = factory.SubFactory(UserFactory)
    shared_user = factory.SubFactory(UserFactory)
    