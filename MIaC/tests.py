from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from .models import User

class UserListViewTests(APITestCase):

    def setUp(self):
        self.user1 = User.objects.create(
            first_name='John', last_name='Doe', email='johndoe@example.com',
            password='password123', phone='1234567890', gender='M'
        )
        self.user2 = User.objects.create(
            first_name='Jane', last_name='Doe', email='janedoe@example.com',
            password='password123', phone='0987654321', gender='F'
        )
        self.url_list = reverse('user_list')

    def test_get_all_users(self):
        response = self.client.get(self.url_list)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 2)

    def test_search_users_by_first_name(self):
        response = self.client.get(self.url_list, {'first_name': 'John'})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]['first_name'], 'John')

    def test_search_users_by_last_name(self):
        response = self.client.get(self.url_list, {'last_name': 'Doe'})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 2)

    def test_search_users_by_email(self):
        response = self.client.get(self.url_list, {'email': 'johndoe@example.com'})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]['email'], 'johndoe@example.com')

    def test_search_users_by_phone(self):
        response = self.client.get(self.url_list, {'phone': '1234567890'})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]['phone'], '1234567890')

    def test_search_users_by_gender(self):
        response = self.client.get(self.url_list, {'gender': 'F'})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]['gender'], 'F')

    def test_create_user(self):
        data = {
            'first_name': 'Alice',
            'last_name': 'Smith',
            'email': 'alicesmith@example.com',
            'password': 'password123',
            'phone': '1112223333',
            'gender': 'F'
        }
        response = self.client.post(self.url_list, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(User.objects.count(), 3)

    def test_update_user(self):
        user = User.objects.first()
        url = reverse('user_detail', args=[user.id])
        data = {'first_name': 'UpdatedName'}
        response = self.client.put(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        user.refresh_from_db()
        self.assertEqual(user.first_name, 'UpdatedName')

    def test_delete_user(self):
        user = User.objects.first()
        url = reverse('user_detail', args=[user.id])
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(User.objects.count(), 1)
