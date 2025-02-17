from pkgutil import extend_path
from django.db import models
from django.contrib.auth.models import User
from phonenumber_field.modelfields import PhoneNumberField


class Profile(models.Model):
    GENDER_MALE = 'male'
    GENDER_FEMALE = 'female'
    GENDER_CHOICES = [(GENDER_MALE, 'ذكر'), (GENDER_FEMALE, 'أنثى')]
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    image = models.ImageField(default='default.png' ,upload_to='profile_Img/', null=True)
    facebook = models.CharField(max_length=255,blank=True, null=True, unique=True)
    telegram = models.CharField(max_length=255,blank=True, null=True, unique=True)
    botpress = models.CharField(max_length=255,blank=True, null=True, unique=True)
    is_complete = models.BooleanField(default=False)
    gender = models.CharField(choices=GENDER_CHOICES, null=True, max_length=25)

    def __str__(self):
        return self.user.username
    
    def get_gender(self):
        if self.gender == 0:
            return 'ذكر'
        else:
            return 'أنثى'


class CompanyProfile(models.Model):
    gov_fin_org = 'gov_fin' ## need to change some time
    gov_man_org = 'gov_man'
    special_org = 'special'
    org_type = [(gov_fin_org, 'مؤسسة حكومية مالية'), (gov_man_org, 'مؤسسة حكومية إدارية'), (special_org, 'مؤسسة خاصة')]
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    customer_name = models.CharField(max_length=255)
    customer_type = models.CharField(choices=org_type,default=2, null=True, max_length=15)
    country = models.CharField(max_length=255, null=True)
    phone = PhoneNumberField(null=True)
    email = models.EmailField(null=True)

    def __str__(self):
        return str(self.customer_name)
    
    def get_type(self):
        for value, label in self.org_type:
            if value == self.customer_type:
                return label
        return "Unknown Type"  

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
    
