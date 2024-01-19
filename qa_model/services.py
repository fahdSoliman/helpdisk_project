# services for loading data to knowladge base , cleaning it split it with stanza, and save the passages to Passage class 

from django.utils.html import strip_tags
from bs4 import BeautifulSoup

from multilingual_pdf2text.pdf2text import PDF2Text
from multilingual_pdf2text.models.document_model.document import Document

import os
import requests
from django.conf import settings
from .models import DataURL
from .language_model import StanfordModel, model_cache
from .translate_model import Translator

#####################
## utils functions ##
#####################

def process_url(url, instance):
    print('test')
    result = requests.get(url)
    c = result.text
    # print(c)
    soup = BeautifulSoup(c, 'html.parser')

    article_text = ''
    article = soup.findAll('p')
    # print(article)
    for element in article:
        article_text += '\n' + ''.join(element.findAll(text = True))
    
    # create output file of type "TEXT"
    # file_name = str.replace(strip_tags(soup.find_all('title')[0]), '\n', ' ') + '.txt'
    # file_out = os.path.join(settings.MEDIA_ROOT, 'knowledgebase\\txt\\', str(instance.id) + '.txt')
    # with open(file_out, 'w', encoding='utf-8') as file:
    #     file.write(article_text)
    #     file.close()
    
    DataURL.objects.filter(id=instance.id).update(text=article_text, title=soup.find('title').string)
    return


def process_file(url, instance):
    response = requests.get(url)
    if response.status_code == 200:
        file_name = url.split("/")[-1]
        file_path = os.path.join(settings.MEDIA_ROOT,'knowledgebase\\download\\', file_name)
        # important!!! geting the name of the file from respose.FILES maybe
        with open(file_path, 'wb') as f:
            f.write(response.content)
        pdf_document = Document(
        document_path= file_path,
        language='ara'
        )
        pdf2text = PDF2Text(document=pdf_document)
        content = pdf2text.extract()
        out = ''
        for text in content:
            out += text.get('text')
        # out_path = os.path.join(settings.MEDIA_ROOT, 'knowledgebase\\txt\\' ,file_name + '.txt')
        # with open(out_path,'w', encoding='utf-8') as file:
        #     file.write(out)
        #     file.close()
        # we need to save TEXT file in 'knowledgebase\\txt\\' 
        # print(out)
        DataURL.objects.filter(id=instance.id).update(text=out, title=": ".join(['file',file_name]))
 
    return


def extract_passages(document):
    if 'stanford_model' not in model_cache:
        model_cache['stanford_model'] = StanfordModel()
    stanford_model = model_cache['stanford_model'] # init the model
    strudctured = stanford_model.NLP(document) # do some nlp at doc 
    passages = stanford_model.sentece_split(strudctured) # extract passages
    return passages



def translate_to_en(passage):
    if 'translator' not in model_cache:
        model_cache['translator'] = Translator()
    translator = model_cache['translator']
    translated_text = translator.ar_translate(passage)
    return translated_text

def translate_to_ar(passage):
    if 'translator' not in model_cache:
        model_cache['translator'] = Translator()
    translator = model_cache['translator']
    translated_text = translator.en_translate(passage)
    return translated_text
