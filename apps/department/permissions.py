from django.contrib.auth.models import User
from rest_framework.permissions import BasePermission, SAFE_METHODS, IsAdminUser
from rest_framework.request import Request
from rest_framework.views import View
from apps.department.models import Department, DepartmentRequest, DepartMember

'''
判断社团的管理员，是否管理的是本身的社团


'''


class DepartmentPermissionControl(BasePermission):
    def has_permission(self, request, view):
        if request.method in SAFE_METHODS:
            return True
            # 如果是对像级的处理，交给下obj——perm处理
        if view.kwargs.get('pk'):
            return True

        return bool(request.user and request.user.is_staff)

    def has_object_permission(self, request, view, obj):

        # 终级管理员可以
        # 禁止社团管理员删除社团
        # 其他obj操作允许

        if request.method in SAFE_METHODS:
            return True
        if request.method in ['PUT','PATCH']:
            return obj.head_user == request.user
        else:
            return bool(request.user and request.user.is_staff)


class DepartMemberPermissionControl(BasePermission):
    def has_permission(self, request: Request, view):


        if request.method in SAFE_METHODS:
            return True
        # 如果是对像级的处理，交给下obj——perm处理
        if view.kwargs.get('pk'):
            return True
        return bool(request.user and request.user.is_staff)

    def has_object_permission(self, request, view, obj: DepartMember):

        # 终级管理员可以
        # 禁止社团管理员删除社团
        # 其他obj操作允许

        if request.method in SAFE_METHODS:
            return True
        if request.method in ['DELETE']:
            return obj.department in request.user.header_department.all()
        else:
            return bool(request.user and request.user.is_staff)


class DepartRequestPermissionControl(BasePermission):

    def has_object_permission(self, request: Request, view, obj: DepartmentRequest):

        # 社团管理员仅仅有同意请求和拒绝请求的权限
        if request.method in SAFE_METHODS:
            return True
        if view.action in ['approve', 'reject']:
            # 如果目标部门，为当前操作用户所拥有的部门权限
            return obj.department in request.user.header_department.all()
        # 终级管理员都可以
        return bool(request.user and request.user.is_staff)
