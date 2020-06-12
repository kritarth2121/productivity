from django.contrib import admin
from .models import Post,Views,Team,TeamMember

admin.site.register(Post)
admin.site.register(Team)
admin.site.register(TeamMember)
admin.site.register(Views)