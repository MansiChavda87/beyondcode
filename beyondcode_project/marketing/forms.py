from django import forms
from django_editorjs import EditorJsField

from .models import Page, Post, NavMenu, Footer, MediaAsset


class PageForm(forms.ModelForm):
    body_json = EditorJsField(blank=True, null=True)
    blocks_json = EditorJsField(blank=True, null=True)

    class Meta:
        model = Page
        fields = [
            'title', 'slug', 'status', 'publish_at', 'unpublish_at',
            'seo_title', 'seo_description', 'og_title', 'og_description',
            'og_image', 'twitter_image', 'primary_image', 'primary_image_upload',
            'body_json', 'blocks_json',
        ]
        widgets = {
            'primary_image_upload': forms.ClearableFileInput(attrs={
                'accept': 'image/*'
            })
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # body_json is kept in the form for backward compat but hidden;
        # all content now lives in blocks_json via rich_text blocks.
        self.fields['body_json'].required = False
        self.fields['body_json'].widget = forms.HiddenInput()


class PostForm(forms.ModelForm):
    body_json = EditorJsField(blank=True, null=True)
    blocks_json = EditorJsField(blank=True, null=True)

    class Meta:
        model = Post
        fields = [
            'title', 'slug', 'status', 'publish_at', 'author_name', 'excerpt',
            'seo_title', 'seo_description', 'og_title', 'og_description',
            'og_image', 'twitter_image', 'primary_image', 'primary_image_upload',
            'cover_image', 'cover_image_upload', 'categories', 'tags', 'body_json', 'blocks_json',
        ]
        widgets = {
            'primary_image_upload': forms.ClearableFileInput(attrs={
                'accept': 'image/*'
            }),
            'cover_image_upload': forms.ClearableFileInput(attrs={
                'accept': 'image/*'
            })
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['body_json'].required = False
        self.fields['body_json'].widget = forms.HiddenInput()


class NavMenuForm(forms.ModelForm):
    class Meta:
        model = NavMenu
        fields = ['name', 'items_json']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['name'].widget = forms.HiddenInput()
        if not self.instance or not self.instance.name:
            self.initial['name'] = 'Primary'


class FooterForm(forms.ModelForm):
    class Meta:
        model = Footer
        fields = [
            'label', 'columns_json', 'cta_title', 'cta_body',
            'cta_button_label', 'cta_button_url', 'legal_text',
        ]


class MediaAssetForm(forms.ModelForm):
    class Meta:
        model = MediaAsset
        fields = [
            'file', 'file_upload', 'alt_text', 'caption', 'width', 'height', 'content_type'
        ]
        widgets = {
            'file_upload': forms.ClearableFileInput(attrs={
                'accept': 'image/*,video/*,audio/*,.pdf,.doc,.docx,.txt,.zip,.rar'
            })
        }

    def clean(self):
        cleaned_data = super().clean()
        file = cleaned_data.get('file')
        file_upload = cleaned_data.get('file_upload')
        
        if not file and not file_upload:
            raise forms.ValidationError('Please provide either a URL or upload a file.')
        
        if file and file_upload:
            raise forms.ValidationError('Please provide either a URL or upload a file, not both.')
        
        return cleaned_data
