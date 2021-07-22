from django_filters import rest_framework as filters

from market.models import AxfGoods


class GoodsFilter(filters.FilterSet):
    typeid = filters.CharFilter(field_name='categoryid', lookup_expr='exact')
    childcid = filters.CharFilter(field_name='childcid', method='filter_child_type')
    order_rule = filters.CharFilter(field_name='', method='order_goods')
    class Meta:
        model = AxfGoods
        fields = ['categoryid']

    def filter_child_type(self, queryset, name, value):
        value = int(value)
        if value > 0:
            return queryset.filter(childcid=int(value))
        return queryset

    def order_goods(self, queryset, name, value):
        """
        :param queryset:查询结果集
        :param name:查询字段
        :param value:查询值
        :return:
        """
        value = int(value)
        if value == 1:
            queryset = queryset.order_by("price")
        elif value == 2:
            queryset = queryset.order_by("-price")
        elif value == 3:
            queryset = queryset.order_by("productnum")
        elif value == 4:
            queryset = queryset.order_by("-productnum")
        return queryset