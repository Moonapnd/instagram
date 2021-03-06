from django.db import models
from django.urls import reverse
from django.contrib.auth.models import User
from taggit.managers import TaggableManager
   

class Post(models.Model):
    title = models.CharField(max_length=250)
    image = models.ImageField(upload_to='post_images', blank=True, null=True) 
    # likes = models.IntegerField(default=0)
    # dislikes = models.IntegerField(default=0)
    liked = models.ManyToManyField(User, default=0, related_name='liked')
    tags = TaggableManager(blank=True)
    created_date = models.DateTimeField(auto_now_add=True)
    updated_date = models.DateTimeField(auto_now=True)
    """
    relationship: each user have multiple album_posts <--> each post belong to one publisher
    querysets: user.album_posts.all() <--> post.publisher
    """
    publisher = models.ForeignKey(User, on_delete=models.CASCADE, related_name='album_posts') 
    """
    relationship: each post have multiple comments <--> each comments belong to one post
    querysets: post.comments.all() <--> comment.post
    """

 
    def get_absolute_url(self):
        return reverse('albums:post_detail', kwargs={'pk': self.pk})
    
    class Meta:
        ordering = ('-updated_date', )

    def __str__(self):
        return self.title

    @property
    def num_likes(self):
        return self.liked.all().count()


LIKE_CHOICES = (
        ('Like', 'Like'),
        ('Unlike', 'Unlike'),
)

class Like(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE) 
    post = models.ForeignKey(Post, on_delete=models.CASCADE) 
    value = models.CharField(choices=LIKE_CHOICES, default='Like', max_length=10) 

    def __str__(self):
        return self.post


class Comment(models.Model):
    body = models.TextField()
    created_date = models.DateTimeField(auto_now_add=True)
    updated_date = models.DateTimeField(auto_now=True)
    """
    relationship: each user have multiple album_comments <--> each comment belong to one publisher
    querysets: user.album_comments.all() <--> comment.publisher
    """
    publisher = models.ForeignKey(User, on_delete=models.CASCADE, related_name='album_comments') 
    """
    relationship: each post have multiple comments <--> each comment belong to one post
    querysets: post.comments.all() <--> comment.post
    """
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='comments') 
    
    class Meta:
        ordering = ('-updated_date',)

    def __str__(self):
        return 'Comment on {}'.format(self.post)

