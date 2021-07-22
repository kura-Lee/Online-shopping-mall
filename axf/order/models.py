from django.db import models
from market.models import AxfGoods
from user.models import AxfUser


class AxfOrder(models.Model):
    """用户订单表"""
    o_price = models.FloatField()
    o_time = models.DateTimeField()
    o_status = models.IntegerField()
    o_user = models.ForeignKey(AxfUser, models.DO_NOTHING, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'axf_order'


class AxfOrdergoods(models.Model):
    """订单商品表"""
    o_goods_num = models.IntegerField()
    o_goods = models.ForeignKey(AxfGoods, models.DO_NOTHING, blank=True, null=True)
    o_order = models.ForeignKey(AxfOrder, models.DO_NOTHING, blank=True, null=True, related_name='goods')

    class Meta:
        managed = False
        db_table = 'axf_ordergoods'