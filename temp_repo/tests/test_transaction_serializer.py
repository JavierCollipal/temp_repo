from django.test import TestCase
from temp_repo.models.transaction import Transaction
from temp_repo.serializers.transaction import TransactionSerializer
from datetime import date
import uuid

class TransactionSerializerTestCase(TestCase):

    def setUp(self):
        self.transaction_data = {
            'description': 'Test Transaction',
            'amount': '100.50',  # Should be a string to mimic JSON input
            'date': date(2024, 1, 1).isoformat()  # ISO format string
        }
        self.transaction = Transaction(
            id=uuid.uuid4(),
            description='Existing Transaction',
            amount=200.75,
            date=date(2024, 2, 2)
        )
        self.transaction.save()

    def test_serialization(self):
        # Serialize a Transaction instance
        serializer = TransactionSerializer(self.transaction)
        data = serializer.data
        self.assertEqual(data['id'], str(self.transaction.id))
        self.assertEqual(data['description'], self.transaction.description)
        self.assertEqual(float(data['amount']), self.transaction.amount)
        self.assertEqual(data['date'], self.transaction.date.isoformat())

    def test_deserialization_and_validation(self):
        # Deserialize and validate data
        serializer = TransactionSerializer(data=self.transaction_data)
        self.assertTrue(serializer.is_valid())
        validated_data = serializer.validated_data
        self.assertEqual(validated_data['description'], self.transaction_data['description'])
        self.assertEqual(validated_data['amount'], 100.50)  # Converted to float
        self.assertEqual(validated_data['date'], date(2024, 1, 1))

    def test_create_transaction(self):
        # Create a new Transaction using the serializer
        serializer = TransactionSerializer(data=self.transaction_data)
        self.assertTrue(serializer.is_valid())
        transaction = serializer.save()
        self.assertIsInstance(transaction, Transaction)
        self.assertEqual(transaction.description, self.transaction_data['description'])
        self.assertEqual(transaction.amount, 100.50)
        self.assertEqual(transaction.date, date(2024, 1, 1))

    def test_update_transaction(self):
        # Update an existing Transaction using the serializer
        updated_data = {
            'description': 'Updated Transaction',
            'amount': '300.25',
            'date': date(2024, 3, 3).isoformat()
        }
        serializer = TransactionSerializer(instance=self.transaction, data=updated_data)
        self.assertTrue(serializer.is_valid())
        updated_transaction = serializer.save()
        self.assertEqual(updated_transaction.description, 'Updated Transaction')
        self.assertEqual(updated_transaction.amount, 300.25)
        self.assertEqual(updated_transaction.date, date(2024, 3, 3))

    def test_invalid_data(self):
        # Test with invalid data
        invalid_data = {
            'description': '',
            'amount': 'invalid',
            'date': 'invalid_date'
        }
        serializer = TransactionSerializer(data=invalid_data)
        self.assertFalse(serializer.is_valid())
        self.assertIn('description', serializer.errors)
        self.assertIn('amount', serializer.errors)
        self.assertIn('date', serializer.errors)
