from django.contrib import messages
from django.shortcuts import get_object_or_404, redirect, render
from django.views import View

from posts.forms import PostForm, PostEditForm
from posts.models import Post


class PostListView(View):

    def get_queryset(self):
        return Post.objects.all()

    def get(self, request):
        queryset = self.get_queryset()
        context = {'posts': queryset}
        return render(request, 'list.html', context)


class PostDetailView(View):

    @property
    def get_object(self):
        id = self.kwargs.get('id')
        return get_object_or_404(Post, id=id)

    def get(self, request, id):
        post = self.get_object
        context = {'post': post}
        return render(request, 'post/detail.html', context)


class PostCreateView(View):

    def get(self, request):
        form = PostForm()
        context = {'form': form}
        return render(request, 'post/create.html', context)

    def post(self, request):
        form = PostForm(request.POST)
        if form.is_valid():
            post = form.save()
            message = 'Your post has been saved correctly.'
            messages.success(request, message)
            return redirect(post.get_absolute_url())
        context = {'form': form}
        return render(request, 'post/create.html', context)


class PostUpdateView(PostDetailView):

    def get(self, request, id):
        post = self.get_object
        form = PostForm(instance=post)
        context = {'form': form}
        return render(request, 'post/update.html', context)

    def post(self, request, id):
        form = PostEditForm(data=request.POST)
        if form.is_valid():
            post = form.save()
            message = 'Your post has been updated correctly.'
            messages.success(request, message)
            return redirect(post.get_absolute_url())
        else:
            message = 'Your post has not been updated correctly.'
            messages.success(request, message)


class PostDeleteView(PostDetailView):

    def get(self, request, id):
        post = self.get_object
        context = {'post': post}
        return render(request, 'post/delete.html', context)

    def post(self, request, id):
        post = self.get_object
        post.delete()
        message = 'Your post has been deleted successfully.'
        messages.success(request, message)
        return redirect('posts:list')
