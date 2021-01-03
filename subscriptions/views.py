from django.shortcuts import render
from .models import SubscriptionPlan

# Create your views here.


def index(request):
    """ A view to return the index page """
    plans = SubscriptionPlan.objects.all() 
    context = {
        'plans' : plans
    }
    return render(request, 'subscriptions/index.html', context)
