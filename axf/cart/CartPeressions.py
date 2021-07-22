from rest_framework.permissions import BasePermission

from user.models import AxfUser


class CartPermission(BasePermission):

    def has_permission(self, request, view):
        # 登录用户返回true
        return isinstance(request.user, AxfUser)