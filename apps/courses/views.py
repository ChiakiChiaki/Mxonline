from django.shortcuts import render,HttpResponse
from django.views.generic import View
from django.db.models import Q

from pure_pagination import Paginator, EmptyPage, PageNotAnInteger
from .models import Course,CourseResource,Video
from operation.models import UserFavorite,CourseCommnet,UserCourse
from utils.mixin_utils import LoginRequiredMixin

import json


# Create your views here.


class CourseListView(View):
    def get(self,request):
        all_courses=Course.objects.all().order_by("-add_time")

        keywords= request.GET.get("keywords","")
        if keywords:
            all_courses=all_courses.filter(Q(name__icontains=keywords)|Q(desc__icontains=keywords)|Q(detail__icontains=keywords))

        sort = request.GET.get("sort", "")
        if sort:
            if sort == "students":
                all_courses = all_courses.order_by("-students")
            elif sort == "hot":
                all_courses = all_courses.order_by("-click_nums")

        try:
            page = request.GET.get('page', 1)
        except PageNotAnInteger:
            page = 1

        p = Paginator(all_courses, 3, request=request)

        courses = p.page(page)
        return render(request,"course-list.html",{"all_courses":courses,"sort":sort})

class CourseDetailView(View):
    def get(self, request,course_id):
        course=Course.objects.get(id=int(course_id))
        course.increase_views()
        has_fav_course=False
        has_fav_org=False
        if request.user.is_authenticated:
            if UserFavorite.objects.filter(user=request.user, fav_id=course_id, fav_type=1):
                has_fav_course = True
            if UserFavorite.objects.filter(user=request.user, fav_id=course.course_org.id, fav_type=2):
                has_fav_org = True

        tag=course.tag
        if tag:
            relate_courses=Course.objects.filter(tag=tag).exclude(id=course_id)[:1]
        else:
            relate_courses=[]

        return render(request, "course-detail.html", {"course":course,"relate_courses":relate_courses
                                                      ,"has_fav_course":has_fav_course,"has_fav_org":has_fav_org})




class CourseInfoView(LoginRequiredMixin,View):
    def get(self, request, course_id):

        course = Course.objects.get(id=int(course_id))
        course.click_nums+=1
        course.save(update_fields=["click_nums"])

        user_courses=UserCourse.objects.filter(user=request.user,course=course)

        if not user_courses:
            user_courses = UserCourse(user=request.user, course=course)
            course.students += 1
            course.save(update_fields=["students"])
            user_courses.save()

        user_courses = UserCourse.objects.filter(course=course)
        user_ids=[user_course.user_id for user_course in user_courses]
        all_user_courses=UserCourse.objects.filter(user_id__in=user_ids)

        course_ids=[user_course.course_id for user_course in all_user_courses]
        # course_ids= list(set((course_ids)))  #去除重复课程ID
        relate_courses=Course.objects.filter(~Q(id=int(course_id)),id__in=course_ids).order_by("-click_nums")[:5]
        # print(relate_courses)

        all_resource=CourseResource.objects.filter(course=course)

        return render(request, "course-video.html", {"course": course, "course_resources":all_resource,"relate_courses":relate_courses})


class CommentsView(LoginRequiredMixin,View):
    def get(self, request, course_id):
        course = Course.objects.get(id=int(course_id))
        all_resource=CourseResource.objects.filter(course=course)
        all_comments=CourseCommnet.objects.filter(course_id=int(course_id))
        return render(request, "course-comment.html", {"course": course, "course_resources":all_resource,"all_comments":all_comments})


class AddCommentView(View):
    def post(self,request):
        if not request.user.is_authenticated:
            result = {"status": "fail", "msg": "用户未登录"}
            return HttpResponse(json.dumps(result), content_type='application/json')

        course_id=request.POST.get("course_id",0)
        comments=request.POST.get("comments","")
        if int(course_id)>0 and comments:
            course_comment=CourseCommnet()
            course=Course.objects.get(id=int(course_id))
            course_comment.comments=comments
            course_comment.course=course
            course_comment.user=request.user
            course_comment.save()
            result = {"status": "success", "msg": "添加成功 "}
            return HttpResponse(json.dumps(result), content_type='application/json')

        else:
            result = {"status": "fail", "msg": "添加失败"}
            return HttpResponse(json.dumps(result), content_type='application/json')




class VideoPlayView(LoginRequiredMixin,View):
    def get(self, request, video_id):
        video = Video.objects.get(id=int(video_id))

        course = video.lesson.course

        # user_courses = UserCourse.objects.filter(user=request.user, course=course)
        #
        # if not user_courses:
        #     user_courses = UserCourse(user=request.user, course=course)
        #     course.students += 1
        #     course.save(update_fields=["students"])
        #     user_courses.save()

        user_courses = UserCourse.objects.filter(course=course)
        user_ids = [user_course.user_id for user_course in user_courses]
        all_user_courses = UserCourse.objects.filter(user_id__in=user_ids)

        course_ids = [user_course.course_id for user_course in all_user_courses]
        # course_ids= list(set((course_ids)))  #去除重复课程ID
        relate_courses = Course.objects.filter(~Q(id=int(course.id)), id__in=course_ids).order_by("-click_nums")[:5]
        # print(relate_courses)

        all_resource = CourseResource.objects.filter(course=course)

        return render(request, "course-play.html",
                          {"course": course, "course_resources": all_resource, "relate_courses": relate_courses,"video":video})



