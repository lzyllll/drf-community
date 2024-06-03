from django.contrib import admin

from apps import snippets
from apps.department.models import Department,DepartMember
# Register your models here.
admin.site.register(snippets.models.Snippet)
admin.site.register(Department)
admin.site.register(DepartMember)

