from django.shortcuts import render

from django.contrib.auth.decorators import login_required

@login_required(login_url='/accounts/login/')
def videos(request):
    """ A view to return the videos page """
    # videos = Video.objects.all() 
    # context = {
    #     'videos' : videos
    # }
    # return render(request, 'users/videos.html', context)
    return render(request, 'users/videos.html')
