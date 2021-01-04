from django.shortcuts import render

# Create your views here.


def videos(request):
    """ A view to return the videos page """
    # videos = Video.objects.all() 
    # context = {
    #     'videos' : videos
    # }
    # return render(request, 'users/videos.html', context)
    return render(request, 'users/videos.html')
