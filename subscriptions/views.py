from django.shortcuts import render
from .models import SubscriptionPlan


def index(request):
    """ A view to return the index page for different subscription plans"""
    plans = SubscriptionPlan.objects.all() 
    context = {
        'plans' : plans
    }
    return render(request, 'subscriptions/index.html', context)
