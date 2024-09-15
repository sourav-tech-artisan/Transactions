from app.apps.transactions.models import Transaction

class TransactionRepository:
    """Transaction repository
    
    This class contains methods for interacting with database for transactions.
    
    Methods defined here:
    - get_model() -> Transaction
    - get_all_queryset() -> QuerySet
    - create_transaction(**fields) -> Transaction
    - update_transaction(transaction, **fields) -> Transaction
    - get_transaction_by_id(transaction_id) -> Transaction
    - bulk_update_transactions(transactions, fields) -> None
    """

    @classmethod
    def get_model(cls):
        """Get the model."""
        return Transaction
    
    @classmethod
    def get_all_queryset(cls):
        """Get all transactions."""
        return Transaction.objects.all()

    @classmethod
    def create_transaction(cls, **fields):
        """Create a transaction."""
        amount = fields.get("amount")
        transaction_type = fields.get("transaction_type")
        total_amount = fields.get("total_amount")
        parent_transaction = fields.get("parent_transaction")
        transaction = Transaction.objects.create(amount=amount, transaction_type=transaction_type, total_amount=total_amount, parent_transaction=parent_transaction)
        return transaction
    
    @classmethod
    def update_transaction(cls, transaction, **fields):
        """Updates a transaction."""
        # update the transaction
        for field, value in fields.items():
            setattr(transaction, field, value)
        transaction.save()
        return transaction

    @classmethod
    def get_transaction_by_id(cls, transaction_id):
        """Get a transaction by id."""
        return Transaction.objects.get(id=transaction_id)
    
    @classmethod
    def bulk_update_transactions(cls, transactions, fields):
        """Bulk update transactions."""
        Transaction.objects.bulk_update(transactions, fields)
