from django_filters import rest_framework
from transactions.main.repositories.transactionrepo import TransactionRepository


class TransactionFilter(rest_framework.FilterSet):
    class Meta:
        model = TransactionRepository.get_model()
        fields = ("transaction_type",)

