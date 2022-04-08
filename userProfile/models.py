from django.db import models
from django.contrib.auth.models import User
from phonenumber_field.modelfields import PhoneNumberField

class Profile(models.Model):
    GENDER_MALE = 0
    GENDER_FEMALE = 1
    GENDER_CHOICES = [(GENDER_MALE, 'ذكر'), (GENDER_FEMALE, 'أنثى')]
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    image = models.ImageField(default='default.png' ,upload_to='profile_Img/')
    fbName = models.CharField(max_length=255, null=True)
    telegram = models.CharField(max_length=255, null=True)
    gender = models.IntegerField(choices=GENDER_CHOICES, null=True)

    def __str__(self):
        return self.user.username
    
    def get_gender(self):
        if self.gender == 0:
            return 'ذكر'
        else:
            return 'أنثى'


class CompanyProfile(models.Model):
    gov_fin_org = 0
    gov_man_org = 1
    special_org = 2
    org_type = [(gov_fin_org, 'مؤسسة حكومية مالية'), (gov_man_org, 'مؤسسة حكومية إدارية'), (special_org, 'مؤسسة خاصة')]
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    customer_name = models.CharField(max_length=255)
    customer_type = models.IntegerField(choices=org_type, null=True)
    country = models.CharField(max_length=255, null=True)
    phone = PhoneNumberField(null=True)
    email = models.EmailField(null=True)

    def __str__(self):
        return str(self.customer_name)

class FinanicalResponse(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    financial_name = models.CharField(max_length=255, null=True)
    phone = PhoneNumberField(null=True)
    email = models.EmailField(null=True)

    def __str__(self):
        return str(self.financial_name)

class TechnicalResponse(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    technical_name = models.CharField(max_length=255, null=True)
    phone = PhoneNumberField(null=True)
    email = models.EmailField(null=True)

    def __str__(self):
        return str(self.technical_name)
    
