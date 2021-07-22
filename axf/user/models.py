from django.db import models


class AxfUser(models.Model):
    """用户表"""
    u_username = models.CharField(unique=True, max_length=32)
    u_password = models.CharField(max_length=256)
    u_email = models.CharField(unique=True, max_length=64)
    is_active = models.IntegerField(default=1)
    is_delete = models.IntegerField()

    class Meta:
        managed = False
        db_table = 'axf_user'
