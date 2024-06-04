from django.contrib.auth.models import User
from django.db import transaction
from django.shortcuts import render
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import viewsets, permissions, status

from rest_framework.decorators import api_view, renderer_classes, action
from rest_framework.generics import get_object_or_404
from rest_framework.pagination import LimitOffsetPagination, PageNumberPagination
from rest_framework.renderers import JSONRenderer, BrowsableAPIRenderer

from rest_framework.response import Response
# model
from apps.department.models import Department, DepartMember, DepartmentRequest
# serialier
from apps.department.serializers import DepartmentSerializer, DepartmentRequestSerializer, DepartMemberSerializer
# permission
from apps.department.permissions import DepartmentPermissionControl, DepartRequestPermissionControl, \
    DepartMemberPermissionControl

from apps.snippets.serializers import UserSerializer
# request typing
from rest_framework.request import Request


# Create your views here.


class DepartmentViewSet(viewsets.ModelViewSet):
    """
    @URL: dep
    @URL_obj: dep/<int:pk>
    @权限：
        admin：增加，删除，修改社团
        自身社团的管理员：修改社团
        普通用户：可读权限
    @filter name,head_user_id
    @description:
        This ViewSet automatically provides `list`, `create`, `retrieve`,
        `update` and `destroy` actions.
    """
    queryset = Department.objects.all()
    serializer_class = DepartmentSerializer
    permission_classes = [DepartmentPermissionControl]
    filterset_fields = ['name','head_user_id']



class DepartMemberViewSet(viewsets.ModelViewSet):
    """
    @URL：  dep_members
    @URL_obj: dep_members/<int:pk>
    @filter : dep_id 查看指定部门的成员
    @权限：
            admin：修改成员,增加成员（所有权限）  （比如哪个成员加入哪个社团）
            社团管理员：删除自身社团成员
            普通用户：可读权限
    @description:
        This ViewSet automatically provides `list`, `create`, `retrieve`,
        `update` and `destroy` actions.
    """
    queryset = DepartMember.objects.all()
    serializer_class = DepartMemberSerializer
    permission_classes = [DepartMemberPermissionControl]
    filterset_fields = ['department_id']

    @action(detail=False, methods=['GET'], permission_classes=[permissions.IsAuthenticated], url_path='custom-path')
    def custom_list(self, request, **kwargs):
        # Custom list logic here
        return Response({"message": "Custom list action"})


class DepartmentRequestViewSet(viewsets.ModelViewSet):
    """
    @URL dep_requests
    @URL_obj dep_requests/<int:pk>
    @filter dep_id 查看指定的部门的请求
    @permission:
        admin：任意请求
        自身社团管理员：approve，reject自身社团请求相关
        普通成员：post，del，

    """
    queryset = DepartmentRequest.objects.all()
    serializer_class = DepartmentRequestSerializer
    permission_classes = [DepartRequestPermissionControl]
    filterset_fields = ['department_id']


    '''
    因为需要在request中增加，members表也要增加，所以需要transaction
    '''
    @transaction.atomic()
    @action(detail=True, methods=['post'], permission_classes=[permissions.IsAuthenticated])
    def approve(self, request, pk=None):
        department_request = self.get_object()
        # 同意请求，保存
        department_request.status = DepartmentRequest.APPROVED
        department_request.save()
        # 添加到成员
        department = department_request.department
        user = department_request.user
        if not DepartMember.objects.filter(user=user, department=department).exists():
            DepartMember.objects.create(user=user, department=department)

        return Response({'status': 'request approved'}, status=status.HTTP_200_OK)

    @action(detail=True, methods=['post'], permission_classes=[permissions.IsAuthenticated])
    def reject(self, request, pk=None):
        department_request = self.get_object()
        # 拒绝请求，保存
        department_request.status = DepartmentRequest.REJECTED
        department_request.save()
        return Response({'status': 'request rejected'}, status=status.HTTP_200_OK)

    '''
    发送请求，默认为自身auth的user发送
    '''
    def perform_create(self, serializer):
        serializer.save(user=self.request.user)
