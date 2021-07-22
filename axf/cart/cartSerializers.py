from rest_framework import serializers

from cart.models import AxfCart
from market.marketserializers import GoodsSerializer
from market.models import AxfGoods


class CartAddSerializer(serializers.Serializer):
    goodsid = serializers.CharField(required=True)
    token = serializers.CharField(required=True)

    def validate_goodis(self, value):
        value = int(value)
        the_goods = AxfGoods.objects.filter(pk=value).first()
        if not the_goods:
            raise serializers.ValidationError('商品不存在')
        return value

    def validate_token(self, value):
        if not value:
            raise serializers.ValidationError('token不存在')
        return value

class CarSerizlizer(serializers.ModelSerializer):
    c_goods = GoodsSerializer()
    class Meta:
        model = AxfCart
        fields = "__all__"