import json

from django.contrib.auth.models import User, Permission
from django.test import TestCase, Client
import uuid


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

        # create pt
        response = self.client.post('/api/v1/missions/',
                                    json.dumps({'name': 'TEST01', 'tip': 'NOTHING', }),
                                    content_type='application/json')

        self.pt = response.json()['id']

        response = self.client.post('/api/v1/images/edit/',
                                    json.dumps({'url': 'xx/xx.tif', 'open_id': str(uuid.uuid4()), 'pt': self.pt}),
                                    content_type='application/json')

        if response.status_code == 201:
            self.parent_id = response.json()['id']
        else:
            print(response.json())

        response = self.client.post('/api/v1/images/label/edit/',
                                    json.dumps(
                                        {'url': 'xx/xx.jpg', 'x': 1, 'y': 1, 'w': 1, 'h': 1, 'parent': self.parent_id}),
                                    content_type='application/json')

        if response.status_code == 201:
            self.parent = response.json()['id']
        else:
            print(response.json())

        response = self.client.post('/api/v1/images/check/edit/',
                                    json.dumps({'url': 'xx/xx.jpg', 'x': 1, 'y': 1, 'w': 1, 'h': 1, 'pt': self.pt,
                                                'parent': self.parent}),
                                    content_type='application/json')

        if response.status_code == 201:
            self.image_id = response.json()['id']
        else:
            print(response.json())

    def test_image_get(self):
        response = self.client.get("/api/v1/images/check/edit/", )
        self.assertEqual(response.status_code, 200, (response.json()))

        response = self.client.get('/api/v1/images/check/edit/{}/'.format(self.image_id), )
        self.assertEqual(response.status_code, 200, (response.json()))

    def test_image_post(self):
        response = self.client.post('/api/v1/images/check/edit/',
                                    json.dumps({'url': 'aa/aa.jpg', 'x': 2, 'y': 2, 'w': 2, 'h': 2, 'pt': self.pt,
                                                'parent': self.parent}),
                                    content_type='application/json')
        self.assertEqual(response.status_code, 201, (response.json()))

    def test_image_batch_post(self):
        response = self.client.post('/api/v1/images/check/edit/',
                                    json.dumps([
                                        {'url': 'bb/bb.jpg', 'x': 2, 'y': 2, 'w': 2, 'h': 2, 'pt': self.pt,
                                         'parent': self.parent},
                                        {'x': 3, 'y': 3, 'w': 3, 'h': 3, 'pt': self.pt, 'parent': self.parent},
                                        {'x': 4, 'y': 4, 'w': 4, 'h': 4, 'pt': self.pt, 'parent': self.parent},
                                    ]),
                                    content_type='application/json')
        self.assertEqual(response.status_code, 201, (response.json()))
        response = self.client.get("/api/v1/images/check/edit/", )
        print(response.json())

    def test_image_put(self):
        response = self.client.put('/api/v1/images/check/edit/{}/'.format(self.image_id),
                                   json.dumps(
                                       {'url': 'aa/aa.jpg', 'x': 2, 'y': 2, 'w': 2, 'h': 2, 'pt': self.pt,
                                        'parent': self.parent}),
                                   content_type='application/json')
        self.assertEqual(response.status_code, 200, (response.json()))

    def test_image_patch(self):
        response = self.client.patch('/api/v1/images/check/edit/{}/'.format(self.image_id),
                                     json.dumps({'flag': 'INVALID'}), content_type='application/json')
        self.assertEqual(response.status_code, 200, (response.json()))

    def test_image_delete(self):
        response = self.client.delete('/api/v1/images/check/edit/{}/'.format(self.image_id), )
        self.assertEqual(response.status_code, 204, (response.content))