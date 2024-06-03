from django.db import models
from django.contrib.auth.models import User


class Department(models.Model):
    name = models.CharField(max_length=50, unique=True)  # 将最大长度增加到50
    description = models.CharField(max_length=300)
    created = models.DateTimeField(auto_now_add=True)
    head_user = models.ForeignKey(User, related_name='header_department', on_delete=models.CASCADE)

    members = models.ManyToManyField(User, related_name='joined_departments', through='DepartMember')

    class Meta:
        ordering = ['created']

    def __str__(self):
        return self.name


class DepartMember(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    department = models.ForeignKey(Department, on_delete=models.CASCADE)
    joined = models.DateField(auto_now_add=True)

    class Meta:
        ordering = ['joined']
        unique_together = ['user', 'department']  # 使用unique_together来确保user和department组合的唯一性


class DepartmentRequest(models.Model):
    PENDING = 'P'
    APPROVED = 'A'
    REJECTED = 'R'
    REQUEST_STATUS_CHOICES = [
        (PENDING, 'Pending'),
        (APPROVED, 'Approved'),
        (REJECTED, 'Rejected'),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='department_requests')
    department = models.ForeignKey(Department, on_delete=models.CASCADE, related_name='requests')
    status = models.CharField(max_length=1, choices=REQUEST_STATUS_CHOICES, default=PENDING)
    created = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['created']
        unique_together = ['user', 'department']  # 确保每个用户对每个社团只有一个请求

    def __str__(self):
        return f"{self.user.username} - {self.department.name} - {self.get_status_display()}"