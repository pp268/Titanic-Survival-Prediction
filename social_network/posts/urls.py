from django.conf.urls import url
from .views import(
    PostListView,
    PostDetailView,
    PostCreateView,
    PostUpdateView,
    PostDeleteView,
    )


urlpatterns=[
    url('^$',PostListView.as_view(),name='home'),
    url('^post/(?P<pk>\d+)/$',PostDetailView.as_view(),name='post-detail'),
    url('^new_post/$',PostCreateView.as_view(),name='post-create'),
    url('^post/(?P<pk>\d+)/update/$',PostUpdateView.as_view(),name='post-update'),
    url('^post/(?P<pk>\d+)/delete/$',PostDeleteView.as_view(),name='post-delete'),

]
