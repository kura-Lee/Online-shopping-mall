import re

from django.shortcuts import render
from rest_framework.generics import GenericAPIView, ListAPIView
from rest_framework.response import Response
from rest_framework.views import APIView

from axf import settings
from market.goodfilter import GoodsFilter
from market.marketserializers import GoodTypeSerializer, GoodsSerializer
from market.models import AxfGoodtype, AxfGoods


class GoodTypeListView(GenericAPIView):
    """
    get:获取商品类型
    """
    queryset = AxfGoodtype.objects.all()
    serializer_class = GoodTypeSerializer
    def get(self, request):
        goodtype_data = GoodTypeSerializer(self.get_queryset(), many=True)
        return Response({
            'code': 200,
            'msg': '请求成功',
            'data': goodtype_data.data
        })

# class GoodTypeListView(ListAPIView):
#     queryset = AxfGoodtype.objects.all()
#     serializer_class = GoodTypeSerializer
#     # def list(self, request, *args, **kwargs):
#     #     goodtype_res = super(GoodTypeListView, self).list(request, *args, **kwargs)
#     #     print(goodtype_res)
#     #     return Response({
#     #                 'code': 200,
#     #                 'msg': '请求成功',
#     #                 'data': goodtype_res
#     #             })


# class GoodsListView(APIView):
#     """
#     get:获取商品列表
#     """
#     def get(self, reuqest, *args, **kwargs):
#         # 获取参数
#         params = reuqest.query_params
#         typeid = params.get('typeid', 0)
#         childid = int(params.get('childcid', 0))
#         ruleid = int(params.get('order_rule', 0))
#         # 商品列表
#         goods_list = AxfGoods.objects.filter(categoryid=int(typeid))
#         # 过滤子类商品
#         if childid > 0:
#             goods_list = goods_list.filter(childcid=childid)
#         #结果排序
#         if ruleid == 1:
#             goods_list = goods_list.order_by("price")
#         elif ruleid == 2:
#             goods_list = goods_list.order_by("-price")
#         elif ruleid == 3:
#             goods_list = goods_list.order_by("productnum")
#         elif ruleid == 4:
#             goods_list = goods_list.order_by("-productnum")
#         # 序列化
#         goods_data = GoodsSerializer(goods_list, many=True)
#
#         # 商品分类的子类列表
#         goodtype = AxfGoodtype.objects.filter(typeid=int(typeid)).first()
#         childtypenames = goodtype.childtypenames
#         #全部分类:0#个人护理:103576#纸品:103578#日常用品:103580#家居清洁:103577
#         childtypenames = [re.split(":", everytype) for everytype in re.split("#", childtypenames)]
#         childtypenames = [ dict([['child_name', eve[0]], ['child_value', eve[1]]]) for eve in childtypenames]
#         #[{'child_name': '全部分类', 'child_value': '0'}...]
#
#         print(childtypenames)
#         return Response({
#             'code': 200,
#             'msg': '查询成功',
#             'data': {
#                 'goods_list': goods_data.data,
#                 'order_rule_list': settings.ORDER_RULE_LIST,
#                 'foodtype_childname_list': childtypenames
#             }
#         })

class GoodsListView(ListAPIView):
    queryset = AxfGoods.objects.all()
    serializer_class = GoodsSerializer
    filter_class = GoodsFilter


    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())
        serializer = self.get_serializer(queryset, many=True)

        #商品分类的子类列表
        typeid = request.query_params.get('typeid', 0)
        goodtype = AxfGoodtype.objects.filter(typeid=int(typeid)).first()
        childtypenames = goodtype.childtypenames
        #全部分类:0#个人护理:103576#纸品:103578#日常用品:103580#家居清洁:103577
        childtypenames = [re.split(":", everytype) for everytype in re.split("#", childtypenames)]
        childtypenames = [ dict([['child_name', eve[0]], ['child_value', eve[1]]]) for eve in childtypenames]
        #[{'child_name': '全部分类', 'child_value': '0'}...]
        return Response({
                    'code': 200,
                    'msg': '查询成功',
                    'data': {
                        'goods_list': serializer.data,
                        'order_rule_list': settings.ORDER_RULE_LIST,
                        'foodtype_childname_list': childtypenames
                    }
        })