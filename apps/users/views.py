from django.shortcuts import render,HttpResponse,HttpResponseRedirect
from django.urls.base import reverse
from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.backends import ModelBackend
from django.contrib.auth.hashers import make_password
from django.db.models import Q
from django.views.generic import View

from .forms import LoginForm,RegisterForm,ForgetForm,ModiFypwdForm,UploadImageForm,UserInfoForm
from operation.models import UserCourse,UserFavorite,UserMessage
from organization.models import CourseOrg,Teacher
from  courses.models import Course
from .models import UserProfile,EmailVerifyRecord,Banner
from utils import email_send
from utils.mixin_utils import LoginRequiredMixin
import json
from pure_pagination import Paginator, EmptyPage, PageNotAnInteger

# Create your views here.
class CustomBackend(ModelBackend):
    def authenticate(self, request, username=None, password=None, **kwargs):
        try:
            user=UserProfile.objects.get(Q(username=username)|Q(email=username))
            if user.check_password(password):
                return user
        except Exception as e:
            return None

class LogoutView(View):
    def get(self,request):
        logout(request)
        return  HttpResponseRedirect(reverse("index"))


class LoginView(View):
    def get(self,request):
        return render(request, "login.html", {})
    def post(self,request):
        login_form=LoginForm(request.POST)
        if login_form.is_valid():
            username = request.POST.get("username")
            pwd = request.POST.get("password")
            user = authenticate(username=username, password=pwd)

            if user is not None:
                if user.is_active:
                    login(request, user)
                    return HttpResponseRedirect(reverse("index"))
                else:
                    return render(request, "login.html", {"msg": "用户名未激活"})
            else:
                return render(request, "login.html", {"msg": "用户名或密码错误"})
        else:
            # err=login_form.errors.as_json()
            # print(err,type(err))
            return render(request, "login.html", {"login_form":login_form})



# def user_login(request):
#     if request.method=="POST":
#         username=request.POST.get("username")
#         pwd=request.POST.get("password")
#         user=authenticate(username=username,password=pwd)
#
#         if  user is not None:
#             login(request,user)
#             return render(request,"index.html")
#         else:
#             return render(request, "login.html",{"msg":"用户名或密码错误"})
#
#     else:
#         return render(request,"login.html",{})



class RegisterView(View):
    def get(self,request):
        register_form=RegisterForm()
        return render(request,"register.html",{"register_form":register_form})
    def post(self,request):
        register_form = RegisterForm(request.POST)
        if register_form.is_valid():
            if UserProfile.objects.filter(email=register_form.cleaned_data["email"]):
                return render(request,"register.html",{"msg":"用户已存在","register_form": register_form})

            user_profile=UserProfile()
            user_profile.email=register_form.cleaned_data["email"]
            user_profile.username = register_form.cleaned_data["email"]
            user_profile.password=make_password(register_form.cleaned_data["password"])
            user_profile.is_active = False
            user_profile.save()

            user_message=UserMessage()
            user_message.user=user_profile.id
            user_message.message="Welcome"
            user_message.save()

            email_send.send_register_email(user_profile.email,"register")


            return render(request, "login.html")
        else:
            return render(request, "register.html", {"register_form": register_form})



class ActiveView(View):
    def get(self,request,active_code):
        all_record=EmailVerifyRecord.objects.filter(code=active_code)
        if all_record:
            for record in all_record:
                email=record.email
                user=UserProfile.objects.get(email=email)
                user.is_active=True
                user.save()
        else:
            return render(request,"active_fail.html")
        return render(request,"login.html")


class ForgetPwdView(View):
    def get(self,request):
        return render(request,"forgetpwd.html",{"ForgetForm":ForgetForm})
    def post(self,request):
        forget_form=ForgetForm(request.POST)
        if forget_form.is_valid():
            data=forget_form.cleaned_data
            email=data["email"]
            email_send.send_register_email(email,"forget")
            return render(request,"send_success.html")
        else:
            return render(request,"forgetpwd.html",{"ForgetForm":ForgetForm})



class ResetView(View):
    def get(self,request,reset_code):
        all_record=EmailVerifyRecord.objects.filter(code=reset_code)
        if all_record:
            for record in all_record:
                email=record.email
                return render(request, "password_reset.html",{"email":email})

        else:
            return render(request,"active_fail.html")
        return render(request,"login.html")


class ModifyPwdView(View):
    def post(self,request):
        modify_form=ModiFypwdForm(request.POST)
        email1 = request.POST["email"]
        if modify_form.is_valid():
            data=modify_form.cleaned_data
            pwd1=data["password1"]
            pwd2=data["password2"]
            email=request.POST.get("email")
            if pwd1!=pwd2:
                return render(request, "password_reset.html", {"msg": "密码不一致"})
            user_profile=UserProfile.objects.get(email=email)
            user_profile.password=make_password(pwd2)
            user_profile.save()

            return render(request,"login.html")
        else:
            email = request.POST.get("email")
            return render(request, "password_reset.html", {"ModiFypwdForm": ModiFypwdForm,"email":email})


