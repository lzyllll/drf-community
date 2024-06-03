from django.core.management.base import BaseCommand
from django.contrib.auth.models import User, Group


class Command(BaseCommand):
    help = 'Ad_group'

    def handle(self, *args, **kwargs):
        try:
            # 获取第一个用户
            first_user = User.objects.first()
            if not first_user:
                self.stdout.write(self.style.ERROR('No users found'))
                return

            # 获取或创建 "manager" 组
            manager_group, created = Group.objects.get_or_create(name='manager')

            # 将用户添加到组
            first_user.groups.add(manager_group)
            self.stdout.write(self.style.SUCCESS(f'Successfully added {first_user.username} to the manager group'))
        except Exception as e:
            self.stdout.write(self.style.ERROR(f'Error: {str(e)}'))


