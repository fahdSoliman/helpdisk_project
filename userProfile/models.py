from django.db import models
from django.conf import settings

class profile(models.Model):
    GENDER_MALE = 0
    GENDER_FEMALE = 1
    GENDER_CHOICES = [(GENDER_MALE, 'Male'), (GENDER_FEMALE, 'Female')]
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    image = models.ImageField(upload_to='profile_Img/', null=True)
    fbName = models.TextField(null=True)
    telegram = models.TextField(null=True)
    gender = models.IntegerField(choices=GENDER_CHOICES)
