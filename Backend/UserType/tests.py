import json

from django.contrib.auth.models import User, Permission
from django.test import TestCase, Client


# Create your tests here.


class UserTypeTestCase(TestCase):
    """
    test for UserType
    """

    def setUp(self):
        self.client = Client()

        self.user = User.objects.create(username="test_user", is_active=True, email="y.wang@stimage.cn")
        self.user.set_password('supersercret')
        for permission in Permission.objects.all():
            self.user.user_permissions.add(permission)
        self.user.save()
        self.client.login(username="test_user", password="supersercret")

        user_type = {
            "name": "医生",
            "description": "人机对战中AI对手，医生",
        }
        response = self.client.post('/api/v1/usertypes/', json.dumps(user_type), content_type='application/json')

        if response.status_code == 201:
            self.type_id = response.json()['id']
        else:
            print(response.json())

    def test_model_get(self):
        response = self.client.get("/api/v1/usertypes/", )
        self.assertEqual(response.status_code, 200, (response.json()))

        response = self.client.get('/api/v1/usertypes/{}/'.format(self.type_id), )
        self.assertEqual(response.status_code, 200, (response.json()))

    def test_model_post(self):
        user_type = {
            "name": "医生",
            "description": "人机对战中AI对手，医生",
        }
        response = self.client.post('/api/v1/usertypes/', json.dumps(user_type), content_type='application/json')
        self.assertEqual(response.status_code, 201, (response.json()))

    def test_model_patch(self):
        response = self.client.patch('/api/v1/usertypes/{}/'.format(self.type_id),
                                     json.dumps({'progress': '90.9%'}), content_type='application/json')
        self.assertEqual(response.status_code, 200, (response.json()))

    def test_model_delete(self):
        response = self.client.delete('/api/v1/usertypes/{}/'.format(self.type_id), )
        self.assertEqual(response.status_code, 204, response.content)
