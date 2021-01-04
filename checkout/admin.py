from django.contrib import admin
from .models import Order


class OrderAdmin(admin.ModelAdmin):
    readonly_fields = ('order_number', 'date', 'order_total'
                    , 'subscription_plan', 'stripe_pid')

    fields = ('order_number', 'date', 'full_name',
              'email', 'phone_number','postcode', 'town_or_city', 'street_address1',
              'street_address2','order_total','stripe_pid')

    list_display = ('order_number', 'date', 'full_name',
                    'order_total')

    ordering = ('-date',)


admin.site.register(Order, OrderAdmin)
