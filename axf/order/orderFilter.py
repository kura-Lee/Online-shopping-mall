from django_filters import rest_framework as filters

from axf import settings
from order.models import AxfOrder


class OrderFilter(filters.FilterSet):
    o_status = filters.CharFilter(field_name='o_status', method='filter_status')

    class Meta:
        model = AxfOrder
        fields = "__all__"

    def filter_status(self, queryset, name, value):
        print(value)
        if value == 'not_pay':
            return queryset.filter(o_status=settings.ORDER_STATUS_NOT_PAY)
        elif value == 'not_send':
            return queryset.filter(o_status=settings.ORDER_STATUS_NOT_SEND)
        return queryset