from django import forms

from posts.models import Post


class PostForm(forms.ModelForm):

    class Meta:
        model = Post
        fields = ('title', 'content')

    def clean_title(self):
        title = self.cleaned_data['title']
        if Post.objects.filter(title__exact=title):
            raise forms.ValidationError(f'Post with that title - "{title}" '
                                        f'already exists.')
        return title


class PostEditForm(forms.ModelForm):

    class Meta:
        model = Post
        fields = ('title', 'content')