class UserInfoView(LoginRequiredMixin,View):
    def get(self,request):

        return  render(request,"usercenter-info.html",{})

    def post(self,request):
        user_info_form=UserInfoForm(request.POST,instance=request.user)
        if user_info_form.is_valid():
            user_info_form.save()
            return HttpResponse(json.dumps({"status":"success"}), content_type='application/json')
        else:
            return HttpResponse(json.dumps(user_info_form.errors),content_type='application/json')



class UploadImageView(LoginRequiredMixin,View):
    def post(self,request):
        image_form=UploadImageForm(request.POST,request.FILES,instance=request.user)
        if image_form.is_valid():
            image_form.save()
            result = {"status": "success"}
            return HttpResponse(json.dumps(result), content_type='application/json')
        else:
            result = {"status": "fail"}
            return HttpResponse(json.dumps(result), content_type='application/json')



class UpdatePwdView(LoginRequiredMixin,View):
    def post(self,request):
        modify_form=ModiFypwdForm(request.POST)

        if modify_form.is_valid():
            data=modify_form.cleaned_data
            pwd1=data["password1"]
            pwd2=data["password2"]

            if pwd1!=pwd2:
                result = {"status": "fail","msg":"密码不一致"}
                return HttpResponse(json.dumps(result), content_type='application/json')
            user=request.user

            user.password=make_password(pwd2)
            user.save()

            result = {"status": "success"}
            return HttpResponse(json.dumps(result), content_type='application/json')
        else:

            result = modify_form.errors
            return HttpResponse(json.dumps(result), content_type='application/json')


class SendEmailCodeView(LoginRequiredMixin,View):
    def get(self,request):
        email=request.GET.get("email","")

        if UserProfile.objects.filter(email=email):
            result = { "email": "邮箱已存在"}
            return HttpResponse(json.dumps(result), content_type='application/json')
        email_send.send_register_email(email, "update_email")
        result = {"status": "success"}
        return HttpResponse(json.dumps(result), content_type='application/json')


class UpdateEmailView(LoginRequiredMixin,View):
    def post(self,request):
        email=request.POST.get("email","")
        code=request.POST.get("code","")

        existed_record = EmailVerifyRecord.objects.filter(code=code,email=email,send_type="update_email")
        if existed_record:
            user=request.user
            user.email=email
            user.save(update_fields=["email"])
            result = {"status": "success"}
            return HttpResponse(json.dumps(result), content_type='application/json')
        else:
            result = {"email": "验证码出错"}
            return HttpResponse(json.dumps(result), content_type='application/json')



class MyCourseView(LoginRequiredMixin,View):
    def get(self,request):
        user_courses=UserCourse.objects.filter(user=request.user)
        return render(request,"usercenter-mycourse.html",{"user_courses":user_courses})




class MyFavOrgView(LoginRequiredMixin,View):

    def get(self,request):
        org_list=[]
        fav_orgs=UserFavorite.objects.filter(user=request.user,fav_type=2)
        if fav_orgs:
            for fav_org in fav_orgs:
                org_id=fav_org.fav_id
                org=CourseOrg.objects.get(id=org_id)
                org_list.append(org)

        return render(request,"usercenter-fav-org.html",{"org_list":org_list})

class MyFavTeacherView(LoginRequiredMixin,View):

    def get(self,request):
        teacher_list=[]
        fav_teachers=UserFavorite.objects.filter(user=request.user,fav_type=3)
        if fav_teachers:
            for fav_teacher in fav_teachers:
                teacher_id=fav_teacher.fav_id
                teacher=Teacher.objects.get(id=teacher_id)
                teacher_list.append(teacher)

        return render(request,"usercenter-fav-teacher.html",{"teacher_list":teacher_list})

class MyFavCourseView(LoginRequiredMixin,View):

    def get(self,request):
        course_list=[]
        fav_courses=UserFavorite.objects.filter(user=request.user,fav_type=1)
        if fav_courses:
            for fav_courses in fav_courses:
                course_id=fav_courses.fav_id
                course=Course.objects.get(id=course_id)
                course_list.append(course)

        return render(request,"usercenter-fav-course.html",{"course_list":course_list})


class MyMessageView(LoginRequiredMixin,View):
    def get(self,request):
        all_messages=UserMessage.objects.filter(user=request.user.id)
        all_unread_messages=UserMessage.objects.filter(has_read=False,user=request.user.id)
        for unread_message in all_unread_messages:
            unread_message.has_read=True
            unread_message.save(update_fields=["has_read"])

        try:
            page = request.GET.get('page', 1)
        except PageNotAnInteger:
            page = 1

        p = Paginator(all_messages, 1, request=request)

        messages = p.page(page)
        return render(request,"usercenter-message.html",{"messages":messages})


class IndexView(View):
    def get(self,requset):
        # print(1/0)
        all_banners=Banner.objects.all().order_by("index")
        courses=Course.objects.filter(is_banner=False)[:6]
        banner_courses=Course.objects.filter(is_banner=True)[:3]
        course_org=CourseOrg.objects.all()[:15]
        return render(requset,"index.html",{"all_banners":all_banners,"course_org":course_org,"banner_courses":banner_courses,"courses":courses})

#django2.0
def page_not_found(request,exception):
    from django.shortcuts import render_to_response
    response=render_to_response("404.html",{})
    response.status_code=404
    return response

def page_error(request):
    from django.shortcuts import render_to_response
    response=render_to_response("500.html",{})
    response.status_code=500
    return response