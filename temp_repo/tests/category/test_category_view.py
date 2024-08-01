from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from temp_repo.models.category import Category
import uuid

class CategoryTestCase(APITestCase):

    def setUp(self):
        self.url_list_create = reverse('category-list-create')
        self.url_detail = lambda pk: reverse('category-detail', kwargs={'category_id': pk})
        print("\n[Setup] Cleaning up the database...")
        Category.objects.delete()
        print("Database cleaned and ready for testing.")

    def test_create_category(self):
        print("\n[TEST] Creating a new category.")
        data = {
            'name': 'Restaurantes',
            'type': 'expense'
        }
        print(f"Sending POST request with data: {data}")
        response = self.client.post(self.url_list_create, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        print(f"Response status: {response.status_code}")
        self.assertEqual(Category.objects.count(), 1)
        print("Verified that 1 category entry exists in the database.")

    def test_get_all_categories(self):
        print("\n[TEST] Retrieving all categories.")
        Category(id=uuid.uuid4(), name="Groceries", type="expense").save()
        Category(id=uuid.uuid4(), name="Salary", type="income").save()
        print("2 categories created.")
        response = self.client.get(self.url_list_create)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        print(f"Response status: {response.status_code}")
        self.assertEqual(len(response.data), 2)
        print("Verified that 2 category entries are retrieved.")

    def test_get_category(self):
        print("\n[TEST] Retrieving a specific category by ID.")
        category = Category(id=uuid.uuid4(), name="Entertainment", type="expense").save()
        print(f"Category created with ID: {category.id}")
        response = self.client.get(self.url_detail(category.id))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        print(f"Response status: {response.status_code}")
        self.assertEqual(response.data['name'], "Entertainment")
        print("Verified that the retrieved category entry matches the expected data.")

    def test_update_category(self):
        print("\n[TEST] Updating a specific category entry.")
        category = Category(id=uuid.uuid4(), name="Bills", type="expense").save()
        data = {
            'name': 'Utilities',
            'type': 'expense'
        }
        print(f"Updating category with ID: {category.id} with data: {data}")
        response = self.client.put(self.url_detail(category.id), data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        updated_category = Category.objects.get(id=category.id)
        self.assertEqual(updated_category.name, 'Utilities')
        print("Verified that the category entry was updated correctly.")

    def test_delete_category(self):
        print("\n[TEST] Deleting a specific category entry.")
        category = Category(id=uuid.uuid4(), name="Shopping", type="expense").save()
        print(f"Deleting category with ID: {category.id}")
        response = self.client.delete(self.url_detail(category.id))
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        print(f"Response status: {response.status_code}")
        self.assertEqual(Category.objects.count(), 0)
        print("Verified that the category entry was deleted.")
