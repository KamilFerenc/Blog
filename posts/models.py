from django.db import models
from django.urls import reverse


class Post(models.Model):
    title = models.CharField(max_length=120)
    content = models.TextField()
    updated = models.DateTimeField(auto_now=True, auto_now_add=False)
    created = models.DateTimeField(auto_now=False, auto_now_add=True)

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('posts:detail', kwargs={'id': self.id})


def get_image_filename(instance, filename):
    id = instance.post.id
    return f'post_images/{id}/{filename}'


class PostImages(models.Model):
    name = models.CharField(max_length=30, blank=True)
    post = models.ForeignKey(Post, default=None,
                             on_delete=models.CASCADE, related_name='images')
    image = models.ImageField(upload_to=get_image_filename)



