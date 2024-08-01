from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from temp_repo.models.transaction import Transaction
from datetime import date
import time
import uuid

class TransactionListCreateViewTestCase(APITestCase):

    def setUp(self):
        self.url = reverse('transaction-list-create')
        self.url_create_many = reverse('transaction-create-many')
        # Clean up the database before running each test
        Transaction.objects.delete()

    def test_create_transaction_with_invalid_data(self):
        # Test POST request with missing required fields
        invalid_data = {
            'description': '',  # Invalid empty description
            'amount': 'invalid_amount',  # Invalid non-numeric amount
            'date': ''  # Invalid empty date
        }
        response = self.client.post(self.url, invalid_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('description', response.data)
        self.assertIn('amount', response.data)
        self.assertIn('date', response.data)

    def test_create_many_transactions(self):
        # Create a list of 1000 transactions for the test
        transaction_data = [
            {
                'id': str(uuid.uuid4()),
                'description': f'Test Transaction {i}',
                'amount': 100.50,
                'date': date(2024, 1, 1).isoformat()
            } for i in range(1000)
        ]

        start_time = time.time()
        response = self.client.post(self.url_create_many, transaction_data, format='json')
        end_time = time.time()

        duration = end_time - start_time
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(len(response.data), 1000)
        self.assertTrue(duration < 8, f"Operation took too long: {duration} seconds")

        # Verify that the 1000 transactions are actually created in the database
        transaction_count = Transaction.objects.count()
        self.assertEqual(transaction_count, 1000)  # 1000 transactions should exist

        print(f"Total time taken for 1000 transactions: {duration} seconds")

    def test_create_transactions_with_small_batch(self):
        # Create a list of 10 transactions for the test
        transaction_data = [
            {
                'id': str(uuid.uuid4()),
                'description': f'Small Batch Transaction {i}',
                'amount': 10.00 * i,
                'date': date(2024, 1, 1).isoformat()
            } for i in range(10)
        ]

        response = self.client.post(self.url_create_many, transaction_data, format='json')

        # Check the response status
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(len(response.data), 10)

        # Verify that the transactions are actually created in the database
        transaction_count = Transaction.objects.count()
        self.assertEqual(transaction_count, 10)  # Only 10 transactions should exist

    def test_list_transactions(self):
    # Test GET request for listing transactions
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIsInstance(response.data, list)

    # Assert that the response length matches the number of transactions in the database
        transaction_count = Transaction.objects.count()
        self.assertEqual(len(response.data), transaction_count)

    def tearDown(self):
        # Clean up the database after all tests
        Transaction.objects.delete()