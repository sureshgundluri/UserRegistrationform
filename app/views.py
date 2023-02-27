from django.shortcuts import render
from app.models import *
from django.http import  HttpResponse,HttpResponseRedirect
from app.forms import *
from django.core.mail import send_mail
from django.contrib.auth import authenticate,logout,login
from django.urls import reverse

from django.contrib.auth.decorators import login_required
# Create your views here.
def Homepage(request):
    if request.session.get('username'):
        username=request.session.get('username')
        d={'username':username}
        return render(request,'Homepage.html',d)
    return render(request,'Homepage.html')
def Registration(request):
    uf=Userform()
    pf=Profileform()
    d={'uf':uf,'pf':pf}
    if request.method=='POST' and request.FILES:
        UFD=Userform(request.POST)
        PFD=Profileform(request.POST,request.FILES)
        if  UFD.is_valid() and PFD.is_valid():
            UFO=UFD.save(commit=False)
            password=UFD.cleaned_data['password']
            UFO.set_password(password)
            UFO.save()

            PFO=PFD.save(commit=False)
            PFO.profile_user=UFO
            PFO.save()

            # send_mail('registration of formate','thankyou for registration','@gmail.com',recipient_list=[UFO.email],fail_silently=False)
            return HttpResponse(' registration is successfully')




    return render(request,'Registration.html',d)


def user_login(request):
    if request.method=='POST':
        username=request.POST['un']
        password=request.POST['pw']
        user=authenticate(username=username,password=password)

        if user and user.is_active:
            login(request,user)
            request.session['username']=username
            return HttpResponseRedirect (reverse('Homepage'))
        else:
            return HttpResponse('y are nott authenticated user')
    return render(request,'user_login.html')


@login_required
def user_logout(request):
    logout(request)
    return HttpResponseRedirect(reverse(Homepage))