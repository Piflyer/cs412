'''
Author : Tim Nguyen
Email : tim7@bu.edu
Desc : Form management to upload post and images to the models.py
'''

from django import forms
from .models import *

class CreateProfileForm(forms.ModelForm):
    '''Create a profile form'''
    class Meta:
        model = Profile
        fields = ["username", "display_name", "bio_text", "profile_image_url"]

class CreatePostForm(forms.ModelForm):
    '''Create a form to add a post'''
    image_file = forms.ImageField(required=True)

    class Meta:
        '''associate this form with the model from our database'''
        model = Post
        fields = ['caption']
        
class UpdateProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields =["display_name", "profile_image_url", "bio_text"]

class UpdatePostForm(forms.ModelForm):
    image_file = forms.ImageField(required=False)
    class Meta:
        '''associate this form with the model from our database'''
        model = Post
        fields = ['caption']