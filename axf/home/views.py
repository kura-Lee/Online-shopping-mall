from django.shortcuts import render
from rest_framework.generics import GenericAPIView
from rest_framework.response import Response

from home.homeSerializers import WheelSerializer, NavSerializer, ShopSerializer, MainShowSerializer, MustbuySerializer
from home.models import AxfWheel, AxfNav, AxfShop, AxfMainshow, AxfMustbuy


class HomeListView(GenericAPIView):
    """
    get:获取首页数据
    """
    serializer_class = WheelSerializer
    queryset = AxfWheel.objects.all()
    def get(self, request):
        # 查询数据
        nav_queryset = AxfNav.objects.all()
        shop_queryset = AxfShop.objects.all()
        mainshow_querset = AxfMainshow.objects.all()
        mustbuy_querset = AxfMustbuy.objects.all()
        # 序列化
        wheel_data = self.serializer_class(self.get_queryset(), many=True)
        nav_data = NavSerializer(nav_queryset, many=True)
        shop_data = ShopSerializer(shop_queryset, many=True)
        mainshow_data = MainShowSerializer(mainshow_querset, many=True)
        mustbuy_data = MustbuySerializer(mustbuy_querset, many=True)
        # 返回数据
        return Response({
            'code': 200,
            'msg': '请求成功',
            'data': {
                'main_wheels': wheel_data.data,
                'main_navs': nav_data.data,
                'main_mustbuys': mustbuy_data.data,
                'main_shops': shop_data.data,
                'main_shows': mainshow_data.data
            },
        })

