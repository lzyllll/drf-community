from django.urls import include, path
from rest_framework.routers import SimpleRouter

from apps.activity.views import ActivityViewSet, ActivityRequestViewSet
from apps.snippets.views import SnippetViewSet


ActivityRouter = SimpleRouter()
ActivityRouter.register(r'activity',ActivityViewSet,basename='activity')
ActivityRouter.register(r'activity_requests',ActivityRequestViewSet,basename='activity_requests')

urlpatterns =[
    path('', include(ActivityRouter.urls)),
]