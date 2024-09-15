from django.contrib import admin
from app.apps.transactions.models import Transaction
from django.contrib import admin

# Register your models here.

class BaseModelAdmin(admin.ModelAdmin):
    """Base model admin class to be inherited by other model admin classes."""

    readonly_fields = ("id", "created_at", "modified_at")

@admin.register(Transaction)
class TransactionAdmin(BaseModelAdmin):
    """Transaction admin class."""
    list_display = ("id", "amount", "transaction_type", "total_amount")
    search_fields = ("id", "amount", "transaction_type")
    