from django.contrib.auth.models import User
from django.db import models


# Create your models here.
class CampusActivity(models.Model):
    name = models.CharField(max_length=50, unique=True)  # 将最大长度增加到50
    description = models.CharField(max_length=300)

    begin_date = models.DateTimeField(auto_now_add=True)
    end_date = models.DateTimeField(null=True)

    sponsors = models.ManyToManyField(User, related_name='sponsor_activity')
    participants = models.ManyToManyField(User, related_name='joined_activity')

    class Meta:
        ordering = ['begin_date']

    def __str__(self):
        return self.name


class CampusActivityRequest(models.Model):
    PENDING = 'P'
    APPROVED = 'A'
    REJECTED = 'R'
    REQUEST_STATUS_CHOICES = [
        (PENDING, 'Pending'),
        (APPROVED, 'Approved'),
        (REJECTED, 'Rejected'),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='activity_requests')
    activity = models.ForeignKey(CampusActivity, on_delete=models.CASCADE, related_name='requests')
    status = models.CharField(max_length=1, choices=REQUEST_STATUS_CHOICES, default=PENDING)
    created = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['created']
        unique_together = ['user', 'activity']  # 确保每个用户对每个社团只有一个请求

    def __str__(self):
        return f"{self.user.username} 申请 {self. activity.name} 的状态为 {self.status}"
