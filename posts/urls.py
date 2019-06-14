from django.conf.urls import url

from posts.views import DetailView, ListView

app_name = 'posts'

urlpatterns = [
    url(r'^$', ListView.as_view(), name='list'),
    url(r'^(?P<id>\d+)/$', DetailView.as_view(), name='detail'),

]
