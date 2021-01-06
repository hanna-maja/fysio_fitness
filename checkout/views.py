from django.shortcuts import (
    render, redirect, reverse, get_object_or_404, HttpResponse
)
from django.contrib import messages
from django.conf import settings

from .forms import OrderForm
from .models import Order
from django.contrib.auth.models import User
from django.contrib.auth import login

from subscriptions.models import SubscriptionPlan

import stripe
from stripe.api_resources.payment_intent import PaymentIntent
import datetime


def checkout(request):
    """ A view to return the checkout page and handle logic for payment"""
    stripe_public_key = settings.STRIPE_PUBLIC_KEY
    stripe_secret_key = settings.STRIPE_SECRET_KEY

    if request.method == 'POST':
        plan_id = request.POST['plan_id']
        subscription_plan = SubscriptionPlan.objects.get(id=plan_id)
        email = request.POST['email']
        password = request.POST['password']
        form_data = {
            'full_name': request.POST['full_name'],
            'email': email,
            'phone_number': request.POST['phone_number'],
            'password': password,
        }

        order_form = OrderForm(form_data)
        if order_form.is_valid():
            order = order_form.save(commit=False)
            pid = request.POST.get('client_secret').split('_secret')[0]
            order.stripe_pid = pid
            order.subscription_plan = subscription_plan
            order.save()

            redirect_string = 'videos'
            try:
                user = User.objects.get(username=email)
                if not request.user.is_authenticated:
                    redirect_string = 'account_login'
            except:
                user = User.objects.create_user(email, email, password)
                login(request, user, 'allauth.account.auth_backends.AuthenticationBackend')

            # add days to user valid
            days = subscription_plan.days
            if user.profile.valid_until is None or user.profile.valid_until < datetime.date.today():
                user.profile.valid_until = datetime.date.today() + datetime.timedelta(days=days)
            else:
                user.profile.valid_until = user.profile.valid_until + datetime.timedelta(days=days)
            user.save()

            return redirect(reverse(redirect_string))
        else:
            intent = PaymentIntent()
            intent.client_secret = request.POST.get('client_secret')
            total = subscription_plan.price
            messages.error(request, ('Fel i formuläret'
                                     'Vänligen dubbelkolla informationen du angivit.'))
    else:
        # get subscription plan
        plan_id = request.GET.get('plan_id', '')
        subscription_plan = SubscriptionPlan.objects.get(id=plan_id)
        if not subscription_plan:
            messages.error(request,
                           "Du måste välja en plan för att checka ut")
            return redirect(reverse('subscriptions'))

        total = subscription_plan.price
        stripe_total = round(total * 100)
        stripe.api_key = stripe_secret_key
        intent = stripe.PaymentIntent.create(
            amount=stripe_total,
            currency=settings.STRIPE_CURRENCY,
        )
        order_form = OrderForm() 
    if not stripe_public_key:
        messages.warning(request, ('Stripe public key is missing. '
                                   'Did you forget to set it in '
                                   'your environment?'))

    template = 'checkout/checkout.html'
    context = {
        'order_form': order_form,
        'stripe_public_key': stripe_public_key,
        'client_secret': intent.client_secret,
        'plan_id': plan_id,
        'total_price': total
    }

    return render(request, template, context)
