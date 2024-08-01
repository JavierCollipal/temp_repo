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
        # Create several transactions in the test database
        self.transaction1 = Transaction(description="PYU *UberEats", amount=-300.00, date=date(2023, 12, 1))
        self.transaction1.save()
        self.transaction2 = Transaction(description="Test Transaction", amount=100.50, date=date(2024, 1, 1))
        self.transaction2.save()
        self.transaction3 = Transaction(description="Existing Transaction", amount=200.75, date=date(2024, 2, 2))
        self.transaction3.save()

    def test_list_transactions(self):
        # Test GET request for listing transactions
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIsInstance(response.data, list)

        self.assertTrue(len(response.data) > 0, "The response data should not be empty")
        
        # Check that all created transactions are in the response
        expected_descriptions = {"PYU *UberEats", "Test Transaction", "Existing Transaction"}
        response_descriptions = {transaction['description'] for transaction in response.data}
        self.assertTrue(expected_descriptions.issubset(response_descriptions))

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

        # Verify that the transactions are actually created in the database
        transaction_count = Transaction.objects.count()
        self.assertEqual(transaction_count, 1003)  # Including the 3 transactions from setUp