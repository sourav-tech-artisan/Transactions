from django.db import models
from app.apps.base.models import TimeStampedUUIDModel

# Models are defined here
class Transaction(TimeStampedUUIDModel):
    """Transaction model."""
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    transaction_type = models.CharField(max_length=50)
    parent_transaction = models.ForeignKey("self", on_delete=models.CASCADE, null=True, blank=True)
    total_amount = models.DecimalField(max_digits=10, decimal_places=2)

    class Meta:
        verbose_name = "Transaction"
        verbose_name_plural = "Transactions"

    def __str__(self):
        return f"{self.id} | {self.transaction_type}"

