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
        self.category = Category(id=uuid.uuid4(), name="Food", type="expense").save()
        self.commerce = Commerce(
            id=uuid.uuid4(),
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
            'merchant_id': str(self.commerce.id)
        }
        print(f"Sending POST request with data: {data}")
        response = self.client.post(self.url_list_create, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        print(f"Response status: {response.status_code}")
        self.assertEqual(Keyword.objects.count(), 1)
        print("Verified that 1 keyword entry exists in the database.")

    def test_get_all_keywords(self):
        print("\n[TEST] Retrieving all keywords.")
        Keyword(id=uuid.uuid4(), keyword="uber", merchant_id=self.commerce).save()
        Keyword(id=uuid.uuid4(), keyword="food delivery", merchant_id=self.commerce).save()
        print("2 keywords created.")
        response = self.client.get(self.url_list_create)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        print(f"Response status: {response.status_code}")
        self.assertEqual(len(response.data), 2)
        print("Verified that 2 keyword entries are retrieved.")

    def test_get_keyword(self):
        print("\n[TEST] Retrieving a specific keyword by ID.")
        keyword = Keyword(id=uuid.uuid4(), keyword="uber eats", merchant_id=self.commerce).save()
        print(f"Keyword created with ID: {keyword.id}")
        response = self.client.get(self.url_detail(keyword.id))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        print(f"Response status: {response.status_code}")
        self.assertEqual(response.data['keyword'], "uber eats")
        print("Verified that the retrieved keyword entry matches the expected data.")

    def test_update_keyword(self):
        print("\n[TEST] Updating a specific keyword entry.")
        keyword = Keyword(id=uuid.uuid4(), keyword="uber eats", merchant_id=self.commerce).save()
        data = {
            'keyword': 'uber eats updated',
            'merchant_id': str(self.commerce.id)
        }
        print(f"Updating keyword with ID: {keyword.id} with data: {data}")
        response = self.client.put(self.url_detail(keyword.id), data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        updated_keyword = Keyword.objects.get(id=keyword.id)
        self.assertEqual(updated_keyword.keyword, 'uber eats updated')
        print("Verified that the keyword entry was updated correctly.")

    def test_delete_keyword(self):
        print("\n[TEST] Deleting a specific keyword entry.")
        keyword = Keyword(id=uuid.uuid4(), keyword="uber eats", merchant_id=self.commerce).save()
        print(f"Deleting keyword with ID: {keyword.id}")
        response = self.client.delete(self.url_detail(keyword.id))
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        print(f"Response status: {response.status_code}")
        self.assertEqual(Keyword.objects.count(), 0)
        print("Verified that the keyword entry was deleted.")