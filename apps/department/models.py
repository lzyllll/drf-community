from django.db import models

# Create your models here.
class Department(models.Model):
    name = models.CharField(max_length=20,unique=True)
    description = models.CharField(max_length=300)
    created = models.DateTimeField(auto_now_add=True)
    head_user = models.ForeignKey('auth.User', related_name='department', on_delete=models.CASCADE)

    class Meta:
        ordering = ['created']

    def __str__(self):
        return self.name

class DepartMember(models.Model):
    user = models.ForeignKey('auth.User', on_delete=models.CASCADE)
    department = models.ForeignKey('Department', on_delete=models.CASCADE)
    joined = models.DateField(auto_now_add=True)

    class Meta:
        ordering = ['joined']
        constraints = [
            models.UniqueConstraint(fields=['user_id', 'department_id'], name='unique_user_department')
        ]