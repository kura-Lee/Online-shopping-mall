from django.shortcuts import render
from rest_framework.generics import GenericAPIView, CreateAPIView
from rest_framework.response import Response
from user.token import token_confirm
from user.userSerializers import UserSerializer, UserRegisterSerializer, UerLoginSerializer

from user.models import AxfUser


class UserShowView(GenericAPIView):
    queryset = AxfUser.objects.all()
    serializer_class = UserSerializer

    def get(self, request):
        """
        使用token用户认证
        """
        # 获取token值
        token = request.query_params.get('token')
        try:
            uid = token_confirm.confirm_validate_token(token, expiration=None)
        except Exception as e:
            print(e)
            return Response({
                'code': 107,
                'msg': 'token失效，请登录',
                'data':{}
            })
        #获取到了uid
        try:
            user = AxfUser.objects.get(pk=uid)
        except Exception as e:
            print(e)
            return Response({
                'code': 107,
                'msg': '该用户不存在',
                'data': {}
            })
        #序列化
        serializer = UserSerializer(instance=user)
        return Response({
            'code': 200,
            'msg': '查询成功',
            'data': {'user_info': serializer.data,
                     'orders_not_pay_num': 0,  # 待付款
                     'orders_not_send_num': 0  # 待收货
                    },
        })


class UserLoginView(GenericAPIView):
    queryset = AxfUser.objects.all()
    serializer_class = UerLoginSerializer
    def post(self, request):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            username = serializer.data.get('u_username')
            user = AxfUser.objects.get(u_username=username)
            token = token_confirm.generate_validate_token(user.id)
            return Response({
                'code': 200,
                'msg': '登录成功',
                'data': {
                    'user_id': user.id,
                    'token': token
                }
            })
        else:
            print(serializer.errors)
            # print(list(dict(serializer.errors).values())[0][0])
            return Response({'code': 1004,
                             'msg': list(dict(serializer.errors).values())[0][0],
                             'data': { }
                             })


class UserRegisterView(GenericAPIView):
    queryset = AxfUser.objects.all()
    serializer_class = UserRegisterSerializer

    def post(self, request):
        serializer = UserRegisterSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            return Response({
                'code': 200,
                'msg': '注册成功',
                'data': {'user_id': user.id}
            })
        return Response({
            'code': 105,
            'msg': '注册失败',
            'data': {'info': serializer.errors}
        })

