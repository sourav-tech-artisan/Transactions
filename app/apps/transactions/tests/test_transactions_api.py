import uuid
import copy
from decimal import Decimal
from rest_framework import status
from rest_framework.test import APITestCase
from app.apps.transactions.repositories.transactionrepo import TransactionRepository
from endpoints import CREATE_TRANSACTION_URL, LIST_TRANSACTION_URL, RETRIEVE_TRANSACTION_URL, UPDATE_TRANSACTION_URL
from fixtures.invalid_creation_data import INVALID_CREATION_DATA
from fixtures.valid_creation_data import VALID_CREATION_DATA
from fixtures.valid_updation_data import VALID_UPDATION_DATA
from fixtures.invalid_updation_data import INVALID_UPDATION_DATA

class TransactionAPITestCase(APITestCase):
    def setUp(self):
        # Create two test transaction
        fields = {
            'amount': Decimal(100.00),
            'total_amount': Decimal(100.00),
            'transaction_type': 'Test transaction'
        }
        self.test_transaction = TransactionRepository.create_transaction(**fields)
       
    def test_create_transaction_with_valid_data(self):
        """Tetsts creating a transaction without a parent transaction."""
        data = copy.deepcopy(VALID_CREATION_DATA[0])
        data["parent_transaction"] = str(self.test_transaction.id)
        VALID_CREATION_DATA.append(data)
        url = CREATE_TRANSACTION_URL
        count = 1
        ids = [str(self.test_transaction.id)]
        for data in VALID_CREATION_DATA:
            response = self.client.post(url, data, format='json')
            self.assertEqual(response.status_code, status.HTTP_201_CREATED)
            count += 1
            self.assertEqual(TransactionRepository.get_all_queryset().count(), count)
            new_transaction = TransactionRepository.get_all_queryset().exclude(id__in=ids).first()
            self.assertEqual(new_transaction.amount, Decimal(data.get('amount')))
            self.assertEqual(new_transaction.transaction_type, data.get('transaction_type'))
            if data.get('parent_transaction'):
                self.assertEqual(str(new_transaction.parent_transaction.id), data.get('parent_transaction'))
                current_total_amount_of_parent = self.test_transaction.total_amount
                self.test_transaction.refresh_from_db()
                self.assertEqual(self.test_transaction.total_amount, current_total_amount_of_parent + new_transaction.amount)
            ids.append(str(new_transaction.id))

    def test_create_transaction_with_invalid_data(self):
        """Tests creating a transaction with an invalid parent transaction."""
        url = CREATE_TRANSACTION_URL
        for data in INVALID_CREATION_DATA:
            response = self.client.post(url, data, format='json')
            self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
            self.assertEqual(TransactionRepository.get_all_queryset().count(), 1)

    def test_update_transaction_with_valid_data(self):
        """Tests updating a transaction."""
        url = UPDATE_TRANSACTION_URL.format(transaction_id=str(self.test_transaction.id))
        for data in VALID_UPDATION_DATA:
            response = self.client.patch(url, data, format='json')
            self.assertEqual(response.status_code, status.HTTP_200_OK)
            self.test_transaction.refresh_from_db()
            for key, value in data.items():
                self.assertEqual(getattr(self.test_transaction, key), value)

    def test_amount_update_in_transaction(self):
        # first create a transaction with self.test_transaction as parent
        data = copy.deepcopy(VALID_CREATION_DATA[0])
        data["parent_transaction"] = str(self.test_transaction.id)
        url = CREATE_TRANSACTION_URL
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        # fetch the new transaction
        new_transaction = TransactionRepository.get_all_queryset().exclude(id=self.test_transaction.id).first()
        url = UPDATE_TRANSACTION_URL.format(transaction_id=str(new_transaction.id))
        data = {"amount": 300}
        new_transaction_total_amount = new_transaction.total_amount
        difference_in_amount = data.get("amount") - new_transaction.amount
        # update the amount of the new transaction
        response = self.client.patch(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        new_transaction.refresh_from_db()
        # check if amount and total amount of the new transaction is updated
        self.assertEqual(new_transaction.amount, Decimal(data.get('amount')))
        self.assertEqual(new_transaction.total_amount, new_transaction_total_amount + difference_in_amount)
        # check if the total amount of the parent transaction is updated
        current_total_amount_of_parent = self.test_transaction.total_amount
        self.test_transaction.refresh_from_db()
        self.assertEqual(self.test_transaction.total_amount, current_total_amount_of_parent + new_transaction.amount)

    def test_update_transaction_with_invalid_data(self):
        """Tests updating a transaction with invalid data."""
        for data in INVALID_UPDATION_DATA:
            url = UPDATE_TRANSACTION_URL.format(transaction_id=str(self.test_transaction.id))
            response = self.client.patch(url, data, format='json')
            self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
            self.test_transaction.refresh_from_db()
            for key, value in data.items():
                self.assertNotEqual(getattr(self.test_transaction, key), value)

    def test_retrieve_transaction(self):
        transaction_id = str(self.test_transaction.id)
        url = RETRIEVE_TRANSACTION_URL.format(transaction_id=transaction_id)
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data.get("id"), transaction_id)
        self.assertEqual(Decimal(response.data['amount']), self.test_transaction.amount)
        self.assertIn('total_amount', response.data) # transaction sum is stored as total_amount

    def test_retrieve_non_existent_transaction(self):
        transaction_id = uuid.uuid4()
        url = RETRIEVE_TRANSACTION_URL.format(transaction_id=transaction_id)
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_list_transactions_without_pagination(self):
        url = LIST_TRANSACTION_URL + '?page_size=0'
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIsInstance(response.data, list)
        self.assertEqual(len(response.data), 1)  
    
    def test_list_transactions_with_pagination(self):
        url = LIST_TRANSACTION_URL
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIsInstance(response.data, dict)
        self.assertIn('results', response.data)
        self.assertEqual(len(response.data.get('results')), 1)
    
    def test_list_transactions_with_type_filter(self):
        url = LIST_TRANSACTION_URL + '?transaction_type=Test transaction'
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIsInstance(response.data, dict)
        self.assertIn('results', response.data)
        self.assertEqual(len(response.data.get('results')), 1)

    def test_list_transactions_with_invalid_filter_key(self):
        url = LIST_TRANSACTION_URL + '?invalid_filter=Test transaction'
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_list_transaction_with_invalid_filter_value(self):
        url = LIST_TRANSACTION_URL + '?transaction_type=Invalid transaction'
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIsInstance(response.data, dict)
        self.assertIn('results', response.data)
        self.assertEqual(len(response.data.get('results')), 0)