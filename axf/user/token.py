import base64
from itsdangerous import URLSafeTimedSerializer as utsr
from axf.settings import SECRET_KEY
# from django.conf import settings as django_settings


class Token():
    def __init__(self, security_key):
        self.security_key = security_key
        self.serializer = utsr(self.security_key)
        self.salt = base64.encodebytes(security_key.encode('utf8'))

    #生成token, value为要加密的字段
    def generate_validate_token(self, value):
        res = self.serializer.dumps(value, self.salt)
        # print(self.serializer)
        return res
    # 验证token，有效时间默认5mins
    def confirm_validate_token(self, token, expiration=3600):
        return self.serializer.loads(token, salt=self.salt, max_age=expiration)
    #移除token
    def remove_validate_token(self, token):
        #print(self.serializer.loads(token, salt=self.salt))
        return self.serializer.loads(token, salt=self.salt)

# 定义为全局变量
token_confirm = Token(SECRET_KEY)


## uuid直接生成token,配合缓存直接完成认证
# import uuid
# from django.core.cache import cache
# token = uuid.uuid4().hex
# 写⼊缓存
# cache.set(token,user.id,3600)