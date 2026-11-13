'''
Author : Tim Nguyen
Email : tim7@bu.edu
Desc : Serializers to convert Jokes and Picture models to JSON for the REST API
'''
from django.utils import timezone
from rest_framework import serializers
from .models import Jokes, Picture


class JokeSerializer(serializers.ModelSerializer):
    '''
    A serializer for the Jokes model.
    Specify which model/fields to send in the API.
    '''
    class Meta:
        model = Jokes
        fields = ['id', 'jokes', 'contributor', 'timestamp']
        read_only_fields = ['timestamp']

    def create(self, validated_data):
        '''
        Override the superclass method that handles object creation.
        Sets the timestamp automatically.
        '''
        print(f'JokeSerializer.create, validated_data={validated_data}.')
        validated_data['timestamp'] = timezone.now()
        return Jokes.objects.create(**validated_data)


class PictureSerializer(serializers.ModelSerializer):
    '''
    A serializer for the Picture model.
    '''
    class Meta:
        model = Picture
        fields = ['id', 'image_url', 'contributor', 'timestamp']
