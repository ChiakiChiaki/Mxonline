 #Author:Sun Jian
import xadmin
from .models import Course,CourseResource,Lesson,Video,BannerCourse
from organization.models import CourseOrg

class LessonInline(object):
    model=Lesson
    extra=1

class CourseResourceInline(object):
    model=CourseResource
    extra=1






class CourseAdmin(object):
     list_display=["name","desc","degree","students","learn_time","click_nums","go_to"]
     search_fields=["name","desc","degree","students","learn_time","click_nums","teacher__name"]
     list_filter=["name","desc","degree","students","learn_time","click_nums","teacher__name"]
     ordering=["-click_nums"]
     readonly_fields=["fav_nums",]
     exclude=["click_nums"]
     list_editable=["degree"]
     inlines=[LessonInline,CourseResourceInline]
     # refresh_times = [100,200]
     style_fields={"detail":"ueditor"}
     import_excel = True

     def queryset(self):
         qs = super(CourseAdmin, self).queryset()
         qs = qs.filter(is_banner=False)
         return qs

     def save_models(self):
         obj=self.new_obj
         obj.save()
         if obj.course_org is not None:
             course_org=obj.course_org
             course_org.course_nums=Course.objects.filter(course_org=course_org).count()
             course_org.save()

     def post(self,request,*args,**kwargs):
        if "excel" in request.FILES:
            pass
        return super(CourseAdmin,self).post(request,*args,**kwargs)







class BannerCourseAdmin(object):
     list_display=["name","desc","degree","students","learn_time","click_nums"]
     search_fields=["name","desc","degree","students","learn_time","click_nums","teacher__name"]
     list_filter=["name","desc","degree","students","learn_time","click_nums","teacher__name"]
     ordering=["-click_nums"]
     readonly_fields=["fav_nums",]
     exclude=["click_nums"]
     inlines=[LessonInline,CourseResourceInline]

     def queryset(self):
         qs = super(BannerCourseAdmin, self).queryset()
         qs = qs.filter(is_banner=True)
         return qs

class LessonAdmin(object):
    list_display=["course","name","add_time"]
    search_fields=["course","name"]
    list_filter=["course__name","name"]

class VideoAdmin(object):
    list_display=["lesson","name","add_time"]
    search_fields=["lesson","name"]
    list_filter=["lesson__name","name"]



class CourseResourceAdmin(object):
    list_display=["course","name","download","add_time"]
    search_fields=["course","name","download"]
    list_filter=["course__name","name","download"]

xadmin.site.register(Course,CourseAdmin)
xadmin.site.register(BannerCourse,BannerCourseAdmin)
xadmin.site.register(Lesson,LessonAdmin)
xadmin.site.register(Video,VideoAdmin)
xadmin.site.register(CourseResource,CourseResourceAdmin)