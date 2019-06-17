from django.contrib import messages
from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator
from django.shortcuts import get_object_or_404, redirect, render
from django.views import View

from posts.forms import ImageFormSet, ImageEditFormSet, PostForm, PostEditForm
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
        context = {'post': post,
                   'images': post.images.all()}
        return render(request, 'post/detail.html', context)


class PostCreateView(View):

    def get(self, request):
        post_form = PostForm()
        image_form = ImageFormSet(queryset=PostImages.objects.none())
        context = {'post_form': post_form,
                   'image_form': image_form}
        return render(request, 'post/create.html', context)

    def post(self, request):
        post_form = PostForm(data=request.POST)
        image_form = ImageFormSet(request.POST, request.FILES,
                                  queryset=PostImages.objects.none())
        if post_form.is_valid() and image_form.is_valid():
            post = post_form.save()
            for form in image_form.cleaned_data:
                if form.get('image'):
                    image = form['image']
                    name = form['name']
                    photo = PostImages(name=name, post=post, image=image)
                    photo.save()
            message = 'Your post has been saved correctly.'
            messages.success(request, message)
            return redirect(post.get_absolute_url())
        context = {'post_form': post_form,
                   'image_form': image_form}
        return render(request, 'post/create.html', context)


class PostUpdateView(PostDetailView):

    def get(self, request, id):
        post = self.get_object
        post_form = PostEditForm(instance=post)
        image_form = ImageEditFormSet(instance=post)
        context = {'post_form': post_form,
                   'image_form': image_form}
        return render(request, 'post/update.html', context)

    def post(self, request, id):
        post = self.get_object
        post_form = PostEditForm(instance=post, data=request.POST)
        image_form = ImageEditFormSet(request.POST,
                                      request.FILES, instance=post)
        if post_form.is_valid() and image_form.is_valid():
            post = post_form.save()
            image_form.save()
            message = 'Your post has been updated correctly.'
            messages.success(request, message)
            return redirect(post.get_absolute_url())
        context = {'post_form': post_form,
                   'image_form': image_form}
        return render(request, 'post/update.html', context)


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
