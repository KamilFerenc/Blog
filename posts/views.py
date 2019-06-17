from django.contrib import messages
from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator
from django.template.context import RequestContext
from django.shortcuts import get_object_or_404, redirect, render
from django.views import View

from posts.forms import ImageFormSet, PostForm, PostEditForm
from posts.models import Post, PostImages


class PostListView(View):

    def get_queryset(self):
        return Post.objects.all().order_by('-created')

    def get(self, request):
        queryset = self.get_queryset()
        paginator = Paginator(queryset, 5)
        page = request.GET.get('page')
        try:
            posts = paginator.get_page(page)
        except PageNotAnInteger:
            posts = paginator.get_page(1)
        except EmptyPage:
            posts = paginator.get_page(paginator.num_pages)
        context = {'posts': posts}
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
        post_form = PostForm()
        image_form = ImageFormSet(queryset=PostImages.objects.none())
        context = {'post_form': post_form,
                   'image_form': image_form}
        return render(request, 'post/create.html', context)

    def post(self, request):
        post_form = PostForm(request.POST)
        image_form = ImageFormSet(request.POST, request.FILES,
                                  queryset=PostImages.objects.none())
        if post_form.is_valid() and image_form.is_valid():
            post_form = post_form.save()
            for form in image_form.cleaned_data:
                if form.get('image'):
                    image = form['image']
                    name = form['name']
                    photo = PostImages(name=name, post=post_form, image=image)
                    photo.save()
            message = 'Your post has been saved correctly.'
            messages.success(request, message)
            return redirect(post_form.get_absolute_url())
        context = {'post_form': post_form,
                   'image_form': image_form}
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
