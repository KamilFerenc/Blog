from django.conf.urls import url

from posts.views import (
    PostCreateView,
    PostDeleteView,
    PostDetailView,
    PostListView,
    PostUpdateView
)


app_name = 'posts'

urlpatterns = [
    url(r'^$', PostListView.as_view(), name='list'),
    url(r'^create/$', PostCreateView.as_view(), name='create'),
    url(r'^(?P<slug>[-\w\d]+)/$', PostDetailView.as_view(), name='detail'),
    url(r'^(?P<slug>[-\w\d]+)/edit/$', PostUpdateView.as_view(), name='update'),
    url(r'^(?P<slug>[-\w\d]+)/delete/$', PostDeleteView.as_view(), name='delete'),

]
