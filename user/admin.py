from django.contrib import admin
from user.models import Profile, CustomUser, Tournament, Game

admin.site.register(Profile)
admin.site.register(CustomUser)
admin.site.register(Game)
admin.site.register(Tournament)
