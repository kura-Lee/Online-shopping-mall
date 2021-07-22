from rest_framework import serializers
from market.models import AxfGoodtype, AxfGoods


class GoodTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = AxfGoodtype
        fields = '__all__'


class GoodsSerializer(serializers.ModelSerializer):
    class Meta:
        model = AxfGoods
        fields = "__all__"
