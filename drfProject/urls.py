"""
URL configuration for drfProject project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from rest_framework.authtoken.views import obtain_auth_token
from rest_framework.routers import DefaultRouter
from rest_framework.urlpatterns import format_suffix_patterns

from apps.snippets import views
from apps.department.views import DepartmentViewSet,DepartMemberViewSet,create_dep

#使用viewset,DepartRouter
DepartRouter = DefaultRouter()
DepartRouter.register(r'department', DepartmentViewSet, basename='department')
DepartRouter.register(r'department/(?P<dep_id>\d+)/members',DepartMemberViewSet,basename='member')


urlpatterns = [
    path('api-auth/', include('rest_framework.urls')),
    path("admin/", admin.site.urls),
    path('api/login/', obtain_auth_token, name='api-login'),
    #查询用户
    path('users/<int:pk>/', views.UserDetail.as_view()),
    path('users/', views.UserList.as_view()),
    #查询代码片段
    path('snippets/', views.SnippetList.as_view()),
    path('snippets/<int:pk>/', views.SnippetDetail.as_view()),
    #下载文件
    path('file/<int:pk>/', views.download_file),
    path('file/', views.show_files),
    path('file/upload/', views.ExampleView.as_view()),
    path('image/<str:title>', views.show_image),
    #测试缓存
    path('view/', views.my_view, name='view'),
    path('refresh/', views.refresh),
    path('dep/cre/',create_dep),

    #depart的viewset
    path('', include(DepartRouter.urls)),

]

# urlpatterns = format_suffix_patterns(urlpatterns)
