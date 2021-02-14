from django.shortcuts import render
from django.contrib.auth.models import User
from userProfile.models import profile

def home(request):
    userprofile = profile.objects.get(id=request.user.id)
    if request.user.is_authenticated:
        return render(request, 'home/home.html',{'profile': userprofile})
    else:
        return render(request, 'home/home.html')
def about(request):
    return render(request, 'home/about.html')