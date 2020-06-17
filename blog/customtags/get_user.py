from django import template
from django.contrib.auth.models import User

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

#register.filter('get_user',get_user)