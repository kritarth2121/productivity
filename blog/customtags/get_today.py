from django import template
from django.contrib.auth.models import User
import datetime
from django.db.models.functions import datetime
register = template.Library()

@register.filter
def get_today(request):
    print(sdfg)
    print(int(datetime.datetime.now().hour))


    return int(datetime.datetime.now().hour)