from django.shortcuts import redirect, render
import datetime

from django.contrib.auth.decorators import login_required
from django.urls import reverse


@login_required(login_url='/accounts/login/')
def videos(request):
    """ A view to return the videos page for only logged in and valid user"""
    if request.user.profile.valid_until is None or request.user.profile.valid_until < datetime.date.today():
        return redirect(reverse('account_login'))
    # videos = Video.objects.all() 
    # context = {
    #     'videos' : videos
    # }
    # return render(request, 'users/videos.html', context)
    return render(request, 'users/videos.html')
