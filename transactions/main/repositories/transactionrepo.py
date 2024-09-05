from transactions.main.models import Transaction

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

    @staticmethod
    def get_model():
        """Get the model."""
        return Transaction
    
    @staticmethod
    def get_all_queryset():
        """Get all transactions."""
        return Transaction.objects.all()

    @staticmethod
    def create_transaction(**fields):
        """Create a transaction."""
        amount = fields.get("amount")
        transaction_type = fields.get("transaction_type")
        total_amount = fields.get("total_amount")
        parent_transaction = fields.get("parent_transaction")
        transaction = Transaction.objects.create(amount=amount, transaction_type=transaction_type, total_amount=total_amount, parent_transaction=parent_transaction)
        return transaction
    
    @staticmethod
    def update_transaction(transaction, **fields):
        """Updates a transaction."""
        # update the transaction
        for field, value in fields.items():
            setattr(transaction, field, value)
        transaction.save()
        return transaction

    @staticmethod
    def get_transaction_by_id(transaction_id):
        """Get a transaction by id."""
        return Transaction.objects.get(id=transaction_id)
    
    @staticmethod
    def bulk_update_transactions(transactions, fields):
        """Bulk update transactions."""
        Transaction.objects.bulk_update(transactions, fields)
