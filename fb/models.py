from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MinValueValidator, MaxValueValidator, RegexValidator


class MyProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    address = models.TextField()
    age = models.IntegerField(default=18, null=True, blank=True)
    description = models.TextField()
    profile_pic = models.ImageField(upload_to = 'images/profiles')
    phone = models.CharField(validators=[RegexValidator('0?[6-9]{1}\d{9}$')], max_length=15, null=True, blank=True)
    status = models.CharField(max_length=10, default = 'single', choices = (('single', 'single'), ('divorced', 'divorced'), ('married', 'married')) )
    gender = models.CharField(max_length=10, default='male', choices=(('male', 'male'), ('female', 'female')))

    def __str__(self):
        return '%s'%self.user

class MyPost(models.Model):
    pic = models.ImageField(upload_to='images/posts')
    subject = models.CharField(max_length=200)
    msg = models.TextField(null=True, blank=True)
    cr_date = models.DateTimeField(auto_now_add=True)
    uploaded_by = models.ForeignKey(MyProfile, on_delete=models.CASCADE, null=True, blank=True)

    def __str__(self):
        return '%s'%self.subject

class PostComment(models.Model):
    post = models.ForeignKey(MyPost, on_delete=models.CASCADE, null=True)
    msg = models.TextField(null=True)
    cr_date = models.DateTimeField(auto_now_add=True)
    commented_by = models.ForeignKey(MyProfile, on_delete=models.CASCADE, null=True, blank=True)
    flag = models.CharField(max_length=20, null=True, blank=True, choices=(('abusive', 'abusive'), ('racist', 'racist'), ('egoistic', 'egoistic')))

    def __str__(self):
        return '%s' %self.msg

class PostLike(models.Model):
    post = models.ForeignKey(MyPost, on_delete=models.CASCADE)
    liked_by = models.ForeignKey(MyProfile, on_delete=models.CASCADE)
    cr_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return '%s' % self.liked_by

class FollowUser(models.Model):
    profile = models.ForeignKey(MyProfile, on_delete=models.CASCADE, related_name='profile')
    followed_by = models.ForeignKey(MyProfile, on_delete=models.CASCADE, related_name='followed_by')

    
    

    
