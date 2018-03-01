from django.shortcuts import render,HttpResponse,get_object_or_404
from django.views.generic import View,ListView,DetailView

from .models import CourseOrg,CityDict,Teacher
from operation.models import UserFavorite

from operation.forms import UserAskForm

from pure_pagination import Paginator, EmptyPage, PageNotAnInteger

from courses.models import Course

import json
from django.db.models import Q





class OrgView(View):

    def get(self,request):
        all_orgs=CourseOrg.objects.all()
        keywords = request.GET.get("keywords", "")
        if keywords:
            all_orgs = all_orgs.filter( Q(name__icontains=keywords) | Q(desc__icontains=keywords))

        all_citys=CityDict.objects.all()
        city_id=request.GET.get("city","")

        if city_id:
            all_orgs=all_orgs.filter(city_id=int(city_id))

        category=request.GET.get("ct","")

        if category:
            all_orgs=all_orgs.filter(category=category)

        sort=request.GET.get("sort","")
        if sort:
            if sort=="students":
                all_orgs=all_orgs.order_by("-students")
            elif sort=="course_nums":
                all_orgs = all_orgs.order_by("-course_nums")


        org_num=all_orgs.count()

        try:
            page = request.GET.get('page', 1)
        except PageNotAnInteger:
            page = 1

        p = Paginator(all_orgs,3, request=request)

        orgs = p.page(page)

        context={"all_orgs":orgs,"all_citys":all_citys,"city_id":city_id,"category":category,"org_num":org_num,"sort":sort}
        return render(request,"org-list.html",context=context)


# class AddUserAskView(View):
#     def post(self,request):
#         userask_form=UserAskForm(request.POST)
#
#         if userask_form.is_valid():
#             user_ask=userask_form.save(commit=False)
#             return HttpResponse("{'status':'success'}",content_type='application/json')
#         else:
#             return HttpResponse("{'status':'fail','msg': %s}"% userask_form.errors, content_type='application/json')

class AddUserAskView(View):

    def post(self, request):
        userask_form = UserAskForm(request.POST)
        if userask_form.is_valid():
            user_ask = userask_form.save(commit=True )
            result={"status":"success"}

            return HttpResponse(json.dumps(result), content_type='application/json')
        else:

            result={"status":"fail", "msg":"您的字段有错,请检查"}
            return HttpResponse(json.dumps(result), content_type='application/json')

class OrgHomeView(View):
    def get(self,request,org_id):
        current_page="home"
        course_org=CourseOrg.objects.get(id__exact=int(org_id))
        course_org.click_num+=1
        course_org.save(update_fields=["click_num"])

        has_fav=False
        if request.user.is_authenticated:
            if UserFavorite.objects.filter(user=request.user,fav_id=course_org.id,fav_type=2):
                has_fav=True
        all_courses=course_org.course_set.all()[:3]
        all_teacher=course_org.teacher_set.all()[:1]

        return render(request,"org-detail-homepage.html",{"all_courses":all_courses,"all_teachers":all_teacher
                      ,"course_org":course_org,"current_page":current_page,"has_fav":has_fav})




class OrgCourseView(View):
    def get(self,request,org_id):
        current_page = "course"
        course_org=CourseOrg.objects.get(id__exact=int(org_id))
        has_fav=False
        if request.user.is_authenticated:
            if UserFavorite.objects.filter(user=request.user,fav_id=course_org.id,fav_type=2):
                has_fav=True
        all_courses=course_org.course_set.all()
        return render(request,"org-detail-course.html",{"all_courses":all_courses,"course_org":course_org,"current_page":current_page,"has_fav":has_fav})







class OrgDescView(View):
    def get(self,request,org_id):
        current_page = "desc"
        course_org=CourseOrg.objects.get(id__exact=int(org_id))
        has_fav=False
        if request.user.is_authenticated:
            if UserFavorite.objects.filter(user=request.user,fav_id=course_org.id,fav_type=2):
                has_fav=True
        return render(request,"org-detail-desc.html",{"course_org":course_org,"current_page":current_page,"has_fav":has_fav})




