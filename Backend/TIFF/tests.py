import json

from django.contrib.auth.models import User, Permission
from django.test import TestCase, Client


# Create your tests here.


class TIFFTestCase(TestCase):
    """
    test for TIFF
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
            self.image_id = response.json()['id']
        else:
            print(response.json())

    def test_image_get(self):
        response = self.client.get("/api/v1/images/", )
        self.assertEqual(response.status_code, 200, (response.json()))

        response = self.client.get('/api/v1/images/{}/'.format(self.image_id), )
        self.assertEqual(response.status_code, 200, (response.json()))

    def test_image_post(self):
        image = {
            "name": "001.kfb",
            "path": "xx/xx/kfb",
            "progress": '60.0%'
        }
        response = self.client.post('/api/v1/images/', json.dumps(image), content_type='application/json')
        self.assertEqual(response.status_code, 201, (response.json()))

    def test_image_patch(self):
        response = self.client.patch('/api/v1/images/{}/'.format(self.image_id),
                                     json.dumps({'progress': '90.9%'}), content_type='application/json')
        self.assertEqual(response.status_code, 200, (response.json()))

    def test_image_delete(self):
        response = self.client.delete('/api/v1/images/{}/'.format(self.image_id), )
        self.assertEqual(response.status_code, 204, response.content)
