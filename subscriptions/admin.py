from django.contrib import admin
from django.contrib.contenttypes.admin import GenericTabularInline
from .models import SubscriptionPlan

# Register your models here.

class SubscriptionPlanAdmin(admin.ModelAdmin):
    readonly_fields = ('plan_id',)
    fields = ('name', 'description', 'price', 'days', 'image')

admin.site.register(SubscriptionPlan, SubscriptionPlanAdmin)