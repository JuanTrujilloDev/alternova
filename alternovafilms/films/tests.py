from django.urls import reverse, resolve
from rest_framework import status
from rest_framework.test import APIClient, APITestCase
from django.contrib.auth.models import User
from rest_framework.authtoken.models import Token
from django.test import TestCase
import json
class FilmListTest(APITestCase):

    url = reverse('films')
    fixtures = ['users.json','genres.json','film-types.json','films.json','ratings.json']

    def setUp(self) -> None:
        self.user = User.objects.create_user(username='test', email='test@test.com')
        self.user.set_password('password')
        self.user.save()
        self.client.login(username='test', password='password')

    def tearDown(self) -> None:
        pass
    
    def test_retrieve_films(self):
        """
        Ensure we can retrieve films from the API.
        """

        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def retrieve_filtered_films(self):
        pass

    def error_invalid_filter(self):
        pass

    def error_invalid_page(self):

        pass

    def error_no_authenticated(self):
        pass