import json

from django.contrib.auth.models import User, Permission
from django.test import TestCase, Client
import random


# Create your tests here.


class LabelTestCase(TestCase):
    """
    test for Label
    """

    def setUp(self):
        self.client = Client()

        self.user = User.objects.create(username="test_user", is_active=True, email="y.wang@stimage.cn")
        self.user.set_password('supersercret')
        for permission in Permission.objects.all():
            self.user.user_permissions.add(permission)
        self.user.save()
        self.client.login(username="test_user", password="supersercret")

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

        pt = {
            "name": "XXXXX",
            "color": "#000000",
            "description": "异常病理类型01"
        }
        response = self.client.post('/api/v1/types/', json.dumps(pt), content_type='application/json')
        if response.status_code == 201:
            self.cell_type = response.json()
        else:
            print(response.json())

        model = {
            "image": self.tiff['id'],
            "cell_type": self.cell_type['id'],
            "x": random.random(),
            "y": random.random(),
            "w": random.random(),
            "h": random.random(),
        }
        response = self.client.post('/api/v1/labels/', json.dumps(model), content_type='application/json')

        if response.status_code == 201:
            self.model_id = response.json()['id']
        else:
            print(response.json())

    def test_model_get(self):
        response = self.client.get("/api/v1/labels/", )
        self.assertEqual(response.status_code, 200, (response.json()))

        response = self.client.get('/api/v1/labels/{}/'.format(self.model_id), )
        self.assertEqual(response.status_code, 200, (response.json()))

    def test_model_post(self):
        model = {
            "image": self.tiff['id'],
            "cell_type": self.cell_type['id'],
            "x": random.random(),
            "y": random.random(),
            "w": random.random(),
            "h": random.random(),
        }
        response = self.client.post('/api/v1/labels/', json.dumps(model), content_type='application/json')
        self.assertEqual(response.status_code, 201, (response.json()))

    def test_model_patch(self):
        model = {
            "w": random.random(),
            "h": random.random(),
        }

        response = self.client.patch('/api/v1/labels/{}/'.format(self.model_id),
                                     json.dumps(model), content_type='application/json')
        self.assertEqual(response.status_code, 200, (response.json()))

    def test_model_delete(self):
        response = self.client.delete('/api/v1/labels/{}/'.format(self.model_id), )
        self.assertEqual(response.status_code, 204, response.content)
