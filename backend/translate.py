from qa_model.models import DataURL, Passage
from qa_model.language_model import SentenceTrans
from qa_model.translate_model import Translator
from django.db.models import Q

# init llm models
print('initiating language models start!')
translator = Translator()
sent_transformer = SentenceTrans()
print('models init is done!')

## translate function
def translate():
    passages_qs = Passage.objects.filter(translated=False)
    for p in passages_qs:
        translated_text = translator.en_translate(p.text)
        p.translate = translated_text
        p.translated = True
        p.save()
        print('object {} is translated'.format(p.id))
    return


## gen embeddings function
def gen_embeddings():
    passages_qs = Passage.objects.filter(Q(ar_pg_embeddings=None) & Q(en_pg_embeddings=None))
    for p in passages_qs:
        if p.text:
            embeddings = sent_transformer.calc_embeddings(p.text)
            p.ar_pg_embeddings = embeddings
        if p.translate:
            embeddings_translate = sent_transformer.calc_embeddings(p.translate)
            p.en_pg_embeddings = embeddings_translate
        print('object {} is calculated'.format(p.id))
    return


print('begin of translating process:')
translate()
print('translation is done!')
print('begin of calc embeddings process:')
gen_embeddings()
print('calculating embeddings is done!')

