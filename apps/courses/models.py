from django.db import models
from organization.models import CourseOrg,Teacher

from DjangoUeditor.models import UEditorField

# Create your models here.

class Course(models.Model):

    degree_choice=(("cj","初级"),("zj","中级"),("gj","高级"))
    name=models.CharField(max_length=50,verbose_name="课程名")
    desc=models.CharField(max_length=300,verbose_name="课程描述")
    detail = UEditorField(verbose_name="课程详情", width=600, height=300, imagePath="courses/ueditor/", filePath="courses/ueditor/", default='')
    degree=models.CharField(choices=degree_choice,verbose_name="难度",max_length=2)
    is_banner=models.BooleanField(default=False,verbose_name="是否輪播")
    teacher=models.ForeignKey(Teacher,verbose_name="讲师",null=True,blank=True,on_delete=models.CASCADE)
    learn_time=models.IntegerField(default=0,verbose_name="学习时长(分)")
    students=models.IntegerField(default=0,verbose_name="学习人数")
    fav_nums= models.IntegerField(default=0, verbose_name="收藏人数")
    image=models.ImageField(upload_to="courses/%Y/%m",verbose_name="封面图",max_length=100,blank=True)
    click_nums=models.IntegerField(default=0, verbose_name="点击数")
    add_time=models.DateTimeField(auto_now=True,verbose_name="添加时间")
    course_org=models.ForeignKey(CourseOrg,verbose_name="课程机构",on_delete=models.CASCADE,null=True)
    category=models.CharField(max_length=20,verbose_name="课程类别",default="后端开发")
    tag=models.CharField(default="",verbose_name="课程标签",max_length=10,blank=True)
    youneed_know=models.CharField(default="",verbose_name="课程须知",max_length=300)
    teacher_tell = models.CharField(default="", verbose_name="老师告诉妮", max_length=300)


    # def get_lesson_nums(self):
    #
    #     return self.lesson_set.count()

    def get_learn_users(self):

        return self.usercourse_set.all()[:5]


    def go_to(self):

        from django.utils.safestring import mark_safe

        return  mark_safe("<a href='http://www.baidu.com'>go</a>")
    go_to.short_description="go"


    def get_course_lessons(self):

        return self.lesson_set.all()


    def increase_views(self):

        self.click_nums+=1
        self.save(update_fields=['click_nums'])


    class Meta:
        verbose_name="课程"
        verbose_name_plural=verbose_name

    def __str__(self):
        return self.name

class Lesson(models.Model):
    course=models.ForeignKey(Course,verbose_name="课程",on_delete=models.CASCADE)
    name = models.CharField(max_length=100, verbose_name="章节名")
    add_time = models.DateTimeField(auto_now=True, verbose_name="添加时间")

    class Meta:
        verbose_name="章节"
        verbose_name_plural=verbose_name

    def __str__(self):
        return self.name

    def get_lesson_video(self):

        return self.video_set.all()


class Video(models.Model):
    lesson=models.ForeignKey(Lesson,verbose_name="章节",on_delete=models.CASCADE)
    name = models.CharField(max_length=100, verbose_name="视频名")
    learn_time = models.IntegerField(default=0, verbose_name="学习时长(分)")
    url=models.CharField(max_length=200,verbose_name="访问地址",default="")
    add_time = models.DateTimeField(auto_now=True, verbose_name="添加时间")



    class Meta:
        verbose_name="视频"
        verbose_name_plural=verbose_name


class CourseResource(models.Model):
    course = models.ForeignKey(Course, verbose_name="课程", on_delete=models.CASCADE)
    name = models.CharField(max_length=100, verbose_name="名称")
    download=models.FileField(upload_to="courses/resource/%Y/%m",verbose_name="资源文件",max_length=100)
    add_time = models.DateTimeField(auto_now=True, verbose_name="添加时间")

    class Meta:
        verbose_name="课程资源"
        verbose_name_plural=verbose_name




class BannerCourse(Course):
    class Meta:
        verbose_name="轮播课程"
        verbose_name_plural=verbose_name
        proxy =True
