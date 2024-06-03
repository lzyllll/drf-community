import io
import os

import matplotlib
from django.core.cache import cache
from matplotlib import pyplot as plt

from django.contrib.contenttypes.models import ContentType
from django.contrib.auth.models import User, Permission
from django.http import JsonResponse, FileResponse
from django.shortcuts import get_object_or_404

from rest_framework import generics, permissions, mixins
from rest_framework.decorators import api_view, parser_classes
from rest_framework.parsers import FileUploadParser, JSONParser, MultiPartParser
from rest_framework.response import Response
from rest_framework.views import APIView

from apps.snippets.models import Snippet
from apps.snippets.permissions import IsOwnerOrReadOnly
from apps.snippets.serializers import UserSerializer, SnippetSerializer


class UserList(generics.ListAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def filter_queryset(self, queryset):
        queryset = queryset.order_by('id')
        return queryset

    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)

class UserDetail(generics.RetrieveAPIView):
    queryset = User.objects.all()

    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]


class SnippetDetail(mixins.RetrieveModelMixin,
                    mixins.UpdateModelMixin,
                    mixins.DestroyModelMixin,
                    generics.GenericAPIView):
    queryset = Snippet.objects.all()
    serializer_class = SnippetSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly,IsOwnerOrReadOnly]


    def get(self, request, *args, **kwargs):

        return self.retrieve(request, *args, **kwargs)


    def put(self, request, *args, **kwargs):
        return self.update(request, *args, **kwargs)

    def delete(self, request, *args, **kwargs):
        return self.destroy(request, *args, **kwargs)

    def post(self,request):
        return JsonResponse('a')


class SnippetList(mixins.ListModelMixin,
                  mixins.CreateModelMixin,
                  generics.GenericAPIView):
    # 相当于是配置，不要动,名称也是固定的
    queryset = Snippet.objects.all()
    serializer_class = SnippetSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    # @method_decorator(cache_page(60 * 15))
    def get(self, request, *args, **kwargs):

        return self.list(request, *args, **kwargs)


    def post(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)

    #混合类的方法会调用
    #保存snippet时，设置owner属性
    def perform_create(self, serializer):
        print("当前用户是：", self.request.user)
        serializer.save(owner=self.request.user)


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
def show_image(request,title):
    #不需要gui页面，只生成图片
    matplotlib.use('Agg')

    x = [1, 2, 3, 4, 5]
    y = [2, 3, 5, 7, 12]

    plt.plot(x, y)
    plt.xlabel('x')
    plt.ylabel('y')
    plt.title(title)

    # 将图表临时保存到内存
    buffer = io.BytesIO()
    plt.savefig(buffer, format='png')
    buffer.seek(0)
    plt.close()

    # 构建响应
    return FileResponse(buffer, content_type='image/png')


class ExampleView(APIView):
    """
    A view that can accept POST requests with JSON content.
    """
    parser_classes = [JSONParser,MultiPartParser]

    def post(self, request, format=None):
        return Response({'received data': request.data})

@api_view(['GET'])
# todo
def download_file(request,pk):
    print(pk)
    url = r"C:\Users\lzy\Desktop\mytestc"
    file_path = os.listdir(url)[pk]
    file_path = os.path.join(url,file_path)
    return FileResponse(open(file_path, "rb"),as_attachment=True)
# todo
@api_view(['GET'])
def show_files(request):
    dir_path = r"C:\Users\lzy\Desktop\mytestc"
    file_path = os.listdir(dir_path)
    res_dict = dict(zip(range(len(file_path)),file_path))
    response = Response(res_dict)
    return response



@api_view(['GET'])
# @cache_page(60 * 15)
def my_view(request):
    '''
    展现所有的代码片段
    '''
    temp = cache.get('a')
    if temp:
        return Response(temp)
    else:
        snippets = Snippet.objects.all()
        ser = SnippetSerializer(snippets,many=True)
        cache.set('a',ser.data)
        return Response(ser.data)


def refresh(request):
    '''
    删除第一个代码片段
    '''
    snippet = Snippet.objects.first()
    ser = SnippetSerializer(snippet)

    snippet.delete()
    cache.clear()

    return JsonResponse({'state':'success','snippet':ser.data})


