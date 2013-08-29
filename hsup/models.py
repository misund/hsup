from django.db import models

class Feed(models.Model):
    feed = models.URLField(max_length=255)
    twitter_accounts = models.ManyToManyField('TwitterAccount')
    facebook_accounts = models.ManyToManyField('FacebookAccount')

class TwitterAccount(models.Model):
    username = models.CharField(max_length=20)

class FacebookAccount(models.Model):
    email = models.EmailField(max_length=254)
