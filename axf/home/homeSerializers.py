from rest_framework import serializers

from home.models import AxfWheel, AxfNav, AxfMainshow, AxfShop, AxfMustbuy


class MainShowSerializer(serializers.ModelSerializer):
    class Meta:
        model = AxfMainshow
        fields = "__all__"


class ShopSerializer(serializers.ModelSerializer):
    class Meta:
        model = AxfShop
        fields = "__all__"


class NavSerializer(serializers.ModelSerializer):
    class Meta:
        model = AxfNav
        fields = "__all__"


class WheelSerializer(serializers.ModelSerializer):
    class Meta:
        model = AxfWheel
        fields = "__all__"


class MustbuySerializer(serializers.ModelSerializer):
    class Meta:
        model = AxfMustbuy
        fields = "__all__"


