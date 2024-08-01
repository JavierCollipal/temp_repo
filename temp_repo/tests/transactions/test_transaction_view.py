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
        print("\n[Setup] Cleaning up the database...")
        Transaction.objects.delete()

    def test_create_transaction_with_invalid_data(self):
        print("\n[TEST] Creating a transaction with invalid data.")
        # Test POST request with missing required fields
        invalid_data = {
            'description': '',  # Invalid empty description
            'amount': 'invalid_amount',  # Invalid non-numeric amount
            'date': ''  # Invalid empty date
        }
        response = self.client.post(self.url, invalid_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        print(f"Expected failure with status: {response.status_code}")
        self.assertIn('description', response.data)
        self.assertIn('amount', response.data)
        self.assertIn('date', response.data)
        print("Validation errors returned as expected.")

    def test_create_many_transactions(self):
        print("\n[TEST] Creating 1000 transactions.")
        # Create a list of 1000 transactions for the test
        transaction_data = [
            {
                'id': str(uuid.uuid4()),
                'description': f'Test Transaction {i}',
                'amount': 100.50,
                'date': date(2024, 1, 1).isoformat()
            } for i in range(1000)
        ]

        print("Sending POST request to create 1000 transactions...")
        start_time = time.time()
        response = self.client.post(self.url_create_many, transaction_data, format='json')
        end_time = time.time()

        duration = end_time - start_time
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(len(response.data), 1000)
        self.assertTrue(duration < 8, f"Operation took too long: {duration} seconds")

        print(f"1000 transactions created in {duration:.2f} seconds.")

        # Verify that the 1000 transactions are actually created in the database
        transaction_count = Transaction.objects.count()
        self.assertEqual(transaction_count, 1000)  # 1000 transactions should exist
        print(f"Verified {transaction_count} transactions exist in the database.")

    def test_create_transactions_with_small_batch(self):
        print("\n[TEST] Creating 10 transactions (small batch).")
        # Create a list of 10 transactions for the test
        transaction_data = [
            {
                'id': str(uuid.uuid4()),
                'description': f'Small Batch Transaction {i}',
                'amount': 10.00 * i,
                'date': date(2024, 1, 1).isoformat()
            } for i in range(10)
        ]

        print("Sending POST request to create 10 transactions...")
        response = self.client.post(self.url_create_many, transaction_data, format='json')

        # Check the response status
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        print(f"Response status: {response.status_code}")
        self.assertEqual(len(response.data), 10)
        print(f"Verified 10 transactions created in response.")

        # Verify that the transactions are actually created in the database
        transaction_count = Transaction.objects.count()
        self.assertEqual(transaction_count, 10)  # Only 10 transactions should exist
        print(f"Verified {transaction_count} transactions exist in the database.")

    def test_list_transactions(self):
        print("\n[TEST] Listing all transactions.")
        # Test GET request for listing transactions
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        print(f"Response status: {response.status_code}")
        self.assertIsInstance(response.data, list)
        print(f"Response is a list containing {len(response.data)} items.")

        # Assert that the response length matches the number of transactions in the database
        transaction_count = Transaction.objects.count()
        self.assertEqual(len(response.data), transaction_count)
        print(f"Verified that the number of transactions in response matches the database count: {transaction_count}.")

    def tearDown(self):
        print("\n[TearDown] Cleaning up the database after test.")
        # Clean up the database after all tests
        Transaction.objects.delete()
        print("Database cleaned.")