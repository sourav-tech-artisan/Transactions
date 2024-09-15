from app.apps.transactions.repositories.transactionrepo import TransactionRepository
from django.db import transaction

class TransactionService:
    """Transaction service
    
    This class contains methods to interact with transactions.
    
    Methods defined here:
    - __update_ancestor_transactions_total_amount(transaction, amount) -> None
    - create_transaction(data) -> transaction
    - update_transaction(transaction, data) -> transaction
    """

    @classmethod
    def __update_ancestor_transactions_total_amount(cls, transaction, amount):
        """Updates the total amount of ancestor transactions.
        
        Args:
            transaction (Transaction): The transaction whose ancestors total amount will be updated.
            amount (Decimal): The amount to be added to the total amount of the ancestor transactions.
        
        Returns:
            None
        """
        # get all the parent transactions
        parent_transactions = []
        parent_transaction = transaction.parent_transaction
        while parent_transaction:
            parent_transaction.total_amount += amount
            parent_transactions.append(parent_transaction)
            parent_transaction = parent_transaction.parent_transaction
        
        # update the parent transactions
        if not parent_transactions:
            return
        TransactionRepository.bulk_update_transactions(parent_transactions, ["total_amount"])

    @classmethod
    @transaction.atomic
    def create_transaction(cls, data):
        """Create a transaction."""
        # create a transaction
        transaction = TransactionRepository.create_transaction(**data)
        # update the total amount of ancestor transactions
        transaction_amount = data.get("amount")
        cls.__update_ancestor_transactions_total_amount(transaction, transaction_amount)
        return transaction
    
    @classmethod
    @transaction.atomic
    def update_transaction(cls, transaction, data):
        """Updates a transaction."""
        current_amount = transaction.amount
        updated_amount = data.get("amount", current_amount) 
        difference_in_amount = updated_amount - current_amount
        # update the transaction
        transaction = TransactionRepository.update_transaction(transaction, **data)
        # update the ancestors total amount
        if difference_in_amount:
            cls.__update_ancestor_transactions_total_amount(transaction, difference_in_amount)
        
        return transaction