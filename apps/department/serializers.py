from rest_framework import serializers
from .models import Department, DepartMember, DepartmentRequest
from django.contrib.auth.models import User


class DepartmentSerializer(serializers.ModelSerializer):
    head_user = serializers.StringRelatedField(read_only=True)
    head_user_id = serializers.PrimaryKeyRelatedField(queryset=User.objects.all(), source='head_user', write_only=True)
    # 方法1 设置slug，因为auth.user.username不允许重复，但是通过username来添加的而不是id
    # members = serializers.SlugRelatedField(
    #     many=True,
    #     slug_field='username',
    #     queryset=User.objects.all()
    # )

    # 方法2，设置一个可读string,再设置一个可写id
    members = serializers.StringRelatedField(many=True, read_only=True)
    member_ids = serializers.PrimaryKeyRelatedField(many=True, queryset=User.objects.all(), source='members',
                                                    write_only=True)

    class Meta:
        model = Department
        fields = ['id', 'name', 'description', 'created', 'head_user', 'head_user_id', 'members', 'member_ids']


class ManagerDepartmentSerializer(DepartmentSerializer):
    class Meta(DepartmentSerializer.Meta):
        fields = ['id', 'name', 'description', 'created', 'head_user', 'members']


class DepartMemberSerializer(serializers.ModelSerializer):
    user = serializers.StringRelatedField(read_only=True)
    user_id = serializers.PrimaryKeyRelatedField(queryset=User.objects.all(), source='user', write_only=True)
    department = serializers.StringRelatedField(read_only=True)
    department_id = serializers.PrimaryKeyRelatedField(queryset=Department.objects.all(), source='department',
                                                       write_only=True)

    class Meta:
        model = DepartMember
        fields = ['id', 'user', 'user_id', 'department', 'department_id', 'joined']

    def validate(self, data):
        user = data.get('user')
        department = data.get('department')

        # 减少代码量，未简化的如下
        if DepartMember.objects.filter(user=user, department=department).exclude(
                id=self.instance.id if self.instance else None).exists():
            raise serializers.ValidationError("一个人不可能同时加入社团两次.")

        return data


class DepartmentRequestSerializer(serializers.ModelSerializer):
    user = serializers.StringRelatedField()

    class Meta:
        model = DepartmentRequest
        fields = ['id', 'user', 'department', 'status', 'created']
        read_only_fields = ['user', 'status']

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
