from django.shortcuts import (
    render, redirect, reverse, get_object_or_404, HttpResponse
)
from django.views.decorators.http import require_POST
from django.contrib import messages
from django.conf import settings

from .forms import OrderForm
from .models import Order

from subscriptions.models import SubscriptionPlan
#from profiles.models import UserProfile

import stripe
import json


@require_POST
def cache_checkout_data(request):
    try:
        pid = request.POST.get('client_secret').split('_secret')[0]
        stripe.api_key = settings.STRIPE_SECRET_KEY
        stripe.PaymentIntent.modify(pid, metadata={
            'bag': json.dumps(request.session.get('bag', {})),
            'save_info': request.POST.get('save_info'),
            'username': request.user,
        })
        return HttpResponse(status=200)
    except Exception as e:
        messages.error(request, ('Sorry, your payment cannot be '
                                 'processed right now. Please try '
                                 'again later.'))
        return HttpResponse(content=e, status=400)


def checkout(request):
    stripe_public_key = settings.STRIPE_PUBLIC_KEY
    stripe_secret_key = settings.STRIPE_SECRET_KEY

    if request.method == 'POST':
        # todo: need to get subscription_plan from request
        # bag = request.session.get('bag', {})
        subscription_plan = None #request #Product.objects.get(id=item_id)
        form_data = {
            'full_name': request.POST['full_name'],
            'email': request.POST['email'],
            'phone_number': request.POST['phone_number'],
            'country': request.POST['country'],
            'postcode': request.POST['postcode'],
            'town_or_city': request.POST['town_or_city'],
            'street_address1': request.POST['street_address1'],
            'street_address2': request.POST['street_address2'],
        }

        order_form = OrderForm(form_data)
        if order_form.is_valid():
            order = order_form.save(commit=False)
            pid = request.POST.get('client_secret').split('_secret')[0]
            order.stripe_pid = pid
            order.subscription_plan = subscription_plan
            order.save()
            
            # Save the info to the user's profile if all is well
            request.session['save_info'] = 'save-info' in request.POST
            return redirect(reverse('checkout_success',
                                    args=[order.order_number]))
        else:
            messages.error(request, ('Fel i formuläret'
                                     'Vänligen dubbelkolla informationen du angivit.'))
    else:
        # get subscription plan
        subscription_plan = SubscriptionPlan() #request.session.get('bag', {})
        subscription_plan.price = 100.00
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

        # Attempt to prefill the form with any info
        # the user maintains in their profile
        # if request.user.is_authenticated:
        #     try:
        #         profile = UserProfile.objects.get(user=request.user)
        #         order_form = OrderForm(initial={
        #             'full_name': profile.user.get_full_name(),
        #             'email': profile.user.email,
        #             'phone_number': profile.default_phone_number,
        #             'country': profile.default_country,
        #             'postcode': profile.default_postcode,
        #             'town_or_city': profile.default_town_or_city,
        #             'street_address1': profile.default_street_address1,
        #             'street_address2': profile.default_street_address2,
        #         })
        #     except UserProfile.DoesNotExist:
        #         order_form = OrderForm()
        # else:
            # order_form = OrderForm()
        order_form = OrderForm() # todo - remove when userprofile
    if not stripe_public_key:
        messages.warning(request, ('Stripe public key is missing. '
                                   'Did you forget to set it in '
                                   'your environment?'))

    template = 'checkout/checkout.html'
    context = {
        'order_form': order_form,
        'stripe_public_key': stripe_public_key,
        'client_secret': intent.client_secret,
    }

    return render(request, template, context)


def checkout_success(request, order_number):
    """
    Handle successful checkouts
    """
    save_info = request.session.get('save_info')
    order = get_object_or_404(Order, order_number=order_number)

    # if request.user.is_authenticated:
    #     profile = UserProfile.objects.get(user=request.user)
    #     # Attach the user's profile to the order
    #     order.user_profile = profile
    #     order.save()

    #     # Save the user's info
    #     if save_info:
    #         profile_data = {
    #             'default_phone_number': order.phone_number,
    #             'default_country': order.country,
    #             'default_postcode': order.postcode,
    #             'default_town_or_city': order.town_or_city,
    #             'default_street_address1': order.street_address1,
    #             'default_street_address2': order.street_address2,
    #             'default_county': order.county,
    #         }
    #         user_profile_form = UserProfileForm(profile_data, instance=profile)
    #         if user_profile_form.is_valid():
    #             user_profile_form.save()

    messages.success(request, f'Order successfully processed! \
        Your order number is {order_number}. A confirmation \
        email will be sent to {order.email}.')

    template = 'checkout/checkout_success.html'
    context = {
        'order': order,
    }

    return render(request, template, context)
