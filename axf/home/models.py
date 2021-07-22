# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey has `on_delete` set to the desired behavior.
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from django.db import models


class AxfMainshow(models.Model):
    """主页表"""
    img = models.CharField(max_length=255)
    name = models.CharField(max_length=64)
    trackid = models.IntegerField()
    categoryid = models.IntegerField()
    brandname = models.CharField(max_length=64)
    img1 = models.CharField(max_length=255)
    childcid1 = models.IntegerField()
    productid1 = models.IntegerField()
    longname1 = models.CharField(max_length=128)
    price1 = models.FloatField()
    marketprice1 = models.FloatField()
    img2 = models.CharField(max_length=255)
    childcid2 = models.IntegerField()
    productid2 = models.IntegerField()
    longname2 = models.CharField(max_length=128)
    price2 = models.FloatField()
    marketprice2 = models.FloatField()
    img3 = models.CharField(max_length=255)
    childcid3 = models.IntegerField()
    productid3 = models.IntegerField()
    longname3 = models.CharField(max_length=128)
    price3 = models.FloatField()
    marketprice3 = models.FloatField()

    class Meta:
        managed = False
        db_table = 'axf_mainshow'


class AxfShop(models.Model):
    """便利店栏"""
    img = models.CharField(max_length=255)
    name = models.CharField(max_length=64)
    trackid = models.IntegerField()

    class Meta:
        managed = False
        db_table = 'axf_shop'


class AxfNav(models.Model):
    """推荐栏"""
    img = models.CharField(max_length=255)
    name = models.CharField(max_length=64)
    trackid = models.IntegerField()

    class Meta:
        managed = False
        db_table = 'axf_nav'


class AxfWheel(models.Model):
    """轮播表"""
    img = models.CharField(max_length=255)
    name = models.CharField(max_length=64)
    trackid = models.IntegerField()

    class Meta:
        managed = False
        db_table = 'axf_wheel'

class AxfMustbuy(models.Model):
    """必买栏"""
    img = models.CharField(max_length=255)
    name = models.CharField(max_length=64)
    trackid = models.IntegerField()

    class Meta:
        managed = False
        db_table = 'axf_mustbuy'