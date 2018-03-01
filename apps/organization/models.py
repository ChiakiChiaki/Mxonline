from django.db import models

# Create your models here.
class CourseOrg(models.Model):
    name=models.CharField(max_length=50,verbose_name="机构名")
    desc=models.TextField(verbose_name="机构描述")
    tag = models.CharField(max_length=10, default="全国知名", verbose_name="标签")
    category=models.CharField(max_length=20,choices=(("pxjg","培训机构"),("gr","个人"),("gx","高校")),verbose_name="机构类别",default="pxjg")
    click_num=models.IntegerField(default=0,verbose_name="点击数")
    fav_num=models.IntegerField(default=0,verbose_name="收藏数")
    image = models.ImageField(upload_to="org/%Y/%m", verbose_name="封面图", max_length=100)
    address=models.CharField(max_length=150,verbose_name="地址名")
    city=models.ForeignKey("CityDict",on_delete=models.CASCADE)
    students=models.IntegerField(default=0,verbose_name="学习人数")
    course_nums=models.IntegerField(default=0,verbose_name="课程数")
    add_time = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name


    class Meta:
        verbose_name="课程机构"
        verbose_name_plural=verbose_name


class CityDict(models.Model):
    name=models.CharField(max_length=20,verbose_name="城市")
    desc=models.CharField(max_length=200,verbose_name="描述")
    add_time=models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name="城市"
        verbose_name_plural=verbose_name
    def __str__(self):
        return self.name

class Teacher(models.Model):
    org=models.ForeignKey(CourseOrg,verbose_name="机构",on_delete=models.CASCADE)
    name = models.CharField(max_length=40, verbose_name="教师名")
    work_years=models.IntegerField(default=0,verbose_name="工作年限")
    work_company=models.CharField(max_length=50,verbose_name="就职公司")
    work_position = models.CharField(max_length=50, verbose_name="公司职位")
    specials=models.CharField(max_length=50,verbose_name="教学特点")
    click_num = models.IntegerField(default=0, verbose_name="点击数")
    fav_num = models.IntegerField(default=0, verbose_name="收藏数数")
    image = models.ImageField(upload_to="teacher/%Y/%m", verbose_name="头像", max_length=100,default="")
    age=models.IntegerField(default="18")
    add_time = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name="教师"
        verbose_name_plural=verbose_name

    def __str__(self):
        return self.name



