from django.contrib import admin
from .models import Profile

class ProfileAdmin(admin.ModelAdmin):
    readonly_fields = ('user',)
    fields = ('valid_until',)

admin.site.register(Profile, ProfileAdmin)
