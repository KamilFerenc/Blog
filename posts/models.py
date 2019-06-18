from django.db import models
from django.db.models.signals import pre_save
from django.dispatch import receiver
from django.urls import reverse
from django.utils.text import slugify


class Post(models.Model):
    title = models.CharField(max_length=120)
    slug = models.SlugField(unique=True)
    content = models.TextField()
    updated = models.DateTimeField(auto_now=True, auto_now_add=False)
    created = models.DateTimeField(auto_now=False, auto_now_add=True)

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('posts:detail', kwargs={'slug': self.slug})

    @staticmethod
    def create_slug(instance):
        slug = slugify(instance.title)
        qs = Post.objects.filter(slug=slug)
        exists = qs.exists()
        if exists:
            # instance_id = last created post.id + 1
            instance_id = Post.objects.last().id + 1
            slug = f'{slug}-{instance_id}'
        return slug


@receiver(pre_save, sender=Post)
def pre_save_post_receiver(sender, instance, *args, **kwargs):
    instance.slug = Post.create_slug(instance)


def get_image_filename(instance, filename):
    id = instance.post.id
    return f'post_images/{id}/{filename}'


class PostImages(models.Model):
    name = models.CharField(max_length=30, blank=True)
    post = models.ForeignKey(Post, default=None,
                             on_delete=models.CASCADE, related_name='images')
    image = models.ImageField(upload_to=get_image_filename)