class OrgTeacherView(View):
    def get(self,request,org_id):
        current_page = "teacher"
        course_org=CourseOrg.objects.get(id__exact=int(org_id))
        has_fav = False
        if request.user.is_authenticated:
            if UserFavorite.objects.filter(user=request.user, fav_id=course_org.id, fav_type=2):
                has_fav = True
        all_teachers=course_org.teacher_set.all()
        return render(request,"org-detail-teachers.html",{"all_teachers":all_teachers,"course_org":course_org,"current_page":current_page,"has_fav":has_fav})


class AddFavView(View):
    def post(self,request):
        fav_id=request.POST.get("fav_id",0)
        fav_type = request.POST.get("fav_type", 0)

        if not request.user.is_authenticated:
            result = {"status": "fail", "msg": "用户未登录"}
            return HttpResponse(json.dumps(result), content_type='application/json')
        exist_records=UserFavorite.objects.filter(user=request.user,fav_id=int(fav_id),fav_type=int(fav_type))

        if exist_records:
            exist_records.delete()
            if fav_type=="1":
                course=Course.objects.get(id=int(fav_id))
                course.fav_nums-=1
                if course.fav_nums < 0:
                    course.fav_nums = 0
                course.save(update_fields=["fav_nums"])
            elif fav_type =="2":
                course_org = CourseOrg.objects.get(id=int(fav_id))
                course_org.fav_num -= 1
                if course_org.fav_num < 0:
                    course_org.fav_num = 0
                course_org.save(update_fields=["fav_num"])
            elif fav_type=="3":
                teacher=Teacher.objects.get(id=int(fav_id))
                teacher.fav_num-=1
                if teacher.fav_num < 0:
                    teacher.fav_num = 0
                teacher.save(update_fields=["fav_num"])



            result = {"status": "success", "msg": "收藏 "}
            return HttpResponse(json.dumps(result), content_type='application/json')
        else:
            user_fav=UserFavorite()
            if int(fav_id)>0 and int(fav_type)>0:
                user_fav.user=request.user
                user_fav.fav_id=int(fav_id)
                user_fav.fav_type = int(fav_type)
                user_fav.save()
                if fav_type == "1":
                    course = Course.objects.get(id=int(fav_id))
                    course.fav_nums += 1
                    course.save(update_fields=["fav_nums"])
                elif fav_type == "2":
                    course_org = CourseOrg.objects.get(id=int(fav_id))
                    course_org.fav_num += 1
                    course_org.save(update_fields=["fav_num"])
                elif fav_type == "3":
                    teacher = Teacher.objects.get(id=int(fav_id))
                    teacher.fav_num += 1
                    teacher.save(update_fields=["fav_num"])

                result = {"status": "success", "msg": "已收藏 "}
                return HttpResponse(json.dumps(result), content_type='application/json')
            else:
                result = {"status": "fail", "msg": "收藏出错"}
                return HttpResponse(json.dumps(result), content_type='application/json')


class TeacherListView(View):
    def get(self,request):
        all_teachers=Teacher.objects.all()
        keywords = request.GET.get("keywords", "")
        if keywords:
            all_teachers = all_teachers.filter(Q(name__icontains=keywords) | Q(work_company__icontains=keywords)| Q(work_position__icontains=keywords))
        sort = request.GET.get("sort", "")
        if sort:
            if sort == "hot":
                all_teachers = all_teachers.order_by("-click_num")

        try:
            page = request.GET.get('page', 1)
        except PageNotAnInteger:
            page = 1

        p = Paginator(all_teachers, 1, request=request)

        teachers = p.page(page)

        return render(request,"teachers-list.html",{"all_teachers":teachers,"sort":sort})


class TeacherDetailView(View):
    def get(self,request,teacher_id):
        teacher=Teacher.objects.get(id=int(teacher_id))
        teacher.click_num+=1
        teacher.save(update_fields=["click_num"])

        all_courses= Course.objects.filter(teacher=teacher)

        has_teacher_fav=False
        if UserFavorite.objects.filter(user=request.user,fav_type=3,fav_id=teacher.id):
            has_teacher_fav=True

        has_org_fav=False
        if UserFavorite.objects.filter(user=request.user,fav_type=2,fav_id=teacher.org.id):
            has_org_fav=True

        return render(request,"teacher-detail.html",{"teacher":teacher,"all_courses":all_courses,"has_org_fav":has_org_fav,"has_teacher_fav":has_teacher_fav})

