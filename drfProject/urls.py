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
from django.urls import path, include, re_path
from rest_framework.authtoken.views import obtain_auth_token
from rest_framework.routers import DefaultRouter
from rest_framework.urlpatterns import format_suffix_patterns
from drf_yasg.views import get_schema_view
from drf_yasg import openapi

from apps.snippets import views
from apps.department.views import DepartmentViewSet,DepartMemberViewSet,DepartmentRequestViewSet,AsyncView
from apps.activity.views import ActivityViewSet,ActivityRequestViewSet
#使用viewset,DepartRouter
DepartRouter = DefaultRouter()
DepartRouter.register(r'department', DepartmentViewSet, basename='department')
DepartRouter.register(r'department_members',DepartMemberViewSet,basename='department_members')
DepartRouter.register(r'department_requests',DepartmentRequestViewSet,basename='department_requests')
DepartRouter.register(r'activity',ActivityViewSet,basename='activity')
DepartRouter.register(r'activity_requests',ActivityRequestViewSet,basename='activity_requests')
DepartRouter.register(r'snippets', views.SnippetViewSet, basename='snippet')


schema_view = get_schema_view(
    openapi.Info(
        title="API接口文档平台",  # 必传
        default_version='v1',  # 必传
        description="这是一个美轮美奂的接口文档",
        terms_of_service="http://api.xiaogongjin.site",
        contact=openapi.Contact(email="360664741@qq.com"),
        license=openapi.License(name="My License"),
    ),
    public=True,
    # permission_classes=(permissions.AllowAny,), # 权限类
)


urlpatterns = [
    path('async/',AsyncView.as_view()),
    #其他
    path('api-auth/', include('rest_framework.urls')),
    path("admin/", admin.site.urls),
    path('api/login/', obtain_auth_token, name='api-login'),
    #接口文档
    re_path(r'^swagger(?P<format>\.json|\.yaml)$',
            schema_view.without_ui(cache_timeout=0), name='schema-json'),
    path('swagger/', schema_view.with_ui('swagger', cache_timeout=0),
         name='schema-swagger-ui'),
    path('redoc/', schema_view.with_ui('redoc', cache_timeout=0), name='schemaredoc'),
    #查询用户
    path('users/<int:pk>/', views.UserDetail.as_view()),
    path('users/', views.UserList.as_view()),

    #下载文件
    path('file/<int:pk>/', views.download_file),
    path('file/', views.show_files),
    path('file/upload/', views.ExampleView.as_view()),
    path('image/<str:title>', views.show_image),
    #测试缓存
    path('view/', views.my_view, name='view'),
    path('refresh/', views.refresh),

    #depart的viewset
    path('', include(DepartRouter.urls)),

]

# urlpatterns = format_suffix_patterns(urlpatterns)
