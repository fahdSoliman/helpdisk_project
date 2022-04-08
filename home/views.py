from django.shortcuts import render
from django.contrib.auth.models import User
from userProfile.models import Profile

def home(request):
    return render(request, 'home/home.html')
    
def about(request):
    return render(request, 'home/about.html')



# default page [[not found]]
def default(request):
    return render(request, 'home/default.html')