'''
Author : Tim Nguyen
Email : tim7@bu.edu
Desc : Managing backend connections with a custom Profile model for user data and attribute for mock Instagram
'''
from django.db import models
from django.urls import reverse
from django.contrib.auth.models import User

# Create your models here.
class Profile(models.Model):
    ''' 
    Profile class for accessing Profiles has attributes:
    username, display_name, profile_image_url, bio_text, join_date
    '''
    username = models.TextField(blank=False)
    display_name = models.TextField(blank=False)
    profile_image_url = models.URLField(blank=False)
    bio_text = models.TextField(blank=False)
    join_date = models.DateTimeField(auto_now=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    
    def get_all_posts(self):
        '''return all posts'''
        post = Post.objects.filter(profile=self).order_by('-timestamp')
        return post
    
    def __str__(self):
        return f"{self.username}, created on {self.join_date}."
    
    def get_absolute_url(self):
        '''return the URL to display this profile'''
        return reverse('show_profile', kwargs={'pk': self.pk})
    
    def get_followers(self):
        '''
        List of followers
        '''
        follow = Follow.objects.filter(profile=self)
        return [follower.follower_profile for follower in follow]
    
    def get_num_followers(self):
        '''return the number of followers'''
        return len(self.get_followers())
    
    def get_following(self):
        '''
        List of following
        '''
        follow = Follow.objects.filter(follower_profile=self)
        return [follower.profile for follower in follow]

    def get_num_post(self):
        '''
        Num of Posts
        '''
        return len(self.get_all_posts())
    
    def get_num_following(self):
        '''return the number of following'''
        return len(self.get_following())
    
    def get_post_feed(self):
        '''gets posts from profiles that this user followed'''
        following = self.get_following()
        posts = Post.objects.filter(profile__in=following).order_by('-timestamp')
        return posts


class Post(models.Model):
    ''' 
    Post class for accessing post has attributes:
    profile, caption, timestamp, and also methods like get_all_photos, get_absolute_url
    '''
    profile = models.ForeignKey("Profile", on_delete=models.CASCADE)
    caption = models.TextField(blank=True)
    timestamp = models.DateTimeField(auto_now=True)
    
    def get_all_photos(self):
        ''' Load all the photos from the appropriate profile'''
        photos = Photo.objects.filter(post=self)
        return photos
    
    def get_absolute_url(self):
        '''get the post url'''
        return reverse('post', kwargs={'pk': self.pk})
    
    def get_likes(self):
        '''return all Likes on this post'''
        likes = Like.objects.filter(post=self)
        return likes

    def get_all_comments(self):
        '''return all Comments on this post, oldest first'''
        comments = Comment.objects.filter(post=self).order_by('-timestamp')
        return comments


    
    def __str__(self):
        return f"{self.caption}, created on {self.timestamp}."

class Photo(models.Model):
    ''' 
    Photo class for accessing photo has attributes:
    post, image_url, image_file, and timestamp also methods like get_image_url
    '''
    post = models.ForeignKey("Post", on_delete=models.CASCADE)
    image_url = models.URLField(blank=True)
    image_file = models.ImageField(blank=True)
    timestamp = models.DateTimeField(auto_now=True)
    
    def get_image_url(self):
        '''Get image url, loads the image based on if its a file or a url'''
        if self.image_file:
            return self.image_file.url
        return self.image_url
    
    def __str__(self):
        if self.image_file:
            return f"{self.image_file.url}, created on {self.timestamp}."
        return f"{self.image_url}, created on {self.timestamp}."

class Follow(models.Model):
    '''Follow model relating follower to following'''
    profile = models.ForeignKey("Profile", on_delete=models.CASCADE, related_name="profile")
    follower_profile = models.ForeignKey("Profile", on_delete=models.CASCADE,related_name="follower_profile")
    timestamp = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"{self.profile}, followed by {self.follower_profile}."

class Comment(models.Model):
    '''Linking coments to post and who posted them'''
    post = models.ForeignKey("Post", on_delete=models.CASCADE)
    profile = models.ForeignKey("Profile", on_delete=models.CASCADE)
    timestamp = models.DateTimeField(auto_now=True)
    text = models.TextField(blank=True)
    
    def __str__(self):
        return f"{self.profile}, commented on {self.post}."

class Like(models.Model):
    '''Mapping likes to people'''
    post = models.ForeignKey("Post", on_delete=models.CASCADE)
    profile = models.ForeignKey("Profile", on_delete=models.CASCADE)
    timestamp = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"{self.profile}, liked {self.post}."
