from django.urls import include, path
from rest_framework.routers import SimpleRouter

from apps.department.views import DepartmentViewSet, DepartMemberViewSet, DepartmentRequestViewSet
from apps.snippets.views import SnippetViewSet

DepartRouter = SimpleRouter()
DepartRouter.register(r'department', DepartmentViewSet, basename='department')
DepartRouter.register(r'department_members',DepartMemberViewSet,basename='department_members')
DepartRouter.register(r'department_requests',DepartmentRequestViewSet,basename='department_requests')
urlpatterns =[
    path('', include(DepartRouter.urls)),
]