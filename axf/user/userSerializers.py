import re

from django.contrib.auth.hashers import make_password, check_password
from rest_framework import serializers
from user.models import AxfUser

class UserSerializer(serializers.ModelSerializer):

    class Meta:
        model = AxfUser
        fields = "__all__"

def vaild_email(email):
    if not re.match('^[a-zA-Z0-9_-]+@[a-zA-Z0-9_-]+(\.[a-zA-Z0-9_-]+)+$', email):
        raise serializers.ValidationError('邮箱格式错误')

class UserRegisterSerializer(serializers.Serializer):
    u_username = serializers.CharField(required=True,)
    u_password = serializers.CharField(min_length=3,
                                       max_length=12,
                                       error_messages={
                                           'max_lenth':'最大长度不超过12字符',
                                           'min_lenth':'最小长度不超过3字符',
                                       })
    u_password2 = serializers.CharField(min_length=3,
                                       max_length=12,
                                       error_messages={
                                           'max_lenth': '最大长度不超过12字符',
                                           'min_lenth': '最小长度不超过3字符',
                                       })
    u_email = serializers.CharField(required=True, validators=[vaild_email,])

    # 验证用户名是否唯一
    def validate_u_username(self, attrs):
        user = AxfUser.objects.filter(u_username=attrs).first()
        if user:
            raise serializers.ValidationError('用户名已经被占用了')
        # 注意单字段验证成功需要返回验证数据
        return attrs

    def validate(self, attrs):
        password = attrs.get('u_password')
        password2 = attrs.get('u_password2')
        if password != password2:
            raise serializers.ValidationError('两次密码不一致')
        return attrs

    def create(self, validated_data):
        # print(validated_data)
        password = validated_data.get('u_password')
        user = AxfUser()
        user.u_username = validated_data.get('u_username')
        user.u_password = make_password(password)
        user.u_email = validated_data.get('u_email')
        # 激活用户
        user.is_active = 1
        # 未删除
        user.is_delete = 0
        user.save()
        return user

    def update(self, instance, validated_data):
        # print(instance)
        user = instance
        user.u_username = validated_data.get('u_username') if validated_data.get('u_username') else user.u_username
        user.u_password = validated_data.get('u_password') if validated_data.get('u_password') else user.u_password
        user.u_email = validated_data.get('u_email') if validated_data.get('u_email') else user.u_email
        # 保存原来状态
        user.is_active = user.is_active
        user.is_delete = user.is_delete
        return user.save()


class UerLoginSerializer(serializers.Serializer):
    u_username = serializers.CharField(required=True, max_length=32, min_length=3, help_text="用户名")
    u_password = serializers.CharField(required=True, min_length=3, max_length=256, help_text="密码")


    def validate(self, attrs):
        username = attrs.get('u_username')
        password = attrs.get('u_password')
        user = AxfUser.objects.filter(u_username=username)
        # 判读用户是否存在
        if not user.exists():
            raise serializers.ValidationError('用户名不存在')
        user = user.first()
        if not check_password(password, user.u_password):
            raise serializers.ValidationError('用户名或密码错误')
        return user