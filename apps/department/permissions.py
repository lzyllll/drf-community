from rest_framework.permissions import BasePermission, SAFE_METHODS, IsAdminUser

from apps.department.models import Department

'''
判断社团的管理员，是否管理的是本身的社团
'''


def isManager(request, view) -> bool:
    """
    先从url中获取dep_id如果获得不到，再从pk中获取
    作为dep_id
    然后根据dep_id 和 request.user 查询是否为管理员

    # """
    # try:
    #     dep_id = view.kwargs.get('dep_id')
    #     if not dep_id:
    #         dep_id = view.kwargs.get('pk')
    #     Department.objects.get(pk=dep_id, head_user=request.user)
    # except:
    #     return False
    return True


def isAdmin(request) -> bool:
    return bool(request.user and request.user.is_staff)


class IsSelfManagerDoDepOrReadOnly(BasePermission):
    """
    凑合用，灵活性过于差，只能用Dep的权限判断
    """
    def has_permission(self, request, view):
        if isAdmin(request):
            return True
        if request.method in ['POST']:
            return False
        # get等查询，直接就可以
        else:
            return True

    def has_object_permission(self, request, view, obj):
        if isAdmin(request):
            return True
        if request.method in ['PUT']:
            return isManager(request, view)

        elif request.method in ['POST', 'PATCH', 'DELETE']:
            # 判断是否为管理员用户
            return False
            # get等查询，直接就可以
        else:
            return True
