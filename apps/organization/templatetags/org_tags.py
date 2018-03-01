#Author:Sun Jian

from organization.models import CourseOrg,Teacher
from django import template

register=template.Library()

@register.simple_tag()
def get_click_courseorg(num=3):
    return CourseOrg.objects.all().order_by("-click_num")[:num]


@register.simple_tag()
def get_click_teacher(num=3):
    return Teacher.objects.all().order_by("-click_num")[:num]


