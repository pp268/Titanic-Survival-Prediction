from django.shortcuts import render,redirect
from django.core.urlresolvers import reverse
from django.contrib.auth import authenticate,login,logout
from .forms import SignUpForm,LoginForm,UserInfoForm
from django.http import HttpResponseRedirect,HttpResponse
from django.contrib.auth.models import User
from django import forms
from django.utils.encoding import force_bytes,force_text
from django.utils.http import urlsafe_base64_decode,urlsafe_base64_encode
from django.template.loader import render_to_string
from .tokens import account_activation_token
from django.contrib.sites.shortcuts import get_current_site
from django.core.mail import EmailMessage
from django.contrib.auth.decorators import login_required
from django.contrib import messages

# Create your views here.

def SignupView(request):
    if request.method=='POST':
        form=SignUpForm(request.POST)
        if form.is_valid():

            user=form.save(commit=False)
            user.is_active=False
            user.save()

            current_site=get_current_site(request)
            subject='Activate Your Social Account'
            message=render_to_string('accounts/account_activation_email.html',{
                'user':user,
                'domain':current_site.domain,
                'uid':urlsafe_base64_encode(force_bytes(user.pk)),
                'token':account_activation_token.make_token(user),
            })
            to_email=form.cleaned_data.get('email')
            email=EmailMessage(subject,message,to=[to_email])
            email.send()
            return redirect('accounts:account_activation_sent')
    else:

        form=SignUpForm()

    return render(request,'accounts/signup.html',{'form':form})

@login_required
def UpdateProfileView(request):
    form=UserInfoForm(instance=request.user.profile)
    if request.method=='POST':
        form=UserInfoForm(request.POST,request.FILES,instance=request.user.profile)
        if form.is_valid():
            form.save()
            #messages.success(request,f'Your account has been updated!')
            return HttpResponseRedirect(reverse('accounts:profile'))

    context={
        'form':form
    }

    return render(request,'accounts/profile_update.html',context)






def LoginView(request):
    form=LoginForm(request.POST or None)
    if request.method=='POST':
        if form.is_valid():
            username=form.cleaned_data.get('username')
            password=form.cleaned_data.get('password')
            user=authenticate(username=username,password=password)
            if user:
                if user.is_active:
                    login(request,user)
                    return HttpResponseRedirect(reverse('accounts:profile'))
            else:
                print("Someone tried to login and failed")
                print("Username:{} and Password {}".format(username,password))
                return HttpResponse("invalid login details")
    context={
        'form':form
    }
    return render(request,'accounts/login.html',context)


def LogoutView(request):
    logout(request)
    return HttpResponseRedirect(reverse("accounts:login"))

def UserProfileView(request):
    return render(request,'accounts/profile.html')


def account_activation_sent(request):
    return render(request,'accounts/account_activation_sent.html')



def activate(request,uidb64,token):
    try:
        uid=force_text(urlsafe_base64_decode(uidb64))
        user=User.objects.get(pk=uid)
    except (TypeError, ValueError,OverflowError,User.DoesNotExist):
        user=None

    if user is not None and account_activation_token.check_token(user,token):
        user.is_active=True
        user.save()

        user.backend = 'django.contrib.auth.backends.ModelBackend'
        login(request,user)
        return HttpResponseRedirect(reverse("accounts:login"))
    else:
        user.delete()
        return render(request,'accounts/account_activation_invalid.html')
