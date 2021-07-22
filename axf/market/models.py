from django.db import models

# Create your models here.

class AxfGoodtype(models.Model):
    """分类表"""
    typeid = models.IntegerField()
    typename = models.CharField(max_length=32)
    childtypenames = models.CharField(max_length=255)
    typesort = models.IntegerField()

    class Meta:
        managed = False
        db_table = 'axf_foodtype'


class AxfGoods(models.Model):
    """商品表"""
    productid = models.IntegerField()
    productimg = models.CharField(max_length=255)
    productname = models.CharField(max_length=128)
    productlongname = models.CharField(max_length=255)
    isxf = models.IntegerField()
    pmdesc = models.IntegerField()
    specifics = models.CharField(max_length=64)
    price = models.FloatField()
    marketprice = models.FloatField()
    categoryid = models.IntegerField()
    childcid = models.IntegerField()
    childcidname = models.CharField(max_length=128)
    dealerid = models.IntegerField()
    storenums = models.IntegerField()
    productnum = models.IntegerField()

    class Meta:
        managed = False
        db_table = 'axf_goods'

