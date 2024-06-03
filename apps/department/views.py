from django.contrib.auth.models import User
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

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)