from django.db import models

class Feed(models.Model):
    feed = models.URLField(max_length=255)
    twitter_accounts = models.ManyToManyField('Twitter_Account')
    facebook_accounts = models.ManyToManyField('Facebook_Accoun')

class Twitter_Account(models.Model)
    username = models.StringField(max_length=20)

class Facebook_Account(models.Model)
    email = models.EmailField(max_length=254)
