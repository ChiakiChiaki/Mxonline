from django.db import models


import datetime

from django.contrib.auth.models  import AbstractUser

class UserProfile(AbstractUser):

    gender_choice=(("male","男"),("female","女"))

    nickname=models.CharField(max_length=40,verbose_name="昵称",default="")
    birthday=models.DateField(verbose_name="生日",blank=True,null=True)
    gender=models.CharField(choices=gender_choice,default="male",max_length=6)
    address=models.CharField(max_length=100,default="")
    mobile=models.CharField(max_length=11,null=True,blank=True)
    avator=models.ImageField(upload_to="image/%Y/%m",default="image/default.png",max_length=100)

    class Meta(AbstractUser.Meta):
        verbose_name = "用户信息"
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.username

    def unread_nums(self):
        from operation.models import UserMessage
        return UserMessage.objects.filter(user=self.id,has_read=False).count()


class EmailVerifyRecord(models.Model):
    choices=(("register","注册"),("forget","找回密码"),("update_email","修改邮箱"))
    code=models.CharField(max_length=20,verbose_name="验证码")
    email=models.EmailField(max_length=50,verbose_name="邮箱")
    send_type=models.CharField(choices=choices,max_length=15)
    send_time=models.DateTimeField(auto_now=True)


    class Meta:
        verbose_name="邮箱验证码"
        verbose_name_plural=verbose_name

    def __str__(self):
        return "%s(%s)"%(self.code,self.email)


class Banner(models.Model):
    title=models.CharField(max_length=100,verbose_name="标题")
    image=models.ImageField(upload_to="banner/%Y/%m",verbose_name="轮播图",max_length=100)
    url=models.URLField(max_length=200,verbose_name="访问地址")
    index=models.IntegerField(default=100,verbose_name="顺序")
    add_time=models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name="轮播图"
        verbose_name_plural=verbose_name






