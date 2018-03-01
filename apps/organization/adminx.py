#Author:Sun Jian
import xadmin
from .models import CourseOrg,CityDict,Teacher

class CourseOrgAdmin(object):
    list_display = ['name', 'desc','category',  'click_num', 'fav_num','add_time' ]
    search_fields = ['name', 'desc','category',  'click_num', 'fav_num']
    list_filter = ['name', 'desc', 'category', 'click_num', 'fav_num','city__name','address','add_time']
    # relfield_style = 'fk-ajax'


class CityDictAdmin(object):
    list_display = ['name', 'desc', 'add_time']
    search_fields = ['name', 'desc']
    list_filter = ['name', 'desc', 'add_time']


class TeacherAdmin(object):
    list_display = ['name', 'org', 'work_years', 'work_company','add_time']
    search_fields = ['org', 'name', 'work_years', 'work_company']
    list_filter = ['org__name', 'name', 'work_years', 'work_company','click_num', 'fav_num', 'add_time']




xadmin.site.register(CourseOrg,CourseOrgAdmin)
xadmin.site.register(CityDict,CityDictAdmin)
xadmin.site.register(Teacher,TeacherAdmin)
