from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from temp_repo.models.commerce import Commerce
from temp_repo.models.category import Category
import uuid

def setup_test_data():
    print("\n[Setup] Creating category and cleaning up the database...")
    category = Category(id=uuid.uuid4(), name="Food", type="expense")
    category.save()
    Commerce.objects.delete()
    print(f"Category created with ID: {category.id}")
    return category

class CommerceTestCase(APITestCase):
    def setUp(self):
        print("[Setup] Creating commerce and category for commerce tests...")
        self.category = Category(id=uuid.uuid4(), name="Food", type="expense").save()
        self.commerce = Commerce(
            id=uuid.uuid4(),
            merchant_name="Uber Eats",
            merchant_logo="http://example.com/logo.png",
            category=self.category
        ).save()
        print(f"Commerce created with ID: {self.commerce.id}, Category ID: {self.category.id}")
        self.url_list_create = reverse('commerce-list-create')
        self.url_detail = lambda pk: reverse('commerce-detail', kwargs={'commerce_id': pk})

    def test_create_commerce(self):
        print("\n[TEST] Creating a new commerce entry.")
        data = {
            'merchant_name': 'Uber Eats',
            'merchant_logo': 'http://example.com/logo.png',
            'category': str(self.category.id)
        }
        print(f"Sending POST request with data: {data}")
        response = self.client.post(self.url_list_create, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        print(f"Response status: {response.status_code}")
        self.assertEqual(Commerce.objects.count(), 1)
        print("Verified that 1 commerce entry exists in the database.")

    def test_get_all_commerces(self):
        print("\n[TEST] Retrieving all commerce entries.")
        Commerce(id=uuid.uuid4(), merchant_name="Uber", merchant_logo="http://example.com/uber.png", category=self.category).save()
        Commerce(id=uuid.uuid4(), merchant_name="Deliveroo", merchant_logo="http://example.com/deliveroo.png", category=self.category).save()
        print("2 commerce entries created.")
        response = self.client.get(self.url_list_create)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        print(f"Response status: {response.status_code}")
        self.assertEqual(len(response.data), 2)
        print("Verified that 2 commerce entries are retrieved.")

    def test_get_commerce(self):
        print("\n[TEST] Retrieving a specific commerce entry by ID.")
        commerce = Commerce(id=uuid.uuid4(), merchant_name="Uber Eats", merchant_logo="http://example.com/ubereats.png", category=self.category).save()
        print(f"Commerce created with ID: {commerce.id}")
        response = self.client.get(self.url_detail(commerce.id))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        print(f"Response status: {response.status_code}")
        self.assertEqual(response.data['merchant_name'], "Uber Eats")
        print("Verified that the retrieved commerce entry matches the expected data.")

    def test_update_commerce(self):
        print("\n[TEST] Updating a specific commerce entry.")
        commerce = Commerce(id=uuid.uuid4(), merchant_name="Uber Eats", merchant_logo="http://example.com/ubereats.png", category=self.category).save()
        data = {
            'merchant_name': 'Uber Eats Updated',
            'merchant_logo': 'http://example.com/ubereats_updated.png',
            'category': str(self.category.id)
        }
        print(f"Updating commerce with ID: {commerce.id} with data: {data}")
        response = self.client.put(self.url_detail(commerce.id), data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        updated_commerce = Commerce.objects.get(id=commerce.id)
        self.assertEqual(updated_commerce.merchant_name, 'Uber Eats Updated')
        print("Verified that the commerce entry was updated correctly.")

    def test_delete_commerce(self):
        print("\n[TEST] Deleting a specific commerce entry.")
        commerce = Commerce(id=uuid.uuid4(), merchant_name="Uber Eats", merchant_logo="http://example.com/ubereats.png", category=self.category).save()
        print(f"Deleting commerce with ID: {commerce.id}")
        response = self.client.delete(self.url_detail(commerce.id))
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        print(f"Response status: {response.status_code}")
        self.assertEqual(Commerce.objects.count(), 0)
        print("Verified that the commerce entry was deleted.")
