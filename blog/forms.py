from django import forms
from blog.models import BlogPost, Category, Tag
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
    blog_tags = forms.ChoiceField(widget=forms.Select(attrs={"class": "save select2", "multiple": "multiple"}), choices=[(tag.id, tag.tag_name) for tag in Tag.objects.all()])

    class Meta:
        model = BlogPost
        widgets = {
            'banner_image': forms.ClearableFileInput(attrs={'class': 'save'}),
        }
        exclude = ('blog_author', 'blog_slug', 'created_on', 'updated_on', 'moderator_accepted', 'published', 'draft', 'preview')

    def clean_blog_category(self):
        blog_category = Category.objects.get(id=self.cleaned_data["blog_category"])
        return blog_category

    def clean_banner_image(self):
        banner_image = self.cleaned_data["banner_image"]
        print(banner_image)
        return banner_image


class BlogPostEditForm(forms.ModelForm):
    blog_title = forms.CharField(widget=forms.TextInput(attrs={"class": "save"}))
    blog_subtitle = forms.CharField(widget=forms.TextInput(attrs={"class": "save"}))
    banner_image_source = forms.CharField(widget=forms.TextInput(attrs={"placeholder": "Ex: Picture taken by @JohnDoe", "class": "save"}))
    content = forms.CharField(widget=CKEditorUploadingWidget())
    blog_category = forms.ChoiceField(widget=forms.Select(attrs={"class": "save"}), choices=[(cat.id, cat.category_name) for cat in Category.objects.all()])
    blog_tags = forms.ChoiceField(widget=forms.Select(attrs={"class": "save", "multiple": "multiple"}), choices=[(tag.id, tag.tag_name) for tag in Tag.objects.all()])

    class Meta:
        model = BlogPost
        widgets = {
            'banner_image': forms.ClearableFileInput(attrs={'class': 'save'}),
        }
        exclude = ('blog_author', 'blog_slug', 'created_on', 'updated_on', 'moderator_accepted', 'published', 'draft', 'preview')

    def clean_blog_category(self):
        blog_category = Category.objects.get(id=self.cleaned_data["blog_category"])
        return blog_category

    def clean_banner_image(self):
        banner_image = self.cleaned_data["banner_image"]
        print("banner Image in the edit form: ", banner_image)

        return banner_image
