import io
import os

import matplotlib
from django.conf.global_settings import MEDIA_ROOT
from django.core.cache import cache
from django.core.files.uploadedfile import InMemoryUploadedFile
from django.views.decorators.cache import cache_page
from matplotlib import pyplot as plt

from django.contrib.contenttypes.models import ContentType
from django.contrib.auth.models import User, Permission
from django.http import JsonResponse, FileResponse
from django.shortcuts import get_object_or_404
from pandas import DataFrame

from rest_framework import generics, permissions, mixins, viewsets, renderers, status, serializers
from rest_framework.decorators import api_view, parser_classes, action, permission_classes
from rest_framework.parsers import FileUploadParser, JSONParser, MultiPartParser
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.serializers import ModelSerializer
from rest_framework.views import APIView
from apps.snippets.models import Snippet
from apps.snippets.permissions import IsOwnerOrReadOnly
from apps.snippets.serializers import UserSerializer, SnippetSerializer
import pandas as pd


class UserList(generics.ListAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    parser_classes = [JSONParser, MultiPartParser]

    def filter_queryset(self, queryset):
        queryset = queryset.order_by('id')
        return queryset

    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)

    # 无法使用，因为没有没有继承viewset


class UserDetail(generics.RetrieveAPIView):
    queryset = User.objects.all()

    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]


class SnippetViewSet(viewsets.ModelViewSet):
    """
    This ViewSet automatically provides `list`, `create`, `retrieve`,
    `update` and `destroy` actions.

    Additionally we also provide an extra `highlight` action.
    """
    queryset = Snippet.objects.all()
    serializer_class = SnippetSerializer
    permission_classes = [IsOwnerOrReadOnly]
    # queryset = Department.objects.all()
    # serializer_class = DepartmentSerializer
    # permission_classes = [DepartmentPermissionControl]

    # @action(detail=True, renderer_classes=[renderers.StaticHTMLRenderer])
    # def highlight(self, request, *args, **kwargs):
    #     snippet = self.get_object()
    #     return Response(snippet.highlighted)

    # def perform_create(self, serializer):
    #     serializer.save(owner=self.request.user)


def add_permissons(request):
    user = get_object_or_404(User, pk=2)
    # any permission check will cache the current set of permissions
    content_type = ContentType.objects.get_for_model(Snippet)
    # all_permission = Permission.objects.filter(content_type=content_type)
    permission = Permission.objects.get(
        name='self-permission',
        codename="change_group",
        content_type=content_type,
    )

    user.user_permissions.add(permission)
    user.save()

    print('用户权限有：')
    # applabel + . + codename

    print(user.has_perm('snippets.change_group'))


@api_view(['GET'])
def show_image(request, title):
    # 不需要gui页面，只生成图片
    matplotlib.use('Agg')

    x = [1, 2, 3, 4, 5]
    y = [2, 3, 5, 7, 12]

    plt.plot(x, y)
    plt.xlabel('x')
    plt.ylabel('y')
    plt.title(title)

    buffer = io.BytesIO()
    plt.savefig(buffer, format='png')
    buffer.seek(0)
    plt.close()

    return FileResponse(buffer, content_type='image/png')


class ExampleView(APIView):
    """
    A view that can accept POST requests with JSON content.
    """
    parser_classes = [JSONParser, MultiPartParser]

    def post(self, request, format=None):
        return Response({'received data': request.data})



@api_view(['POST'])
@permission_classes([permissions.IsAdminUser])
def load_user_by_xlsx(request):
    file: InMemoryUploadedFile = request.data.get('file')
    result = []
    try:
        df = pd.read_excel(file)
    except:
        return Response({'msg': '无法读取该文件，请查看文件类型是否为xlsx'}, status.HTTP_400_BAD_REQUEST)

    try:
        user = df['username'].tolist()
        pwd = df['password'].tolist()
    except:
        return Response({'msg': '请检查是否有username和password的字段'}, status.HTTP_400_BAD_REQUEST)

    for user, pwd in zip(user, pwd):
        if not User.objects.filter(username=user).exists():
            User.objects.create_user(username=user, password=pwd)
        else:
            result.append(
                {
                    'user': user,
                    'msg': '已存在该用户，无法添加'
                }
            )
    if result:
        return Response({'result': result})
    else:
        return Response({'msg': 'success'})




@api_view(['GET'])
# todo
def download_file(request, pk):
    print(pk)
    url = r"C:\Users\lzy\Desktop\mytestc"
    file_path = os.listdir(url)[pk]
    file_path = os.path.join(url, file_path)
    return FileResponse(open(file_path, "rb"), as_attachment=True)


# todo
@api_view(['GET'])
def show_files(request):
    dir_path = r"C:\Users\lzy\Desktop\mytestc"
    file_path = os.listdir(dir_path)
    res_dict = dict(zip(range(len(file_path)), file_path))
    response = Response(res_dict)
    return response


@api_view(['GET'])
@cache_page(60 * 15)
def my_view(request):
    '''
    展现所有的代码片段
    '''
    # if not cache.get('a'):
    #     cache.set('a',ser.data)
    # else :
    #     return cache.get('a')

    snippets = Snippet.objects.all()
    ser = SnippetSerializer(snippets, many=True)
    return Response(ser.data)


def refresh(request):
    '''
    删除第一个代码片段
    '''
    snippet = Snippet.objects.first()
    ser = SnippetSerializer(snippet)

    snippet.delete()
    cache.clear()

    return JsonResponse({'state': 'success', 'snippet': ser.data})
