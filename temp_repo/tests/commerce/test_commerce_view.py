import random
import string
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from temp_repo.models.commerce import Commerce
from temp_repo.models.category import Category
from bson import ObjectId

class CommerceTestCase(APITestCase):

    def setUp(self):
        self.category = Category(name="Food", type="expense").save()
        self.url_list_create = reverse('commerce-list-create')
        self.url_detail = lambda pk: reverse('commerce-detail', kwargs={'commerce_id': pk})

    def test_create_commerce(self):
        print("\n[TEST] Creating a new commerce.")
        random_name = ''.join(random.choices(string.ascii_uppercase + string.digits, k=10))
        data = {
            'merchant_name': random_name,  # Unique name
            'merchant_logo': 'http://example.com/ubereats.png',
            'category': str(self.category.id)  # Assuming self.category is set up in setUp method
        }
        print(f"Sending POST request with data: {data}")
        response = self.client.post(self.url_list_create, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        print(f"Response status: {response.status_code}")
        created_commerce = Commerce.objects.get(merchant_name=random_name)
        self.assertIsNotNone(created_commerce)
        print("Verified that the new commerce entry exists in the database.")

    def test_get_all_commerces(self):
        print("\n[TEST] Retrieving all commerces.")
        Commerce(merchant_name="Uber Eats", merchant_logo="http://example.com/ubereats.png", category=self.category).save()
        Commerce(merchant_name="Rappi", merchant_logo="http://example.com/rappi.png", category=self.category).save()
        print("2 commerces created.")
        response = self.client.get(self.url_list_create)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        print(f"Response status: {response.status_code}")
        self.assertGreaterEqual(len(response.data), 2)
        print("Verified that 2 or more commerce entries are retrieved.")

    def test_get_commerce(self):
        print("\n[TEST] Retrieving a specific commerce by ID.")
        commerce = Commerce(merchant_name="Uber Eats", merchant_logo="http://example.com/ubereats.png", category=self.category).save()
        print(f"Commerce created with ID: {commerce.id}")
        response = self.client.get(self.url_detail(str(commerce.id)))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        print(f"Response status: {response.status_code}")
        self.assertEqual(response.data['merchant_name'], "Uber Eats")
        print("Verified that the retrieved commerce entry matches the expected data.")

    def test_update_commerce(self):
        print("\n[TEST] Updating a specific commerce entry.")
        commerce = Commerce(merchant_name="Uber Eats", merchant_logo="http://example.com/ubereats.png", category=self.category).save()
        data = {
            'merchant_name': 'Uber Eats Updated',
            'merchant_logo': 'http://example.com/ubereats_updated.png',
            'category': str(self.category.id)
        }
        print(f"Updating commerce with ID: {commerce.id} with data: {data}")
        response = self.client.put(self.url_detail(str(commerce.id)), data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        updated_commerce = Commerce.objects.get(id=commerce.id)
        self.assertEqual(updated_commerce.merchant_name, 'Uber Eats Updated')
        print("Verified that the commerce entry was updated correctly.")

    def test_delete_commerce(self):
        print("\n[TEST] Deleting a specific commerce entry.")
        commerce = Commerce(merchant_name="Uber Eats", merchant_logo="http://example.com/ubereats.png", category=self.category).save()
        print(f"Deleting commerce with ID: {commerce.id}")
        response = self.client.delete(self.url_detail(str(commerce.id)))
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        print("Verified that the commerce entry was deleted.")
