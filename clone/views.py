from django.shortcuts import render, get_object_or_404
from .models import User

# Create your views here.

def index(request):
    if request.POST:
        # try:
        e = request.POST['email']
        u = get_object_or_404(User, email = e)
        print(u.password) 
        # except (KeyError, User.DoesNotExist) :
        #     return render(request, "login.html", {
        #         'error_message': "Invalid username !!!"
        #         }
        #     ) 
        return render(request, "index.html", {})
    else:
        return render(request, "index.html", {})

def login(request):
    if request.POST:
        print(request.POST)
        a = User(username = request.POST['username'], email = request.POST['email'], firstname = request.POST['firstname'], lastname = request.POST['lastname'], password = request.POST['password'], plan = request.POST['plan'])
        a.save()
    return render(request, "login.html", {})

def signup(request):
    return render(request, "sign-up.html", {})