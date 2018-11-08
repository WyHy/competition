import json

from django.contrib.auth.models import User, Permission
from django.test import TestCase, Client


# Create your tests here.


class ActivityTestCase(TestCase):
    """
    test for Activity
    """

    def setUp(self):
        self.client = Client()

        self.user = User.objects.create(username="test_user", is_active=True, email="y.wang@stimage.cn")
        self.user.set_password('supersercret')
        for permission in Permission.objects.all():
            self.user.user_permissions.add(permission)
        self.user.save()
        self.client.login(username="test_user", password="supersercret")

        # 大图诊断类型
        tiff_type = {
            "name": "HSIL",
            "color": "#000000",
            "description": "异常病理类型01"
        }
        response = self.client.post('/api/v1/types/', json.dumps(tiff_type), content_type='application/json')

        if response.status_code == 201:
            self.tiff_type_id = response.json()['id']
        else:
            print(response.json())

        # 用户类型
        user_type = {
            "name": "医生",
            "description": "人机对战中AI对手，医生",
        }
        response = self.client.post('/api/v1/usertypes/', json.dumps(user_type), content_type='application/json')
        if response.status_code == 201:
            self.user_type = response.json()
        else:
            print(response.json())

        # 用户信息
        profile = {
            "user": self.user.id,
            "nickname": "zero",
            "type": self.user_type['id'],
        }
        response = self.client.post('/api/v1/profiles/', json.dumps(profile), content_type='application/json')
        if response.status_code == 201:
            self.profile_id = response.json()['id']
        else:
            print(response.json())

        # 大图信息
        tiff = {
            "name": "001.kfb",
            "path": "xx/xx/kfb",
        }
        response = self.client.post('/api/v1/images/', json.dumps(tiff), content_type='application/json')

        if response.status_code == 201:
            self.tiff_id = response.json()['id']
        else:
            print(response.json())

        activity = {
            "image": self.tiff_id,
            "profile": self.profile_id,
            "answer": self.tiff_type_id
        }

        response = self.client.post('/api/v1/activities/', json.dumps(activity), content_type='application/json')

        if response.status_code == 201:
            self.model_id = response.json()['id']
        else:
            print(response.json())

    def test_model_get(self):
        response = self.client.get("/api/v1/activities/", )
        self.assertEqual(response.status_code, 200, (response.json()))

        response = self.client.get('/api/v1/activities/{}/'.format(self.model_id), )
        self.assertEqual(response.status_code, 200, (response.json()))

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

        response = self.client.patch('/api/v1/activities/{}/'.format(self.model_id),
                                     json.dumps({'image': tiff['id']}), content_type='application/json')
        self.assertEqual(response.status_code, 200, (response.json()))

    def test_model_delete(self):
        response = self.client.delete('/api/v1/activities/{}/'.format(self.model_id), )
        self.assertEqual(response.status_code, 204, response.content)
