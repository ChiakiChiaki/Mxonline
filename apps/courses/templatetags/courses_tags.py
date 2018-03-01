from courses.models import Course
from django import template

register=template.Library()

@register.simple_tag()
def get_click_course(num=3):
    return Course.objects.all().order_by("-click_nums")[:num]