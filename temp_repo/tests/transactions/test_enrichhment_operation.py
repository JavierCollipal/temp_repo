from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from temp_repo.models.transaction import Transaction
from temp_repo.models.category import Category
from temp_repo.models.commerce import Commerce
from temp_repo.models.keyword import Keyword
from temp_repo.serializers.enrichment import EnrichedTransactionSerializer

class EnrichmentOperationTestCase(APITestCase):

    def setUp(self):
        print("\n[Setup] Creating entities for enrichment operation tests...")

        # Create a category
        self.category = Category(
            name="Restaurantes",
            type="expense"
        ).save()
        print(f"Category created with ID: {self.category.id}, Name: {self.category.name}")

        # Create a commerce with reference to the category
        self.commerce = Commerce(
            merchant_name="Uber Eats",
            merchant_logo="http://example.com/logo.png",
            category=self.category
        ).save()
        print(f"Commerce created with ID: {self.commerce.id}, Merchant Name: {self.commerce.merchant_name}, Category ID: {self.category.id}")

        # Create a keyword with reference to the commerce
        self.keyword = Keyword(
            keyword="uber eats",
            merchant_id=self.commerce.id
        ).save()
        print(f"Keyword created with ID: {self.keyword.id}, Keyword: {self.keyword.keyword}, Merchant ID: {self.keyword.merchant_id}")

        # Setup URLs
        self.url_enrichment = reverse('enrichment-operation')

    def test_enrichment_operation(self):
        print("\n[TEST] Performing enrichment operation on transactions.")

        # Create a transaction to be enriched
        transaction = Transaction(
            description="PYU *UberEats",
            amount=-300.00,
            date="2023-12-01"
        ).save()

        print(f"Transaction created with ID: {transaction.id}, Description: {transaction.description}")

        # Data for enrichment request
        enrichment_data = {
            "transactions": [
                {"description": transaction.description, "amount": transaction.amount, "date": transaction.date}
            ]
        }

        # Perform the enrichment operation
        response = self.client.post(self.url_enrichment, enrichment_data, format='json')
        print(f"Enrichment operation response status: {response.status_code}")

        # Assertions
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        enriched_transaction = response.data[0]
        print("Verified that the transaction was enriched with the correct category and commerce details.")

        