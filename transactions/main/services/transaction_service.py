from transactions.main.repositories.transactionrepo import TransactionRepository
from django.db import transaction

class TransactionService:
    """Transaction service
    
    This class contains methods to interact with transactions.
    
    Methods defined here:
    - __update_ancestor_transactions_total_amount(transaction, amount) -> None
    - create_transaction(data) -> transaction
    - update_transaction(transaction, data) -> transaction
    """

    @staticmethod
    def __update_ancestor_transactions_total_amount(transaction, amount):
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

    @staticmethod
    @transaction.atomic
    def create_transaction(data):
        """Create a transaction."""
        # create a transaction
        transaction = TransactionRepository.create_transaction(**data)
        # update the total amount of ancestor transactions
        transaction_amount = data.get("amount")
        TransactionService.__update_ancestor_transactions_total_amount(transaction, transaction_amount)
        return transaction
    
    @staticmethod
    @transaction.atomic
    def update_transaction(transaction, data):
        """Updates a transaction."""
        current_amount = transaction.amount
        updated_amount = data.get("amount", current_amount) 
        difference_in_amount = updated_amount - current_amount
        # if the parent transaction is being updated
        if "parent_transaction" in data:
            # update the existing ancestors total amount
            TransactionService.__update_ancestor_transactions_total_amount(transaction, -current_amount)
            # update current transaction
            transaction = TransactionRepository.update_transaction(transaction, **data)
            # refresh objects from the database
            transaction.refresh_from_db()
            # update the new ancestors total amount
            TransactionService.__update_ancestor_transactions_total_amount(transaction, transaction.amount)
            return transaction
        
        # update the transaction
        transaction = TransactionRepository.update_transaction(transaction, **data)
        # update the ancestors total amount
        if difference_in_amount:
            TransactionService.__update_ancestor_transactions_total_amount(transaction, difference_in_amount)
        
        return transaction