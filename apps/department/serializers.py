from django.contrib.auth.models import User
from rest_framework import serializers

from apps.department.models import Department, DepartMember
class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email']

class DepartmentSerializer(serializers.ModelSerializer):

    class Meta:
        model = Department
        fields = '__all__'


class DepartMemberSerializer(serializers.ModelSerializer):
    user = UserSerializer()
    class Meta:
        model = DepartMember
        exclude = ['department','id']

class DepartMemberDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = DepartMember
        fields = '__all__'
