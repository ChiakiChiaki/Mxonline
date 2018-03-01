"""LearNonline URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.conf.urls import url,include
import xadmin

from django.views.static import serve
from users.views import LoginView,RegisterView,ActiveView,ResetView,ForgetPwdView,ModifyPwdView,LogoutView,IndexView

from Mxonline.settings import MEDIA_ROOT

urlpatterns = [
    url(r'^xadmin/', xadmin.site.urls),
    url(r"^$",IndexView.as_view(),name="index"),
    url(r"^login/$",LoginView.as_view(),name="login"),
    url(r"^logout/$", LogoutView.as_view(), name="logout"),
    url(r"^register/$", RegisterView.as_view(), name="register"),
    url(r'^captcha/', include('captcha.urls')),
    url(r"^active/(?P<active_code>.*)/$",ActiveView.as_view(),name="active"),
    url(r"^forget/$",ForgetPwdView.as_view(),name="forget"),
    url(r"^reset/(?P<reset_code>.*)/$",ResetView.as_view(),name="reset"),
    url(r"^modify_pwd/$",ModifyPwdView.as_view(),name="modify_pwd"),

    url(r"^org/",include("organization.urls",namespace="org")),

    url(r"^course/",include("courses.urls",namespace="course")),
    url(r"^users/",include("users.urls",namespace="users")),

    url(r'^media/(?P<path>.*)$',serve,{"document_root":MEDIA_ROOT}),


    # url(r'^static/(?P<path>.*)$',serve,{"document_root":STATIC_ROOT}),

    url(r'^ueditor/',include("DjangoUeditor.urls")),



]

handler404= "users.views.page_not_found"
handler500="users.views.page_error"
