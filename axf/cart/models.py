from django.db import models
from market.models import AxfGoods
from user.models import AxfUser


class AxfCart(models.Model):
    """购物车表"""
    c_goods_num = models.IntegerField()
    c_is_select = models.IntegerField()
    c_goods = models.ForeignKey(AxfGoods, models.DO_NOTHING, blank=True, null=True)
    c_user = models.ForeignKey(AxfUser, models.DO_NOTHING, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'axf_cart'