from django import forms

from .models import Page, Post, NavMenu, Footer


class PageForm(forms.ModelForm):
    class Meta:
        model = Page
        fields = [
            'title', 'slug', 'status', 'publish_at', 'unpublish_at',
            'seo_title', 'seo_description', 'og_title', 'og_description',
            'og_image', 'twitter_image', 'primary_image',
            'body_json', 'blocks_json',
        ]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # body_json is kept in the form for backward compat but hidden;
        # all content now lives in blocks_json via rich_text blocks.
        self.fields['body_json'].required = False
        self.fields['body_json'].widget = forms.HiddenInput()


class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = [
            'title', 'slug', 'status', 'publish_at', 'author_name', 'excerpt',
            'seo_title', 'seo_description', 'og_title', 'og_description',
            'og_image', 'twitter_image', 'primary_image', 'cover_image',
            'categories', 'tags', 'body_json', 'blocks_json',
        ]

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