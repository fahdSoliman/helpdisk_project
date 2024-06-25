from qa_model.models import DataURL, Passage
from qa_model.language_model import SentenceTrans
from django.db.models import Q


'''calculate embeddings {only new records}'''
# init llm models
print('initiating language models start!')
sent_transformer = SentenceTrans()
print('models init is done!')


## gen embeddings function
def gen_embeddings():
    passages_qs = Passage.objects.filter(Q(ar_pg_embeddings=None) | Q(en_pg_embeddings=None))
    for p in passages_qs:
        if p.text:
            embeddings = sent_transformer.calc_embeddings(p.text)
            p.ar_pg_embeddings = embeddings
        if p.translate:
            embeddings_translate = sent_transformer.calc_embeddings(p.translate)
            p.en_pg_embeddings = embeddings_translate
        p.save()
        print('object {} is calculated'.format(p.id))
    return


print('begin of calc embeddings process:')
gen_embeddings()
print('calculating embeddings is done!')

