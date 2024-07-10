from django.urls import include, path
from rest_framework.routers import SimpleRouter
from apps.snippets.views import SnippetViewSet

SnippetRouter = SimpleRouter()
SnippetRouter.register(r'snippets', SnippetViewSet, basename='snippet')
urlpatterns =[
    path('', include(SnippetRouter.urls)),
]