from django import forms

from posts.models import Post, PostImages


class PostForm(forms.ModelForm):

    class Meta:
        model = Post
        fields = ('title', 'content')

    def clean_title(self):
        title = self.cleaned_data['title']
        if Post.objects.filter(title__exact=title):
            raise forms.ValidationError(f'Post with the title - "{title}" '
                                        f'already exists.')
        return title


class PostImageForm(forms.ModelForm):
    image = forms.ImageField(label='Image')

    class Meta:
        model = PostImages
        fields = ('name', 'image',)


class PostEditForm(forms.ModelForm):

    class Meta:
        model = Post
        fields = ('title', 'content')


ImageFormSet = forms.modelformset_factory(PostImages, PostImageForm, extra=4)
ImageEditFormSet = forms.inlineformset_factory(Post, PostImages,
                                               fields=('name', 'image'))
