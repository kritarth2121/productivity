from django import template
from django.contrib.auth.models import User
import datetime
register = template.Library()

########################
@register.filter
def get_user(username):
    try:
        user = User.objects.get(username__iexact=username)
    except User.DoesNotExist: 
        user = User.objects.none()
    print(123456)
    print(user)
    print(username)
    return user

@register.simple_tag
def get_today(request):
    print(123)
    print(int(datetime.datetime.now().hour))

    return int(datetime.datetime.now().hour)

#register.filter('get_user',get_user)