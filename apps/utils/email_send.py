#Author:Sun Jian
import random
from users.models import EmailVerifyRecord
from django.core.mail import send_mail
from Mxonline.settings import EMAIL_FROM


def send_register_email(email,send_type="register"):
    email_record=EmailVerifyRecord()
    if send_type=="update_email":
        random_code=random_str(4)
    else:
        random_code=random_str(16)
    email_record.code=random_code
    email_record.email=email
    email_record.send_type=send_type
    email_record.save()

    email_title=""
    email_body=""
    if send_type=="register":
        email_title="注册激活连接"
        email_body="请点击如下激活：127.0.0.1:8000/active/%s" %random_code

        send_status=send_mail(email_title,email_body,EMAIL_FROM,[email])
        if send_status:
            pass

    elif send_type=="forget":
        email_title="密碼重置鏈接"
        email_body="请点击如下激活：127.0.0.1:8000/reset/%s" %random_code
        send_status=send_mail(email_title,email_body,EMAIL_FROM,[email])
        if send_status:
            pass


    elif send_type=="update_email":

        email_title="修改密码"
        email_body="验证码,%s" %random_code
        send_status=send_mail(email_title,email_body,EMAIL_FROM,[email])
        if send_status:
            pass



def random_str(randomlength=8):
    nums=[]
    for i in range(0,9):
        nums.append(i)
    for i in range(65,91):
        nums.append(i)
    for i in range(97,123):
        nums.append(i)
    random_str=""
    list=random.sample(nums,randomlength)
    for i,v in enumerate(list):
        if v>10:
            list[i]=chr(v)
        random_str = random_str + str(list[i])
    return random_str






