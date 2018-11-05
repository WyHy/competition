import json

from django.contrib.auth.models import User, Permission
from django.test import TestCase, Client


# Create your tests here.


class AllocationTestCase(TestCase):
    """
    test for Allocation
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
            "profile": self.user.id,
            "type": self.user_type['id'],
        }
        response = self.client.post('/api/v1/profiles/', json.dumps(model), content_type='application/json')

        if response.status_code == 201:
            self.profile = response.json()
        else:
            print(response.json())

        # create IMAGE
        image = {
            "name": "001.kfb",
            "path": "xx/xx/kfb",
        }
        response = self.client.post('/api/v1/images/', json.dumps(image), content_type='application/json')
        if response.status_code == 201:
            self.tiff = response.json()
        else:
            print(response.json())

        model = {
            "profile": self.profile['id'],
            "tiff": self.tiff['id'],
        }
        response = self.client.post('/api/v1/missions/', json.dumps(model), content_type='application/json')

        if response.status_code == 201:
            self.model_id = response.json()['id']
        else:
            print(response.json())

    def test_model_get(self):
        response = self.client.get("/api/v1/missions/", )
        self.assertEqual(response.status_code, 200, (response.json()))

        response = self.client.get('/api/v1/missions/{}/'.format(self.model_id), )
        self.assertEqual(response.status_code, 200, (response.json()))

    def test_model_post(self):
        model = {
            "profile": self.user.id,
            "tiff": self.tiff['id'],
        }
        response = self.client.post('/api/v1/missions/', json.dumps(model), content_type='application/json')
        self.assertEqual(response.status_code, 400, (response.json()))

    def test_model_patch(self):
        # create IMAGE
        image = {
            "name": "002.kfb",
            "path": "xx/xx/kfb",
        }
        response = self.client.post('/api/v1/images/', json.dumps(image), content_type='application/json')
        if response.status_code == 201:
            tiff = response.json()
        else:
            print(response.json())

        response = self.client.patch('/api/v1/missions/{}/'.format(self.model_id),
                                     json.dumps({'tiff': tiff['id']}), content_type='application/json')
        self.assertEqual(response.status_code, 200, (response.json()))

    def test_model_delete(self):
        response = self.client.delete('/api/v1/missions/{}/'.format(self.model_id), )
        self.assertEqual(response.status_code, 204, response.content)
