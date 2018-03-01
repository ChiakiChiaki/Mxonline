#Author:Sun Jian

import xadmin
from .models import EmailVerifyRecord,UserProfile,Banner
from  xadmin.plugins.auth import UserAdmin
from xadmin import views

class BaseSetting(object):
    enable_themes=True
    use_booswatch=True

class GlobalSettings(object):
    site_title="后台管理系统"
    site_footer="在线平台"
    menu_style="accordion"

# class UserProfileAdmin(UserAdmin):
#     pass

class EmailVerifyRecordAdmin(object):

    list_display=['code','email',"send_type","send_time"]
    search_fields=['code','email',"send_type","send_time"]
    list_filter=['code','email',"send_type","send_time"]
    model_icon="fa fa-bath"


class BannerAdmin(object):
    list_display=['title',"image",'url',"index","add_time"]
    search_fields=['title',"image",'url',"index","add_time"]
    list_filter=['title',"image",'url',"index","add_time"]


# xadmin.site.register(UserProfile,UserProfileAdmin)
xadmin.site.register(EmailVerifyRecord,EmailVerifyRecordAdmin)
xadmin.site.register(Banner,BannerAdmin)
xadmin.site.register(views.BaseAdminView,BaseSetting)
xadmin.site.register(views.CommAdminView,GlobalSettings)