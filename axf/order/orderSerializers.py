from rest_framework.serializers import Serializer,ModelSerializer

from market.marketserializers import GoodsSerializer
from order.models import AxfOrder, AxfOrdergoods


class OrderSerializer(ModelSerializer):

    class Meta:
        model = AxfOrder
        fields = "__all__"

    def to_representation(self, instance):
        # 调用父类方法获取序列化后的数据
        OrderedDict = super().to_representation(instance)
        #添加我们需要的数据字段
        order_goods = instance.goods.all()
        #序列化
        serializer = OrderGoodsSerializer(order_goods, many=True)
        OrderedDict['order_goods_info'] = serializer.data
        return OrderedDict


class OrderGoodsSerializer(ModelSerializer):
    o_goods = GoodsSerializer()
    class Meta:
        model = AxfOrdergoods
        fields = "__all__"
