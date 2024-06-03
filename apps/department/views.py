from django.contrib.auth.models import User
from django.db import transaction
from django.shortcuts import render
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
from apps.department.permissions import IsSelfManagerDoDepOrReadOnly

from apps.snippets.serializers import UserSerializer
# request typing
from rest_framework.request import Request


# Create your views here.


class DepartmentViewSet(viewsets.ModelViewSet):
    """
    @URL: dep
    @URL_obj: dep/<int:pk>
    @权限：
        超级用户：增加，删除，修改社团
        自身社团的管理员：修改社团
        普通用户：可读权限
    @description:
        This ViewSet automatically provides `list`, `create`, `retrieve`,
        `update` and `destroy` actions.
    """
    queryset = Department.objects.all()
    serializer_class = DepartmentSerializer
    permission_classes = [IsSelfManagerDoDepOrReadOnly]


class DepartMemberViewSet(viewsets.ModelViewSet):
    """
    @URL：  dep/<int:dep_id>/members
    @URL_obj: dep/<int:dep_id>/members/<int:pk>
    @权限：
            管理员：修改成员  （比如哪个成员加入哪个社团）
            社团管理员：删除自身社团成员，增加自身社团的成员
            普通用户：可读权限
    @description:
        This ViewSet automatically provides `list`, `create`, `retrieve`,
        `update` and `destroy` actions.
    """
    queryset = DepartMember.objects.all()
    serializer_class = DepartMemberSerializer
    permission_classes = []

    @action(detail=False, methods=['GET'], permission_classes=[permissions.IsAuthenticated], url_path='custom-path')
    def custom_list(self, request, **kwargs):
        # Custom list logic here
        return Response({"message": "Custom list action"})


class DepartmentRequestViewSet(viewsets.ModelViewSet):
    queryset = DepartmentRequest.objects.all()
    serializer_class = DepartmentRequestSerializer
    permission_classes = [permissions.IsAuthenticated]

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

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)
