from django.shortcuts import render
from rest_framework.exceptions import APIException
from rest_framework.generics import CreateAPIView, ListAPIView, GenericAPIView
from rest_framework.response import Response
from rest_framework.views import APIView

from cart.CartAuthentication import CartAuthtication
from cart.CartPeressions import CartPermission
from cart.cartSerializers import CartAddSerializer, CarSerizlizer
from cart.models import AxfCart
from market.models import AxfGoods
from user.models import AxfUser
from user.token import token_confirm


class AddcartView(CreateAPIView):
    queryset = AxfUser.objects.all()
    serializer_class = CartAddSerializer
    authentication_classes = (CartAuthtication,)
    permission_classes = (CartPermission,)

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            # 商品和token存在
            # # 获取token
            # token = serializer.data.get('token')
            # try:
            #     uid = token_confirm.confirm_validate_token(token, expiration=None)
            # except Exception as e:
            #     print(e)
            #     return Response({
            #         'code': 1006,
            #         'msg': 'token失效',
            #         'data': {}
            #     })
            # try:
            #     user = AxfUser.objects.get(pk=uid)
            # except Exception as e:
            #     print(e)
            #     return Response({
            #         'code': 1006,
            #         'msg': '用户不存在',
            #         'data': {}
            #     })
            uid = request.user.id
            #在购物车找到用户的记录
            carts = AxfCart.objects.filter(c_user_id=uid)
            goodsid = serializer.data.get('goodsid')
            carts = carts.filter(c_goods_id=goodsid)
            if carts.exists():
                cart = carts.first()
                cart.c_goods_num += 1
                cart.save()
            else:
                cart = AxfCart()
                cart.c_goods_num = 1
                cart.c_goods = AxfGoods.objects.get(pk=goodsid)
                cart.c_user = AxfUser.objects.get(pk=uid)
                cart.c_is_select =1
                cart.save()
            return Response({
                'code': 200,
                'msg': '请求成功',
                'data': {'c_goods_num': cart.c_goods_num}
            })
        else:
            return Response({
                'code': 1006,
                'msg': '商品不存在',
                'data': {}
            })


class CartListView(ListAPIView):
    queryset = AxfCart.objects.all()
    serializer_class = CarSerizlizer
    permission_classes = (CartPermission, )
    authentication_classes = (CartAuthtication, )

    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        uid = request.user.id
        queryset = queryset.filter(c_user_id=uid)
        queryset = self.filter_queryset(queryset)
        # print(queryset)

        # 计算已选择的商品总价
        total = 0
        select_all = True
        for rec in queryset:
            if rec.c_is_select == 0:
                select_all = False
            else:
                total += rec.c_goods_num * rec.c_goods.price
        # print("total=",total)
        # 序列化
        serializer = self.get_serializer(queryset, many=True)

        return Response({
            'code': 200,
            'msg': '查询成功',
            'data': {
                'title': '购物车',
                'is_all_select': select_all,
                'total_price': total,
                'carts': serializer.data
            }
        })

    def patch(self, request, id):
        # print('进入patch', id)
        carts = AxfCart.objects.filter(pk=id)
        if carts.exists():
            cart = carts.first()
            if cart.c_is_select:
                cart.c_is_select = 0
            else:
                cart.c_is_select = 1
            cart.save()
            return Response({
                'code': 200,
                'msg': '请求成功',
                'data': {}
            })
        else:
            return Response({
                'code': 107,
                'msg': '请求失败',
                'data': {}
            })


class SubcartView(GenericAPIView):
    queryset = AxfUser.objects.all()
    serializer_class = CartAddSerializer
    authentication_classes = (CartAuthtication,)
    permission_classes = (CartPermission,)

    def post(self, request):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            uid = request.user.id
            goodsid = serializer.data.get('goodsid')
            carts = AxfCart.objects.filter(c_user_id=uid)
            cart = carts.filter(c_goods_id=goodsid).first()
            if cart.c_goods_num == 1:
                cart.delete()
                return Response({
                    'code': 200,
                    'msg': '请求成功',
                    'data': {}
                })
            else:
                cart.c_goods_num -= 1
                cart.save()
                return Response({
                    'code': 200,
                    'msg': '请求成功',
                    'data': {'c_goods_num': cart.c_goods_num}
            })
        else:
            return Response({
                'code': 1006,
                'msg': '商品不存在',
                'data': {}
            })