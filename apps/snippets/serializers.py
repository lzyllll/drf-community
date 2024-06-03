from django.contrib.auth.models import User
from rest_framework import serializers

from apps.snippets.models import Snippet


class UserSerializer(serializers.ModelSerializer):

    # snippets = serializers.PrimaryKeyRelatedField(many=True, queryset=Snippet.objects.all())
    # snippets = serializers.SlugRelatedField(many=True, read_only=True, slug_field='title')
    snippets = serializers.StringRelatedField(many=True, read_only=True)
    class Meta:
        model = User
        fields = ['id', 'username', 'snippets']


class SnippetSerializer(serializers.ModelSerializer):

    class Meta:
        model = Snippet
        owner = serializers.ReadOnlyField(source='owner.username')
        fields = ['id', 'title', 'code', 'linenos', 'language', 'style','owner']


    def create(self, validated_data):
        return super().create(validated_data)

