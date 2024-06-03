import unittest

from django.test import TestCase
from rest_framework.test import APITestCase, APIClient
#model
from django.contrib.auth.models import User
from rest_framework.authtoken.models import Token

import logging


logger = logging.getLogger(__name__)
# Create your tests here.

class myTest(TestCase):

    @unittest.skip("暂时跳过此测试")
    def tearDown(self):
        print('清理完毕了')

    def setUp(self):
        self.client = APIClient()
        # 创建用户
        self.user = User.objects.create_user(username='testuser', password='123456')
        # 加入认证信息
        # self.client.force_authenticate(user=self.user)

    def test_login(self):
        data = {'username': 'testuser', 'password': '123456'}
        response = self.client.post('/api/login/',data, format='json')
        token = response.data.get('token')
        print(response.json())
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + token)
        print(token)
        self.assertEqual(response.status_code,200,'登录失败')

    def test_create_dep(self):

        response = self.client.post('/department/')
        print(response.json())

    def test_dep_get(self):
        response = self.client.get('/department/')
        self.assertEqual(response.status_code, 200,'查看部门列表失败')
        response = self.client.get('/department/1')
        self.assertEqual(response.status_code, 200,'查看指定部门失败')

