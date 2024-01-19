from django.db import models
from ckeditor.fields import RichTextField
from django.utils.html import strip_tags
from django.utils.text import Truncator

# Create your models here.


class DataURL(models.Model):
    choices = [
        ('pdf', 'PDF file'),
        ('web', 'Website Page')
    ]
    url = models.URLField()
    title = models.CharField(max_length=200 ,null=True, blank=True)
    text = RichTextField(null=True, blank=True)
    data_type = models.CharField(choices=choices, max_length=50)
    pub_date = models.DateTimeField(auto_now=False,auto_now_add=True)
    updated = models.DateTimeField(auto_now=True,auto_now_add=False)

    def __str__(self) -> str:
        return self.title or "some Data URL"
        
    def get_text_clean(self):
        striped = strip_tags(str(self.text))
        trimed =  str(striped).replace('&nbsp;', '')
        return trimed
    
    def get_text_trancated(self):
        striped = strip_tags(str(self.text))
        cleaned =  str(striped).replace('&nbsp;', '')
        trancated = Truncator(cleaned).words(20)
        return trancated

class Passage(models.Model):
    knowledge = models.ForeignKey(DataURL, on_delete=models.CASCADE)
    text = models.TextField(blank=True, null=True)
    translate = models.TextField(blank=True, null=True)
    translated = models.BooleanField(default=False, null=True)
    pub_date = models.DateTimeField(auto_now=False,auto_now_add=True)
    updated = models.DateTimeField(auto_now=True,auto_now_add=False)

    def __str__(self) -> str:
        return self.knowledge.title or "some Passage of Data source"
    def get_translate_truncated(self):
        truncated = Truncator(self.translate).words(10)
        return truncated
