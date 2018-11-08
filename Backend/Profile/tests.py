import json

from django.contrib.auth.models import User, Permission
from django.test import TestCase, Client


# Create your tests here.


class ProfileTestCase(TestCase):
    """
    test for Profile
    """

    def setUp(self):
        self.client = Client()

        self.user = User.objects.create(username="test_user", is_active=True, email="y.wang@stimage.cn")
        self.user.set_password('supersercret')
        for permission in Permission.objects.all():
            self.user.user_permissions.add(permission)
        self.user.save()
        self.client.login(username="test_user", password="supersercret")

        # create 用户类型
        user_type = {
            "name": "医生",
            "description": "人机对战中AI对手，医生",
        }
        response = self.client.post('/api/v1/usertypes/', json.dumps(user_type), content_type='application/json')
        if response.status_code == 201:
            self.user_type = response.json()
        else:
            print(response.json())

        model = {
            "user": self.user.id,
            "nickname": "zero",
            "type": self.user_type['id'],
        }
        response = self.client.post('/api/v1/profiles/', json.dumps(model), content_type='application/json')

        if response.status_code == 201:
            self.model_id = response.json()['id']
        else:
            print(response.json())

    def test_model_get(self):
        response = self.client.get("/api/v1/profiles/", )
        self.assertEqual(response.status_code, 200, (response.json()))

        response = self.client.get('/api/v1/profiles/{}/'.format(self.model_id), )
        self.assertEqual(response.status_code, 200, (response.json()))

    def test_model_post(self):
        model = {
            "user": self.user.id,
            "nickname": "zero",
            "type": self.user_type['id'],
        }
        response = self.client.post('/api/v1/profiles/', json.dumps(model), content_type='application/json')
        self.assertEqual(response.status_code, 400, (response.json()))

    def test_model_create_user_post(self):
        model = {
            "type": 1,
            "nickname": "zero",
            "user": {
                "username": "13260231030",
            }
        }

        response = self.client.post('/api/v1/users/', json.dumps(model), content_type='application/json')
        print(response.json())
        self.assertEqual(response.status_code, 201, (response.json()))

    def test_model_patch(self):
        user_type = {
            "name": "医生01",
            "description": "人机对战中AI对手，医生01",
        }
        response = self.client.post('/api/v1/usertypes/', json.dumps(user_type), content_type='application/json')
        if response.status_code == 201:
            user_type = response.json()
        else:
            print(response.json())

        response = self.client.patch('/api/v1/profiles/{}/'.format(self.model_id),
                                     json.dumps({'type': user_type['id']}), content_type='application/json')
        self.assertEqual(response.status_code, 200, (response.json()))

    def test_model_delete(self):
        response = self.client.delete('/api/v1/profiles/{}/'.format(self.model_id), )
        self.assertEqual(response.status_code, 204, response.content)
