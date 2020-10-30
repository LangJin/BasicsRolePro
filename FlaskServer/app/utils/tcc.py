import json
from tencentcloud.common import credential
from tencentcloud.common.profile.client_profile import ClientProfile
from tencentcloud.common.profile.http_profile import HttpProfile
from tencentcloud.common.exception.tencent_cloud_sdk_exception import TencentCloudSDKException
from tencentcloud.sms.v20190711 import sms_client, models


def SendTxSms(phone,templateType,code):
    """
    腾讯云发送短信方法
    """
    TemplateDict = {
        "login":"746300",
        "payps":"746299",
        "ps":"743776"
    }
    TemplateID = TemplateDict.get(templateType)
    try: 
        cred = credential.Credential("AKIDwjNq8EutR6at21OscGhzFMQjvgBUtfXC", "d7QnW4RefWEnYrzxkLkz2G8qMfmhiXIu") 
        httpProfile = HttpProfile()
        httpProfile.endpoint = "sms.tencentcloudapi.com"
        clientProfile = ClientProfile()
        clientProfile.httpProfile = httpProfile
        client = sms_client.SmsClient(cred, "", clientProfile) 
        req = models.SendSmsRequest()
        params = {
            "PhoneNumberSet": [ "+86{}".format(phone) ],
            "TemplateParamSet":["{}".format(code)],
            "TemplateID": TemplateID,
            "SmsSdkAppid": "1400435144",
            "Sign":"许昌九羊文化传播有限公司"
        }
        req.from_json_string(json.dumps(params))
        resp = client.SendSms(req) 
        return json.loads(resp.to_json_string())
    except TencentCloudSDKException as err: 
        return err