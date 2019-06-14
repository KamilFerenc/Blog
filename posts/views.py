from django.shortcuts import render, get_object_or_404
from django.views import View

from posts.models import Post


class ListView(View):

    queryset = Post.objects.all()

    def get(self, request):
        context = {'posts': self.queryset}
        return render(request, 'list.html', context)


class DetailView(View):

    def get(self, request, id):
        post = get_object_or_404(Post, id=id)
        print(post)
        context = {'post': post}
        return render(request, 'post/detail.html', context)

    def update(self, request):
        pass

    def delete(self, request):
        pass
