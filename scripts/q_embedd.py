from qa_model.models import QA
from qa_model.language_model import SentenceTrans
from django.db.models import Q




'''calculate embeddings {only new records}'''
# init llm models
sent_transformer = SentenceTrans()
print('models init is done!')

def gen_embeddings():
    qa = QA.objects.all()
    for p in qa:
        embeddings = sent_transformer.calc_embeddings(p.ar_question)
        p.ar_q_embeddings = embeddings
        p.save()
        print('object {} is calculated'.format(p.id))
    return
gen_embeddings()




