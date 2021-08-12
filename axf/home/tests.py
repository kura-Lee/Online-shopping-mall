from alipay import AliPay,AliPayConfig
from django.test import TestCase

# Create your tests here.
from axf.settings import ALI_APP_ID,APP_PRIVATE_KEY,ALIPAY_PUBLIC_KEY


def ali_buy(request):
    alipay = AliPay(
        appid=ALI_APP_ID,
        app_notify_url=None, # 默认回调url
        app_private_key_string=APP_PRIVATE_KEY,
        # 支付宝的公钥，验证支付宝回传消息使用,
        alipay_public_key_string=ALIPAY_PUBLIC_KEY,
        sign_type="RSA2", # RSA 或者 RSA2
        debug=True, # 默认False
        verbose = True,  # 输出调试数据
        # config=AliPayConfig(timeout=15)  # 可选，请求超时时间
    )

    #订单
    order_string = alipay.api_alipay_trade_page_pay(
        out_trade_no="2019061900100", #订单号，⾃自⼰己定义
        total_amount=90, #订单金额
        subject="macpro",#订单名称
        return_url="http://localhost:8000/mine/index", #回调地址
        #异步通知商家服务器地址，post
        notify_url="http://localhost:8000/mine/index" # 可选, 不填则使⽤用默认notify url
    )
    print(order_string)
    # 支付宝网关
    net = "https://openapi.alipaydev.com/gateway.do?"
    data = {
        "msg": "ok",
        "status": 200,
        "data": {
        "pay_url": net + order_string
        }
    }
    # return Response(data)
    print(net + order_string)

ali_buy(11)
# print(APP_PRIVATE_KEY)
# print(ALIPAY_PUBLIC_KEY)