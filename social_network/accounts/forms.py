from django import forms
from django.contrib.auth import authenticate
from django.contrib.auth.forms import UserCreationForm,UserChangeForm
from django.contrib.auth.models import User
from .models import GENDER_CHOICES,Profile



class SignUpForm(UserCreationForm):

    username = forms.CharField(label="Username*",widget=forms.TextInput(attrs={ 'autofocus':'on','autocomplete':'off', 'class':'form-control', 'placeholder':'Username', "required":"required"}))
    first_name = forms.CharField(label="First Name*",widget=forms.TextInput(attrs={ 'autocomplete':'off', 'class':'form-control', 'placeholder':'First Name', "required":"required"}))
    last_name = forms.CharField(label="Last Name",required=False,widget=forms.TextInput(attrs={'autocomplete':'off', 'class':'form-control', 'placeholder':'Last Name',}))
    email = forms.EmailField(label="Email*",required=True,widget=forms.EmailInput(attrs={'autocomplete':'off', 'class':'form-control', 'placeholder':'Email',"required":"required"}))
    password1 = forms.CharField(label="" , widget=forms.PasswordInput(attrs={'autocomplete':'off','class':'form-control', 'placeholder':'Password'}))
    password2 = forms.CharField(label="" , widget=forms.PasswordInput(attrs={'autocomplete':'off','class':'form-control', 'placeholder':'Confirm Password'}))

    class Meta:
        model=User
        fields=('username','first_name','last_name','email','password1','password2')
    # def clean_email(self):
    #     email=self.cleaned_data.get('email')
    #     if len(User.objects.filter(email=email)):
    #         raise forms.ValidationError("Email Already Exist!")
    #     return email



class UserInfoForm(forms.ModelForm):
    dob = forms.DateField(label="Date of birth*", widget=forms.SelectDateWidget(years=range(1990, 2010), attrs={'class':'form-control'}))
    gender = forms.CharField(required=False,label="Gender*", widget=forms.RadioSelect(choices=GENDER_CHOICES,attrs={'class':'form-sontrol'}))
    about = forms.CharField(required=False,label="",widget=forms.TextInput(attrs={'autofocus':'off', 'autocomplete':'off', 'class':'form-control', 'placeholder':'Tell something about yourself...'}))
    city = forms.CharField(required=False,label="",widget=forms.TextInput(attrs={'autofocus':'off', 'autocomplete':'off', 'class':'form-control', 'placeholder':'Where you live?'}))
    work = forms.CharField(required=False,label="",widget=forms.TextInput(attrs={'autofocus':'off', 'autocomplete':'off', 'class':'form-control', 'placeholder':'Your profession'}))
    profile_pic=forms.ImageField(required=False,widget=forms.FileInput(attrs={'class':'form-control'}))
    class Meta:
        model=Profile
        fields=('about','dob','gender','city','work','profile_pic')

class LoginForm(forms.Form):
    username=forms.CharField(label="", widget=forms.TextInput(attrs={'autocomplete':'off','autofocus':'on','class':'form-control', 'placeholder':'Username'}))
    password = forms.CharField(label="" , widget=forms.PasswordInput(attrs={'autocomplete':'off','class':'form-control', 'placeholder':'Password'}))

    def clean_username(self):
        username=self.cleaned_data.get('username')
        if len(User.objects.filter(username=username))==0:
            raise forms.ValidationError("Username does not Exist")
        return username
    def clean_password(self):
        username=self.cleaned_data.get("username")
        password=self.cleaned_data.get("password")
        user = authenticate(username=username,password=password)
        if user is None:
            raise forms.ValidationError("Wrong Username or Password")
        return password
