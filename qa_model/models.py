from html import unescape
from django.db import models
from ckeditor.fields import RichTextField
from django.utils.html import strip_tags
from django.utils.safestring import SafeString
from django.utils.text import Truncator
from django.contrib.postgres.fields import ArrayField
from pgvector.django import VectorField
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
        stripped = strip_tags(str(self.text))
        cleaned = unescape(stripped)
        return cleaned
    
    def get_text_trancated(self):
        striped = strip_tags(str(self.text))
        cleaned =  str(striped).replace('&nbsp;', '')
        trancated = Truncator(cleaned).words(20)
        return trancated

class Passage(models.Model):
    knowledge = models.ForeignKey(DataURL, on_delete=models.CASCADE)
    text = models.TextField(blank=True, null=True)
    translate = models.TextField(blank=True, null=True)

    ar_embeddings = ArrayField(models.FloatField(), size=768, blank=True, null=True)
    en_embeddings = ArrayField(models.FloatField(), size=768, blank=True, null=True)

    ar_pg_embeddings = VectorField(dimensions=768, blank=True, null=True)
    en_pg_embeddings = VectorField(dimensions=768, blank=True, null=True)
    
    translated = models.BooleanField(default=False, null=True)
    pub_date = models.DateTimeField(auto_now=False,auto_now_add=True)
    updated = models.DateTimeField(auto_now=True,auto_now_add=False)

    def __str__(self) -> str:
        return str('passage: ' + str(self.pk)) or "some Passage of Data source"
    def get_translate_truncated(self):
        truncated = Truncator(self.translate).words(10)
        return truncated


class QA(models.Model):
    question = models.TextField(blank=True, null=True)
    ar_question = models.TextField(blank=True, null=True)
    answer = models.TextField(blank=True, null=True)
    ar_answer = models.TextField(blank=True, null=True)
    passages = models.ManyToManyField(Passage, null=True, blank=True)
    score = models.IntegerField(default=0)
    ar_q_embeddings = VectorField(dimensions=768, blank=True, null=True)

    def question_truncated(self):
        return Truncator(self.question).words(10)

    def ar_question_truncated(self):
        return Truncator(self.ar_question).words(10)
    
    def answer_truncated(self):
        return Truncator(self.answer).words(10)
        
    def ar_answer_truncated(self):
        return Truncator(self.ar_answer).words(10)
    