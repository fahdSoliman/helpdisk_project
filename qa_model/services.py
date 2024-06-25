# services for loading data to knowladge base , cleaning it split it with stanza, and save the passages to Passage class 

from django.utils.html import strip_tags
from bs4 import BeautifulSoup

from multilingual_pdf2text.pdf2text import PDF2Text
from multilingual_pdf2text.models.document_model.document import Document

import os
import requests
from django.conf import settings
from .models import DataURL, Passage
from .language_model import StanfordModel,SentenceTrans ,model_cache, AraELECTRA, LFQA
import numpy as np
from .translate_model import Translator
from .semantic import semantic_search_arabic, semantic_search_english
from langchain.text_splitter import RecursiveCharacterTextSplitter
import urllib3

#####################
## utils functions ##
#####################

def process_url(url, instance):
    article_tags = ['h1', 'h2', 'h3', 'h4', 'h5', 'p', 'b', 'a', 'span', 'li']
    article_texts = []
    http = urllib3.PoolManager()
    try:
        response = http.request('GET', url=url)
        if response.status == 200:
            html = response.data
            soup = BeautifulSoup(html, 'html.parser')

            all_tags = soup.find_all()

            for tag in all_tags:
                if tag.name in article_tags:
                    text = tag.get_text(separator=' ', strip=True) 
                    if text:
                        article_texts.append(text)

            article_text = '\n'.join(article_texts)
            DataURL.objects.filter(id=instance.id).update(text=article_text, title=soup.find('title').string)
            return
    except Exception as e:
        print(f"Error fetching URL: {e}")
    return


    # result = requests.get(url)
    # c = result.text
    # # print(c)
    # soup = BeautifulSoup(c, 'html.parser')

    # article_text = ''
    # article = soup.findAll('p')
    # # print(article)
    # for element in article:
    #     article_text += '\n' + ''.join(element.findAll(text = True))
    
    # # create output file of type "TEXT"
    # # file_name = str.replace(strip_tags(soup.find_all('title')[0]), '\n', ' ') + '.txt'
    # # file_out = os.path.join(settings.MEDIA_ROOT, 'knowledgebase\\txt\\', str(instance.id) + '.txt')
    # # with open(file_out, 'w', encoding='utf-8') as file:
    # #     file.write(article_text)
    # #     file.close()
    
    # DataURL.objects.filter(id=instance.id).update(text=article_text, title=soup.find('title').string)
    # return


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
        out = str(out).replace('&copy;', ' ')
        out = str(out).replace('&nbsp;', ' ')
        out = str(out).replace('&raquo;', ' ')
        out = str(out).replace('»', '،')
        out = str(out).replace('&laquo;', ' ')
        DataURL.objects.filter(id=instance.id).update(text=out, title=": ".join(['file',file_name]))
    return


def extract_passages(document):
    if 'stanford_model' not in model_cache:
        model_cache['stanford_model'] = StanfordModel()
    stanford_model = model_cache['stanford_model'] # init the model
    strudctured = stanford_model.NLP(document) # do some nlp at doc 
    passages = stanford_model.sentece_split(strudctured) # extract passages
    return passages

def extract_passages_lang_chain(document):
    text_splitter = RecursiveCharacterTextSplitter(
        separators=['\n\n', '\n', ' ', ''],
        chunk_size=500,
        chunk_overlap=40,
        length_function=len,
        is_separator_regex=False,
    )
    passages = text_splitter.split_text(document)
    return passages
# translation utils

def translate_to_en(passage):
    if 'translator' not in model_cache:
        model_cache['translator'] = Translator()
    translator = model_cache['translator']
    translated_text = translator.translate_to_en(passage)
    return translated_text

def translate_to_ar(passage):
    if 'translator' not in model_cache:
        model_cache['translator'] = Translator()
    translator = model_cache['translator']
    divided_passage = extract_passages(passage)
    translated_text = translator.translate_to_ar(divided_passage)
    return translated_text



############
# LLMs Utils

def init_AraELECTRA_Models():
    if 'sent_transformer' not in model_cache:
        model_cache['sent_transformer'] = SentenceTrans()
    if 'Ara_ELECTRA' not in model_cache:
        model_cache['Ara_ELECTRA'] = AraELECTRA()
    return


def init_BART_LFQA_Models():
    if 'sent_transformer' not in model_cache:
        model_cache['sent_transformer'] = SentenceTrans()
    if 'LFQA' not in model_cache:
        model_cache['LFQA'] = LFQA()
    if 'translator' not in model_cache:
        model_cache['translator'] = Translator()
    return



# arabic contents
def search_for_electra(question):
    passage = semantic_search_arabic(question)
    return passage

def retrieve_answer_electra(question, retrieved_context):
    if 'Ara_ELECTRA' not in model_cache:
        model_cache['Ara_ELECTRA'] = AraELECTRA()
    ara_electra = model_cache['Ara_ELECTRA']
    answer = ara_electra.predict(question, retrieved_context)
    return answer


def abstract_answer_bart(question, passages):
    docs = []
    for p in passages:
        docs.append(p.translate)
    if 'LFQA' not in model_cache:
        model_cache['LFQA'] = LFQA()
    lfqa = model_cache['LFQA']
    query_and_docs = lfqa.prepare_inputs(docs, question)
    answer = lfqa.generate_answer(query_and_docs)
    return answer



