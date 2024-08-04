from django.test import TestCase, Client
from unittest.mock import patch
import json
from django.contrib.auth.models import User
from rest_framework_simplejwt.tokens import RefreshToken
from toxicity_checker import is_toxic


class PostCreateAPITest(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.client = Client()
        cls.test_user = User.objects.create_user(id=1, username='testuser', password='testpass')
        refresh = RefreshToken.for_user(cls.test_user)
        cls.token = str(refresh.access_token)

    def setUp(self):
        self.client = Client(HTTP_AUTHORIZATION=f'Bearer {self.token}')

    def test_create_post_entries_with_non_toxic_content(self):
        post_data = {
            "title": "Test Post",
            "content": "This is a post",
            "user_id": self.test_user.id,
        }
        headers = {'content-type': 'application/json'}
        response = self.client.post('/api/posts/create',
                                    json.dumps(post_data),
                                    content_type='application/json',
                                    **headers)
        print(response.content)
        self.assertEqual(response.status_code, 200)
        response_dict = response.json()
        self.assertEqual(response.json()["title"], post_data["title"])
        self.assertEqual(response.json()["content"], post_data["content"])
        self.assertEqual(response.json()["user_id"], self.test_user.id)

    def test_create_post_entries_with_toxic_content(self):
        # Create a request
        post_data = {
            "title": "Test Post",
            "content": "This is a toxic post",
            "user_id": self.test_user.id,
        }
        headers = {'content-type': 'application/json'}
        response = self.client.post('api/posts/create', post_data,  content_type='application/json',
                                      **headers)
        print(response.content)
        self.assertEqual(response.status_code, 403)
        response_dict = response.json()
        self.assertEqual(response_dict, {"message": "The post contains toxic content and has been blocked."})

