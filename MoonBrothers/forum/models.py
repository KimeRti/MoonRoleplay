from django.contrib.auth.models import User
from django.db import models


class Category(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()
    picture = models.ImageField(upload_to='category/', blank=True)

    def __str__(self):
        return self.name

    def topic_count(self):
        return self.posts.count()

    def comment_count(self):
        total_comments = 0
        for post in self.posts.all():
            total_comments += post.comments.count()
        return total_comments


class Post(models.Model):
    STATUS_CHOICES = [
        ('approved', 'Onaylanmış'),
        ('rejected', 'Reddedilmiş'),
        ('pending', 'Beklemede'),
    ]
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    title = models.CharField(max_length=250)
    content = models.TextField(max_length=700)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='posts')
    photo = models.ImageField(upload_to='posts/', blank=True, null=True)
    pub_date = models.DateTimeField(auto_now_add=True, blank=True, null=True, editable=False)
    modified_date = models.DateTimeField(auto_now=True, blank=True, null=True)

    def __str__(self):
        return self.title


class Comment(models.Model):
    content = models.TextField(max_length=700)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='comments')
    pub_date = models.DateTimeField(auto_now_add=True, blank=True, null=True, editable=False)
    modified_date = models.DateTimeField(auto_now=True, blank=True, null=True)

    def __str__(self):
        return f"{self.author.username} - {self.post.title}"
