from django import forms
from blog.models import BlogPost, Category
from ckeditor_uploader.widgets import CKEditorUploadingWidget
from django.conf import settings
from PIL import Image
from toolbelt.utils import (
    get_user_directory_thumbnail_path,
    )


class BlogPostForm(forms.ModelForm):
    blog_title = forms.CharField(widget=forms.TextInput(attrs={"class": "save"}))
    blog_subtitle = forms.CharField(widget=forms.TextInput(attrs={"class": "save"}))
    banner_image_source = forms.CharField(widget=forms.TextInput(attrs={"placeholder": "Ex: Picture taken by @JohnDoe", "class": "save"}))
    content = forms.CharField(widget=CKEditorUploadingWidget())
    blog_category = forms.ChoiceField(widget=forms.Select(attrs={"class": "save"}), choices=[(cat.id, cat.category_name) for cat in Category.objects.all()])
    # blog_tags = forms.CharField(widget=forms.TextInput(attrs={"data-role": "tagsinput", "class": "form-control"}))

    class Meta:
        model = BlogPost
        widgets = {
            'banner_image': forms.ClearableFileInput(attrs={'class': 'save'}),
        }
        exclude = ('blog_author', 'blog_slug', 'created_on', 'updated_on', 'moderator_accepted', 'published', 'draft', 'preview')

    def clean_blog_category(self):
        category = self.cleaned_data["blog_category"]
        try:
            category = Category.objects.get(id=category)
            return category
        except Exception:
            return None
