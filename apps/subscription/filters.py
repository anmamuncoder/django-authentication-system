import django_filters
from apps.subscription.models import Transaction

class TransactionFilterSet(django_filters.FilterSet):
    class Meta:
        model = Transaction
        fields = "__all__"
