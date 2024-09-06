from django_filters import rest_framework
from app.apps.transactions.repositories.transactionrepo import TransactionRepository


class TransactionFilter(rest_framework.FilterSet):
    """Transaction filter class."""
    class Meta:
        model = TransactionRepository.get_model()
        fields = ("transaction_type",)

