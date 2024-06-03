from django.contrib.auth.models import User
from django.shortcuts import render
from rest_framework import viewsets, permissions, status

from rest_framework.decorators import api_view, renderer_classes, action
from rest_framework.generics import get_object_or_404
from rest_framework.pagination import LimitOffsetPagination, PageNumberPagination
from rest_framework.renderers import JSONRenderer, BrowsableAPIRenderer

from rest_framework.response import Response
# model
from apps.department.models import Department, DepartMember
# serialier
from apps.department.serializers import DepartmentSerializer, DepartMemberDetailSerializer
# permission
from apps.department.permissions import IsSelfManagerDoDepOrReadOnly

from apps.snippets.serializers import UserSerializer
# request typing
from rest_framework.request import Request


# Create your views here.


@api_view(['GET'])
def create_dep(request):
    created_dep = Department.objects.create(name='英语社', description='不值得加入的社团');

    dict = {
        'name': created_dep.name,
        'des': created_dep.description,
        'len': Department.objects.all().__len__()
    }
    return Response(dict)


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


# 使用方法，不知道怎么享受到快速调试POST,PUT的表单
# @api_view(['GET', 'POST']t)
# @renderer_classes([JSONRenderer, BrowsableAPIRenderer])
# def depart_memberlist(request: Request, pk):
#     if request.method == 'GET':
#         queryset = DepartMember.objects.filter(department_id=pk)
#         # 创建分页器实例
#         paginator = PageNumberPagination()
#
#         # 对查询集进行分页
#         page = paginator.paginate_queryset(queryset, request)
#
#         # 如果有分页结果，序列化并返回分页响应
#         if page is not None:
#             serializer = DepartMemberDetailSerializer(page, many=True)
#             return paginator.get_paginated_response(serializer.data)
#         # 如果没有分页结果（可能查询集为空），直接返回序列化结果
#         serializer = DepartMemberDetailSerializer(queryset, many=True)
#         return Response(serializer.data)
#
#     elif request.method == 'POST':
#         serializer = DepartMemberDetailSerializer(data=request.data)
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data, status=status.HTTP_201_CREATED)
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

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
    serializer_class = DepartMemberDetailSerializer
    # permission_classes = [permissions.IsAdminUser]

    def get_permissions(self):
        # if self.action == 'list':
        #     self.permission_classes = [permissions.AllowAny]
        return super().get_permissions()

    def filter_queryset(self, queryset):
        dep_id = self.kwargs.get('dep_id')
        if dep_id:
            return queryset.filter(department_id=dep_id)
        return queryset

    @action(detail=False, methods=['GET'], permission_classes=[permissions.IsAuthenticated],url_path='custom-path')
    def custom_list(self, request,**kwargs):
        # Custom list logic here
        return Response({"message": "Custom list action"})


    def list(self, request:Request, *args, **kwargs):
        return super().list(request, *args, **kwargs)


    def create(self, request, *args, **kwargs):
        return super().create(request, *args, **kwargs)

    def retrieve(self, request, *args, **kwargs):
        return super().retrieve(request, *args, **kwargs)

    def partial_update(self, request, *args, **kwargs):
        return super().partial_update(request, *args, **kwargs)

    def update(self, request, *args, **kwargs):
        return super().update(request, *args, **kwargs)

    def destroy(self, request, *args, **kwargs):
        return super().destroy(request, *args, **kwargs)

    def perform_create(self, serializer):
        department_id = self.kwargs.get('dep_id')
        # 获取 Department 实例
        department = Department.objects.get(pk=department_id)
        serializer.save(department=department)
