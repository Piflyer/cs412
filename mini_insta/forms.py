'''
Author : Tim Nguyen
Email : tim7@bu.edu
Desc : Form management to upload post and images to the models.py
'''

from django import forms
from .models import *

class CreatePostForm(forms.ModelForm):
    '''Create a form to add a post'''
    image_url = forms.URLField(required=False)

    class Meta:
        '''associate this form with the model from our database'''
        model = Posts
        fields = ['caption']
        
    