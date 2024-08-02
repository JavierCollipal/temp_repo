from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from temp_repo.models.keyword import Keyword
from temp_repo.models.commerce import Commerce
from temp_repo.models.category import Category
import uuid

class KeywordTestCase(APITestCase):

    def setUp(self):
        print("\n[Setup] Creating commerce and category for keyword tests...")
        # Create Category
        self.category = Category(
            external_id=uuid.uuid4(),
            name="Food",
            type="expense"
        ).save()
        
        # Create Commerce
        self.commerce = Commerce(
            external_id=uuid.uuid4(),
            merchant_name="Uber Eats",
            merchant_logo="http://example.com/logo.png",
            category=self.category
        ).save()

        print(f"Commerce created with ID: {self.commerce.id}, Category ID: {self.category.id}")
        self.url_list_create = reverse('keyword-list-create')
        self.url_detail = lambda pk: reverse('keyword-detail', kwargs={'keyword_id': pk})

    def test_create_keyword(self):
        print("\n[TEST] Creating a new keyword.")
        data = {
            'keyword': 'uber eats',
            'merchant_id': str(self.commerce.id)  # Use commerce.id for the reference
        }
        print(f"Sending POST request with data: {data}")
        response = self.client.post(self.url_list_create, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        print(f"Response status: {response.status_code}")

    def test_get_all_keywords(self):
        print("\n[TEST] Retrieving all keywords.")
        Keyword(
            external_id=uuid.uuid4(),
            keyword="uber",
            merchant_id=self.commerce
        ).save()
        
        Keyword(
            external_id=uuid.uuid4(),
            keyword="food delivery",
            merchant_id=self.commerce
        ).save()
        print("2 keywords created.")
        response = self.client.get(self.url_list_create)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertGreaterEqual(len(response.data), 2)

    def test_get_keyword(self):
        print("\n[TEST] Retrieving a specific keyword by ID.")
        keyword = Keyword(
            external_id=uuid.uuid4(),
            keyword="uber eats",
            merchant_id=self.commerce
        ).save()
        print(f"Keyword created with ID: {keyword.id}")
        response = self.client.get(self.url_detail(str(keyword.id)))  # Use external_id
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        print(f"Response status: {response.status_code}")
        self.assertEqual(response.data['keyword'], "uber eats")
        print("Verified that the retrieved keyword entry matches the expected data.")

    def test_update_keyword(self):
        print("\n[TEST] Updating a specific keyword entry.")
        keyword = Keyword(
            external_id=uuid.uuid4(),
            keyword="uber eats",
            merchant_id=self.commerce
        ).save()
        data = {
            'keyword': 'uber eats updated',
            'merchant_id': str(self.commerce.id)  # Use commerce.id for the reference
        }
        print(f"Updating keyword with ID: {keyword.id} with data: {data}")
        response = self.client.put(self.url_detail(str(keyword.id)), data, format='json')  # Use external_id
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        updated_keyword = Keyword.objects.get(external_id=keyword.external_id)
        self.assertEqual(updated_keyword.keyword, 'uber eats updated')
        print("Verified that the keyword entry was updated correctly.")

    def test_delete_keyword(self):
        # Create a keyword for testing
        keyword = Keyword(
            external_id=uuid.uuid4(),
            keyword="for delete",
            merchant_id=self.commerce
        ).save()
         

    # Perform delete request using ObjectId
        response = self.client.delete(self.url_detail(str(keyword.id)))

    # Assertions
        self.assertEqual(response.status_code, 204)  # No Content