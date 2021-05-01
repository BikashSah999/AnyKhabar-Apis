from django.db import models
from ckeditor.fields import RichTextField
from django.utils import timezone
from django.contrib.auth.admin import User


# Create your models here.
class Category(models.Model):
    id = models.AutoField(primary_key=True)
    category_name = models.CharField(max_length=20, null=False)

    def __str__(self):
        return(self.category_name)

class Logo(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=20)
    logo = models.ImageField(upload_to='website/logo')
    status = models.BooleanField(default = True)

    def __str__(self):
        return(self.name)

class News(models.Model):
    id = models.AutoField(primary_key=True)
    headline = models.CharField(max_length=500, null=False)
    description = RichTextField(null=False)
    views = models.IntegerField(default=0)
    sub_cat_list = (('National', 'National'), ('International','International'))
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True, related_name='category')
    sub_category = models.CharField(choices=sub_cat_list, max_length=20, default='National')
    image = models.ImageField(upload_to='website/news')
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='author')
    credit = models.CharField(max_length=30, null=True, blank=True)
    posted_date = models.DateField(default=timezone.now)
    time_to_read = models.IntegerField(default=2)


    def __str__(self):
        return(self.headline)

class Comments(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100, null=False)
    mail_address = models.CharField(max_length=100, null=False)
    comment = RichTextField(max_length=2000, null=False)
    news_id = models.ForeignKey(News, on_delete=models.SET_NULL, null=True)
    posted_date = models.DateField(default=timezone.now)
    
    def __str__(self):
        return(self.name)

class Hashtags(models.Model):
    id = models.AutoField(primary_key = True)
    tags = models.CharField(max_length=100, null=False)

    def __str__(self):
        return(self.tags)

class Message(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100, null=False)
    mail = models.CharField(max_length=100, null=False)
    message = RichTextField(max_length=2000, null=False)
    posted_date = models.DateField(default=timezone.now)

    def __str__(self):
        return(self.name)

class VotingPoll(models.Model):
    id = models.AutoField(primary_key=True)
    question = models.CharField(max_length=2000, null=False)
    total_votes = models.IntegerField(default=0, null=False)

    def __str__(self):
        return(self.question)

class PollOptions(models.Model):
    id = models.AutoField(primary_key=True)
    option = models.CharField(max_length=100, null=False)
    voting_poll = models.ForeignKey(VotingPoll, on_delete=models.CASCADE, null=False)
    num_of_votes = models.IntegerField(default=0, null=False)

    def __str__(self):
        return(self.option)

class Ads(models.Model):
    id  = models.AutoField(primary_key=True)
    page_list = (('Header', 'Header'), ('Side Bar', 'Side Bar'))
    ads_location = (('H-970*90', 'H-970*90'), ('S1-150*150','S1-150*150'), ('S2-150*150','S2-150*150'))
    name = models.CharField(max_length=50, blank=False)
    image = models.ImageField(upload_to='ads')
    page = models.CharField(choices=page_list, default='Home Page', max_length=20)
    location = models.CharField(choices=ads_location, max_length=20)
    status = models.BooleanField(default=True)
    url_link = models.CharField(max_length=1000, blank=False, default="#")

    def __str__(self):
        return(self.name)

