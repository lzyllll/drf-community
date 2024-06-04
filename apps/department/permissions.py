from django.contrib.auth.models import User
from rest_framework.permissions import BasePermission, SAFE_METHODS, IsAdminUser
from rest_framework.request import Request
from rest_framework.views import View
from apps.department.models import Department, DepartmentRequest, DepartMember
from apps.department.views import DepartmentRequestViewSet

'''
判断社团的管理员，是否管理的是本身的社团
'''


def isAdmin(request) -> bool:
    return bool(request.user and request.user.is_staff)


class DepartmentPermissionControl(BasePermission):

    def has_permission(self, request: Request, view):
        if request.method in SAFE_METHODS:
            return True
        return isAdmin(request)

    def has_object_permission(self, request, view, obj):

        # 终级管理员可以
        # 禁止社团管理员删除社团
        # 其他obj操作允许
        if request.method in ['DELETE']:
            return isAdmin(request)
        else:
            return obj.head_user in request.user or isAdmin(request)


class DepartMemberPermissionControl(BasePermission):


    def has_object_permission(self, request, view, obj:DepartMember):

        # 终级管理员可以
        # 禁止社团管理员删除社团
        # 其他obj操作允许
        if request.method in ['DELETE']:
            return  obj.department in request.user.header_department.all() or isAdmin(request)
        else:
            return isAdmin(request)


class DepartRequestPermissionControl(BasePermission):

    def has_object_permission(self, request: Request, view: DepartmentRequestViewSet, obj: DepartmentRequest):
        # 社团管理员仅仅有同意请求和拒绝请求的权限
        if view.action in ['approve', 'reject']:
            # 如果目标部门，为当前操作用户所拥有的部门权限
            return obj.department in request.user.header_department.all() or isAdmin(request)
        # 终级管理员都可以
        return isAdmin(request)
