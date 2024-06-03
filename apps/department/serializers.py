from rest_framework import serializers
from .models import Department, DepartMember, DepartmentRequest
from django.contrib.auth.models import User


class DepartmentSerializer(serializers.ModelSerializer):
    head_user = serializers.StringRelatedField()  # Assuming you want to display the head_user's username
    members = serializers.StringRelatedField(many=True)  # Displaying member usernames

    class Meta:
        model = Department
        fields = ['id', 'name', 'description', 'created', 'head_user', 'members']


class DepartMemberSerializer(serializers.ModelSerializer):
    user = serializers.StringRelatedField()
    department = serializers.StringRelatedField()

    class Meta:
        model = DepartMember
        fields = ['id', 'user', 'department', 'joined']


class DepartmentRequestSerializer(serializers.ModelSerializer):
    user = serializers.StringRelatedField()
    department = serializers.StringRelatedField()
    status_display = serializers.CharField(source='get_status_display', read_only=True)

    class Meta:
        model = DepartmentRequest
        fields = ['id', 'user', 'department', 'status', 'status_display', 'created']
