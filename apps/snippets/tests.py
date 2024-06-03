from django.test import TestCase,Client
import logging
from django.contrib.auth.models import User, Permission
from apps.snippets.models import Snippet
logger = logging.getLogger(__name__)
# Create your tests here.

class myTest(TestCase):
    def setUp(self):
        # 创建一个测试客户端实例
        self.client = Client()
        self.username = 'lzy'
        self.password = 'q1248163264'
        # 加入一个用户
        user = User.objects.create_user(
            id = 2,
            username= self.username,
            email='your_email@example.com',
            password= self.password
        )

        # 保存新创建的 User 对象
        user.save()


    def test_login(self):
        login_data = {
            'username': self.username,
            'password': self.password
        }
        response = self.client.post('/api/login/', login_data)

        self.assertEqual(response.status_code, 200,'登录失败')

        # 提取 token
        token = response.data.get('token')
        print(token)

        # 将 token 添加到授权头中发送请求
        # todo


    def test_query_user(self):
        client = self.client
        response = client.get('/users/')
        self.assertEqual(response.status_code, 200, "user测试失败")
        print(response.json())


    def test_query_detail_user(self):
        client = self.client
        response = client.get('/users/2')
        self.assertEqual(response.status_code, 200, "detail,user测试失败")


    def tearDown(self):
        # from django_redis import get_redis_connection
        # get_redis_connection("default").flushall()
        print('执行完毕')
