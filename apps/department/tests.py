# tests.py

import pytest
from django.contrib.auth.models import User
from rest_framework import status
from rest_framework.test import APIClient
from apps.department.models import Department, DepartMember, DepartmentRequest


# todo 之后可能会用reverse来代替字符串的url，url可能会有变动

@pytest.fixture
def api_client():
    return APIClient()


@pytest.fixture
def admin_user(db):
    return User.objects.create_superuser(username='admin', email='admin@example.com', password='admin')


@pytest.fixture
def regular_user(db):
    return User.objects.create_user(username='user', email='user@example.com', password='user')


@pytest.fixture
def department(db, admin_user):
    return Department.objects.create(name='admin Department', head_user_id=admin_user.id)


@pytest.fixture
def regular_department(db, regular_user):
    return Department.objects.create(name='regular Department', head_user_id=regular_user.id)


@pytest.fixture
def depart_member(db, department, regular_user):
    return DepartMember.objects.create(department=department, user=regular_user)


@pytest.fixture
def regular_depart_member(db, regular_department, regular_user):
    return DepartMember.objects.create(department=regular_department, user=regular_user)


@pytest.fixture
def department_request(db, department, regular_user):
    return DepartmentRequest.objects.create(department=department, user=regular_user)


@pytest.fixture
def regular_department_request(db, regular_department, regular_user):
    return DepartmentRequest.objects.create(department=regular_department, user=regular_user)


@pytest.mark.django_db
class TestDepartmentViewSet:
    def test_list_departments_as_admin(self, api_client, admin_user):
        api_client.force_authenticate(user=admin_user)

        response = api_client.get('/department/')
        assert response.status_code == status.HTTP_200_OK

    # admin可以创建部门
    def test_create_department_as_admin(self, api_client, admin_user):
        api_client.force_authenticate(user=admin_user)
        request_data = {
            "name": "new dep",
            "description": "this is new dep",
            "head_user_id": admin_user.id,
            "member_ids": []
        }
        response = api_client.post('/department/', request_data, format='json')
        assert response.status_code == status.HTTP_201_CREATED

    # 普通用户无法创建部门
    def test_create_department_as_regular_user(self, api_client, regular_user):
        api_client.force_authenticate(user=regular_user)
        request_data = {
            "name": "New Department",
            "description": "This is a new department",
            "head_user_id": regular_user.id,
            "member_ids": []
        }
        response = api_client.post('/department/', request_data, format='json')
        assert response.status_code == status.HTTP_403_FORBIDDEN


@pytest.mark.django_db
class TestDepartMemberViewSet:
    # safe 不用检查
    def test_list_depart_members_as_regular_user(self, api_client, regular_user):
        api_client.force_authenticate(user=regular_user)
        response = api_client.get('/department_members/')
        assert response.status_code == status.HTTP_200_OK

    # admin 任意操作
    def test_create_depart_member_as_admin(self, api_client, admin_user, department, regular_user):
        api_client.force_authenticate(user=admin_user)
        response = api_client.post('/department_members/',
                                   {'user_id': regular_user.id, 'department_id': department.id})
        assert response.status_code == status.HTTP_201_CREATED

    def test_delete_depart_member_as_admin(self, api_client, admin_user, depart_member):
        api_client.force_authenticate(user=admin_user)
        response = api_client.delete(f'/department_members/{depart_member.id}/')
        assert response.status_code == status.HTTP_204_NO_CONTENT

    # 自身社团的，可以删除成员
    def test_delete_depart_member_as_selfManager(self, api_client, regular_department, regular_depart_member,
                                                 regular_user):
        api_client.force_authenticate(user=regular_user)
        response = api_client.delete(f'/department_members/{regular_depart_member.id}/')
        assert response.status_code == status.HTTP_204_NO_CONTENT


@pytest.mark.django_db
class TestDepartmentRequestViewSet:
    # safe，任意人可
    def test_list_department_requests_as_admin(self, api_client, admin_user):
        api_client.force_authenticate(user=admin_user)
        response = api_client.get('/department_requests/')
        assert response.status_code == status.HTTP_200_OK

    # 任意用户，可以发送request请求，且user为request.user
    def test_create_department_request_as_regular_user(self, api_client, regular_user, department):
        api_client.force_authenticate(user=regular_user)
        response = api_client.post('/department_requests/', {'department': department.id}, format='json')
        assert response.status_code == status.HTTP_201_CREATED

    # 自身社团的，可以同意或拒绝请求
    # 非自身社团无法
    def test_approve_department_request_as_selfManager(self, api_client, regular_department_request,
                                                       department_request,regular_depart_member, regular_user):
        api_client.force_authenticate(user=regular_user)
        response = api_client.post(f'/department_requests/{regular_department_request.id}/approve/')
        assert response.status_code == status.HTTP_200_OK

        response = api_client.post(f'/department_requests/{department_request.id}/approve/')
        assert response.status_code == status.HTTP_403_FORBIDDEN

    def test_reject_department_request_as_selfManager(self, api_client, regular_department_request,
                                                      department_request,regular_depart_member, regular_user):
        api_client.force_authenticate(user=regular_user)
        response = api_client.post(f'/department_requests/{regular_department_request.id}/reject/')
        assert response.status_code == status.HTTP_200_OK

        response = api_client.post(f'/department_requests/{department_request.id}/reject/')
        assert response.status_code == status.HTTP_403_FORBIDDEN

    # admin，可同意任何请求
    def test_approve_department_request_as_admin(self, api_client, admin_user, department_request):
        api_client.force_authenticate(user=admin_user)
        response = api_client.post(f'/department_requests/{department_request.id}/approve/')
        assert response.status_code == status.HTTP_200_OK

    def test_reject_department_request_as_admin(self, api_client, admin_user, department_request):
        api_client.force_authenticate(user=admin_user)
        response = api_client.post(f'/department_requests/{department_request.id}/reject/')
        assert response.status_code == status.HTTP_200_OK
