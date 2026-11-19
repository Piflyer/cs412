'''
Author : Tim Nguyen
Email : tim7@bu.edu
Desc : Serializers to convert mini_insta models to JSON for the REST API
'''
from rest_framework import serializers
from .models import Profile, Post, Photo, Follow, Like, Comment, User


def get_viewer(serializer):
    '''
    Return the Profile id of whoever is "logged in" in the app,
    passed as ?viewer=<id> on the request (no authentication yet).
    '''
    request = serializer.context.get('request')
    if request is None:
        return None
    return request.query_params.get('viewer')


class PhotoSerializer(serializers.ModelSerializer):
    '''Serializer for Photo; exposes a single usable image URL.'''
    image = serializers.SerializerMethodField()

    class Meta:
        model = Photo
        fields = ['id', 'post', 'image', 'timestamp']

    def get_image(self, obj):
        '''Return the file URL or the external URL, whichever exists.'''
        return obj.get_image_url()


class PostSerializer(serializers.ModelSerializer):
    '''
    Serializer for Post, with its photos nested.
    On create, accepts an optional image_url or image_file to attach a Photo.
    '''
    photos = serializers.SerializerMethodField()
    num_likes = serializers.SerializerMethodField()
    num_comments = serializers.SerializerMethodField()
    liked = serializers.SerializerMethodField()
    image_url = serializers.URLField(write_only=True, required=False)
    image_file = serializers.ImageField(write_only=True, required=False)

    class Meta:
        model = Post
        fields = ['id', 'profile', 'caption', 'timestamp', 'photos',
                  'num_likes', 'num_comments', 'liked', 'image_url', 'image_file']
        read_only_fields = ['timestamp']

    def get_photos(self, obj):
        '''Return all photos for this post.'''
        return PhotoSerializer(obj.get_all_photos(), many=True).data

    def get_num_likes(self, obj):
        '''Return the number of likes on this post.'''
        return obj.get_likes().count()

    def get_num_comments(self, obj):
        '''Return the number of comments on this post.'''
        return obj.get_all_comments().count()

    def get_liked(self, obj):
        '''Return True if the viewer has liked this post.'''
        viewer = get_viewer(self)
        return bool(viewer) and Like.objects.filter(post=obj, profile_id=viewer).exists()

    def create(self, validated_data):
        '''Create the Post, then a Photo from the image_url or image_file.'''
        print(f'PostSerializer.create, validated_data={validated_data}.')
        image_url = validated_data.pop('image_url', None)
        image_file = validated_data.pop('image_file', None)
        post = Post.objects.create(**validated_data)
        if image_file:
            Photo.objects.create(post=post, image_file=image_file)
        elif image_url:
            Photo.objects.create(post=post, image_url=image_url)
        return post


class ProfileSerializer(serializers.ModelSerializer):
    '''Serializer for Profile.'''
    num_posts = serializers.SerializerMethodField()
    num_followers = serializers.SerializerMethodField()
    num_following = serializers.SerializerMethodField()
    is_following = serializers.SerializerMethodField()

    class Meta:
        model = Profile
        fields = ['id', 'username', 'display_name', 'profile_image_url',
                  'bio_text', 'join_date', 'num_posts', 'num_followers',
                  'num_following', 'is_following']
        read_only_fields = ['username', 'join_date']

    def get_num_posts(self, obj):
        '''Returns number of post'''
        return obj.get_num_post()

    def get_num_followers(self, obj):
        '''Returns number of followers'''
        return obj.get_num_followers()

    def get_num_following(self, obj):
        '''Retruns the number of following'''
        return obj.get_num_following()

    def get_is_following(self, obj):
        '''Return True if the viewer follows this profile.'''
        viewer = get_viewer(self)
        return bool(viewer) and Follow.objects.filter(
            profile=obj, follower_profile_id=viewer).exists()


class CommentSerializer(serializers.ModelSerializer):
    '''Serializer for Comment, including who wrote it.'''
    username = serializers.CharField(source='profile.username', read_only=True)
    profile_image_url = serializers.CharField(source='profile.profile_image_url', read_only=True)

    class Meta:
        model = Comment
        fields = ['id', 'post', 'profile', 'username', 'profile_image_url', 'text', 'timestamp']
        read_only_fields = ['post', 'timestamp']

class UserSerializer(serializers.ModelSerializer):
    ''' Seralizer for user login'''
    password = serializers.CharField(write_only=True)
    
    class Meta:
        model = User
        fields = ['username', 'password', 'email']

    def create(self, validated_data):
        '''Validate User input'''
        user = User.objects.create_user(
            username=validated_data['username'],
            password=validated_data['password'],
            email=validated_data.get('email')
        )
        return user

