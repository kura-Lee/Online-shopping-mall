from datetime import datetime

from django.shortcuts import render
from rest_framework import status
from rest_framework.generics import ListCreateAPIView
from rest_framework.response import Response

from cart.CartAuthentication import CartAuthtication
from cart.CartPeressions import CartPermission
from cart.models import AxfCart
from order.models import AxfOrder, AxfOrdergoods
from order.orderFilter import OrderFilter
from order.orderSerializers import OrderSerializer
from axf import settings

class OrderListCreateView(ListCreateAPIView):
    """
    get:使用list方法查询出数据
    post:使用create方法保存数据
    """
    queryset = AxfOrder.objects.all()
    serializer_class = OrderSerializer
    authentication_classes = (CartAuthtication,)
    permission_classes = (CartPermission,)
    filter_class = OrderFilter
    def create(self, request, *args, **kwargs):
        uid = request.user.id
        user_carts = AxfCart.objects.filter(c_user_id=uid).filter(c_is_select=1)
        if user_carts.exists():
            data = {'o_price': self.order_price(user_carts), 'o_time': datetime.now(), 'o_status':settings.ORDER_STATUS_NOT_PAY, 'o_user': request.user}
            # print(date)
            # serializer = self.get_serializer(data=date)
            # print(serializer)
            # if serializer.is_valid():
            #     self.perform_create(serializer)
            order = AxfOrder.objects.create(**data)
            # print(order)
            self.add_to_ordergoods(user_carts, order)
            return Response({
                'code': 200,
                'msg': '请求成功',
                'data': {'order_id': order.id}
            })

        print('错误')
        return Response({
            'code':104,
            'msg': '请求错误'
            })


    def list(self, request, *args, **kwargs):
        queryset = self.queryset.filter(o_user=request.user)
        queryset = self.filter_queryset(self.get_queryset())
        serializer = self.get_serializer(queryset, many=True)
        print(serializer.data)
        return Response({'code': 200, 'msg': '请求成功', 'data': serializer.data})


    def order_price(self, user_carts):
        """传入所选商品集，计算所选商品集的总价"""
        price = 0
        for cart in user_carts:
            price += cart.c_goods.price * cart.c_goods_num
        return price
    def add_to_ordergoods(self, user_carts, user_order):
        query = []
        for cart in user_carts:
            # 实例化订单商品对象
            order_goods = AxfOrdergoods()
            order_goods.o_goods_num = cart.c_goods_num
            order_goods.o_goods = cart.c_goods
            order_goods.o_order = user_order
            query.append(order_goods)
        AxfOrdergoods.objects.bulk_create(query)

