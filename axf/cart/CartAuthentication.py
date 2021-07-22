from rest_framework.authentication import BaseAuthentication
from rest_framework.exceptions import APIException, AuthenticationFailed
from rest_framework.response import Response

from user.models import AxfUser
from user.token import token_confirm


class CartAuthtication(BaseAuthentication):
    def authenticate(self, request):
        # 获取token
        token = request.data.get('token') or request.query_params.get('token')
        try:
            uid = token_confirm.confirm_validate_token(token, expiration=None)
        except Exception as e:
            #print(e)
            # return Response({
            #     'code': 1006,
            #     'msg': 'token失效',
            #     'data': {}
            # })
            raise AuthenticationFailed("token失效")
            # return
        try:
            user = AxfUser.objects.get(pk=uid)
        except Exception as e:
            # print(e)
            # return Response({
            #     'code': 1006,
            #     'msg': '用户不存在',
            #     'data': {}
            # })
            raise AuthenticationFailed("用户不存在")
            # return
        # 验证成功
        return user, token