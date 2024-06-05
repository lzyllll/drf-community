from django.contrib import admin

from apps import snippets
from apps.department.models import *
from apps.activity.models import *

# Register your models here.
admin.site.register(snippets.models.Snippet)
admin.site.register(Department)
admin.site.register(DepartmentRequest)
admin.site.register(CampusActivity)
admin.site.register(CampusActivityRequest)


admin.site.register(DepartMember)


