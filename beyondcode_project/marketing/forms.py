from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User

from .models import Page, Post, NavMenu, Footer, MediaAsset
from .widgets import GrapesJSAdminWidget


class PageForm(forms.ModelForm):
    blocks_json = forms.JSONField(
        widget=GrapesJSAdminWidget(
            options={
                'height': '600px',
                'width': 'auto',
                'storageManager': False,
                'plugins': [],
                'pluginsOpts': {},
            }
        ),
        required=False
    )

    class Meta:
        model = Page
        fields = [
            'title', 'slug', 'status', 'publish_at', 'unpublish_at',
            'seo_title', 'seo_description', 'og_title', 'og_description',
            'og_image', 'twitter_image', 'primary_image', 'primary_image_upload',
            'blocks_json',
        ]
        widgets = {
            'primary_image_upload': forms.ClearableFileInput(attrs={
                'accept': 'image/*'
            })
        }


class PostForm(forms.ModelForm):
    blocks_json = forms.JSONField(
        widget=GrapesJSAdminWidget(
            options={
                'height': '600px',
                'width': 'auto',
                'storageManager': False,
                'plugins': [],
                'pluginsOpts': {},
            }
        ),
        required=False
    )

    class Meta:
        model = Post
        fields = [
            'title', 'slug', 'status', 'publish_at', 'author_name', 'excerpt',
            'seo_title', 'seo_description', 'og_title', 'og_description',
            'og_image', 'twitter_image', 'primary_image', 'primary_image_upload',
            'cover_image', 'cover_image_upload', 'categories', 'tags', 'blocks_json',
        ]
        widgets = {
            'primary_image_upload': forms.ClearableFileInput(attrs={
                'accept': 'image/*'
            }),
            'cover_image_upload': forms.ClearableFileInput(attrs={
                'accept': 'image/*'
            }),
            'categories': forms.CheckboxSelectMultiple(),
            'tags': forms.CheckboxSelectMultiple(),
        }


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


class LoginForm(AuthenticationForm):
    """Custom login form with Bootstrap styling."""
    username = forms.CharField(
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Username or Email'
        })
    )
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={
            'class': 'form-control',
            'placeholder': 'Password'
        })
    )


class RegisterForm(UserCreationForm):
    """Custom registration form."""
    email = forms.EmailField(
        required=True,
        widget=forms.EmailInput(attrs={
            'class': 'form-control',
            'placeholder': 'Email address'
        })
    )

    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2')
        widgets = {
            'username': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Username'
            }),
            'password1': forms.PasswordInput(attrs={
                'class': 'form-control',
                'placeholder': 'Password'
            }),
            'password2': forms.PasswordInput(attrs={
                'class': 'form-control',
                'placeholder': 'Confirm Password'
            }),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Remove help texts
        self.fields['password1'].help_text = None
        self.fields['password2'].help_text = None
