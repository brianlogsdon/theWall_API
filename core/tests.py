from django.urls import reverse
from rest_framework.test import APIRequestFactory
from rest_framework.test import APITestCase
from rest_framework.test import APIClient
from django.contrib.auth.models import User
from rest_framework.authtoken.models import Token
from rest_framework import status

class APITest(APITestCase):
    def setUp(self):
        #  originally create a user. 
        self.test_user = User.objects.create_user('testuser', 'test@example.com', 'testpassword')

        # URL for creating an account.
        self.create_url = reverse('account-create')

    def test_create_user(self):
        """
        Ensure we can create a new user and it returns a token
        """
        data = {
                'username': 'foobar',
                'email': 'foobar@example.com',
                'password': 'somepassword'
                }

        response = self.client.post(self.create_url , data, format='json')
        user = User.objects.latest('id')
        
        self.assertEqual(User.objects.count(), 2)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['username'], data['username'])
        self.assertEqual(response.data['email'], data['email'])
        self.assertIn("token", response.data)

   

    def test_create_user_with_no_password(self):
        data = {
                'username': 'foobar',
                'email': 'foobarbaz@example.com',
                'password': ''
                }

        response = self.client.post(self.create_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(User.objects.count(), 1)
        self.assertEqual(len(response.data['password']), 1)

    
    def test_create_user_with_no_username(self):
        data = {
                'username': '',
                'email': 'foobarbaz@example.com',
                'password': 'foobarbaz'
                }

        response = self.client.post(self.create_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(User.objects.count(), 1)
        self.assertEqual(len(response.data['username']), 1)
    
    #make sure anyone can read messages
    def test_read_messages(self):
        response = self.client.get('/messages/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
    
    #make sure you cannot post message without be authenticated
    def post_bad_message(self):
        data = {'name':'brian','message': 'hello world'}
        response = self.client.post('/messages/', data, format='json')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def post_good_message(self):
        client.force_authenticate(user=user)
        data = {'name':'brian','message': 'hello world'}
        response = self.client.post('/messages/', data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
    
    

    


   

    