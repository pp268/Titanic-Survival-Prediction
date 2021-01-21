from django.conf.urls import url
from .views import (
    SignupView,
    UserProfileView,
    LogoutView,
    LoginView,
    account_activation_sent,
    UpdateProfileView,
    activate
    )
from django.contrib.auth.views import(
    password_reset,
    password_reset_done,
    password_reset_confirm,
    password_reset_complete,
    )





urlpatterns=[
    url(r'^signup/$',SignupView,name='signup'),
    url(r'^login/$',LoginView,name='login'),
    url(r'^logout/$',LogoutView,name='logout'),
    url(r'^update_profile/$',UpdateProfileView ,name='update_profile'),
    url(r'^profile/$',UserProfileView,name='profile'),
    url(r'^account_activation_sent/$', account_activation_sent, name='account_activation_sent'),
    url(r'^activate/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/$',activate, name='activate'),
    url(r'^password_reset/$',password_reset, {'template_name':'accounts/password_reset_form.html'},name='password_reset'),
    url(r'^reset/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/$',password_reset_confirm, {'template_name':'accounts/password_reset_confirm.html'}, name='password_reset_confirm'),
    url(r'^password_reset/done/$',password_reset_done,{'template_name':'accounts/password_reset_done.html'},name='password_reset_done'),
    url(r'^reset/done/$',password_reset_complete, {'template_name':'accounts/password_reset_complete.html'},name='password_reset_complete'),

]
