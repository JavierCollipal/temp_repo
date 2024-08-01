from django.test import TestCase
from temp_repo.models.transaction import Transaction
from datetime import date

class TransactionModelTestCase(TestCase):
    
    def setUp(self):
        # Set up initial data for the tests, if necessary
        self.transaction_data = {
            'description': 'Test Transaction',
            'amount': 100.50,
            'date': date(2024, 1, 1)
        }

    def test_create_transaction(self):
        # Test creating a transaction
        transaction = Transaction(**self.transaction_data)
        transaction.save()

        # Verify the transaction is saved correctly
        saved_transaction = Transaction.objects.get(id=transaction.id)
        self.assertEqual(saved_transaction.description, self.transaction_data['description'])
        self.assertEqual(saved_transaction.amount, self.transaction_data['amount'])
        self.assertEqual(saved_transaction.date, self.transaction_data['date'])

    def test_retrieve_transaction(self):
        # Create and save a transaction
        transaction = Transaction(**self.transaction_data)
        transaction.save()

        # Retrieve the transaction by ID
        retrieved_transaction = Transaction.objects.get(id=transaction.id)

        # Verify the retrieved transaction
        self.assertIsNotNone(retrieved_transaction)
        self.assertEqual(retrieved_transaction.id, transaction.id)

    def test_transaction_field_validation(self):
        # Test missing required fields
        with self.assertRaises(Exception):
            Transaction().save()

        with self.assertRaises(Exception):
            Transaction(description='No amount', date=date(2024, 1, 1)).save()

        with self.assertRaises(Exception):
            Transaction(description='No date', amount=100.50).save()