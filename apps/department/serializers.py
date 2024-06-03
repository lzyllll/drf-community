from rest_framework import serializers
from .models import Department, DepartMember, DepartmentRequest
from django.contrib.auth.models import User


class DepartmentSerializer(serializers.ModelSerializer):
    head_user = serializers.StringRelatedField(read_only=True)
    head_user_id = serializers.PrimaryKeyRelatedField(queryset=User.objects.all(), source='head_user', write_only=True)
    members = serializers.StringRelatedField(many=True, read_only=True)
    member_ids = serializers.PrimaryKeyRelatedField(many=True, queryset=User.objects.all(), source='members',
                                                    write_only=True)

    class Meta:
        model = Department
        fields = ['id', 'name', 'description', 'created', 'head_user', 'head_user_id', 'members', 'member_ids']


class DepartMemberSerializer(serializers.ModelSerializer):

    user = serializers.StringRelatedField(read_only=True)
    user_id = serializers.PrimaryKeyRelatedField(queryset=User.objects.all(), source='user', write_only=True)
    department = serializers.StringRelatedField(read_only=True)
    department_id = serializers.PrimaryKeyRelatedField(queryset=Department.objects.all(), source='department',
                                                       write_only=True)

    class Meta:
        model = DepartMember
        fields = ['id', 'user', 'user_id', 'department', 'department_id', 'joined']


class DepartmentRequestSerializer(serializers.ModelSerializer):
    user = serializers.StringRelatedField()

    class Meta:
        model = DepartmentRequest
        fields = ['id', 'user', 'department', 'status','created']
        read_only_fields = ['user','status']

    def validate(self, data):
        user = self.context['request'].user
        department = data['department']
        if self.instance:
            # 更新时的操作，排除自己
            existing_requests = DepartmentRequest.objects.filter(user=user, department=department).exclude(
                pk=self.instance.pk)
            if existing_requests.exists():
                raise serializers.ValidationError("每个用户对每个社团只能有一个请求。")
        else:
            # 添加时的操作
            if DepartmentRequest.objects.filter(user=user, department=department).exists():
                raise serializers.ValidationError("每个用户对每个社团只能有一个请求。")
        return data