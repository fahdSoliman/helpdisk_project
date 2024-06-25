# semantic search functions using sentence_transformers library also PGvector for postgresql as vector DB
from .language_model import SentenceTrans ,model_cache
from .models import Passage, QA
from pgvector.django import L2Distance, CosineDistance
from torch import from_numpy




def sent_embeddings(passage):
    if 'sent_transformer' not in model_cache:
        model_cache['sent_transformer'] = SentenceTrans()
    sent_transformer = model_cache['sent_transformer']
    embeddings = sent_transformer.calc_embeddings(passage)
    # list_embeddings = np.asarray(embeddings).tolist()
    return embeddings





def sematic_search_transformer(question_embedding, ar_embeddings, k):
    sentence_transformer = model_cache['sent_transformer']
    # question_embedding = sentence_transformer.calc_embeddings(question)
    top = sentence_transformer.semantic_search(question_embedding, ar_embeddings, k)
    return top

def semantic_search_arabic(question_embeddings):
    top_threshold = 0.70
    # low_threshold = 0.65
    top_passages = Passage.objects.annotate(score=1-CosineDistance('ar_pg_embeddings', question_embeddings)).filter(score__gt=top_threshold).order_by('-score')[:3]
    
    return top_passages

def semantic_search_qa(question_embeddings):
    top_threshold = 0.9
    first_q = QA.objects.annotate(q_score=1-CosineDistance('ar_q_embeddings', question_embeddings)).filter(q_score__gt=top_threshold).order_by('-q_score')[:1]
    return first_q


def semantic_search_english(question_embeddings):
    threshold = 0.70
    passages = Passage.objects.annotate(score=1-CosineDistance('en_pg_embeddings', question_embeddings)).filter(score__gt=threshold).order_by('-score')[:8]
    return passages

def semantic_search_electra(question_embeddings):
    threshold = 0.4
    top_passages = Passage.objects.annotate(score=1-CosineDistance('ar_pg_embeddings', question_embeddings)).filter(score__gt=threshold).order_by('-score')[:2]
    return top_passages

def semantic_search(question_embeddings, algorithm):
    if algorithm == 'CosineDistance':
        top_threshold = 0.60
        top_passages = Passage.objects.annotate(score=1-CosineDistance('ar_pg_embeddings', question_embeddings)).filter(score__gt=top_threshold).order_by('-score')[:3]
        return top_passages
    if algorithm == 'L2Distance':
        passages = Passage.objects.order_by(L2Distance('ar_pg_embeddings', question_embeddings))[:8].annotate(score =8 - L2Distance('ar_pg_embeddings', question_embeddings))
        return passages
    if algorithm == 'transformer-Cosine':
        if 'corpus_embeddings' not in model_cache:
            model_cache['corpus_embeddings'] = load_embeddings()
        corpus_embeddings = model_cache['corpus_embeddings']
        p = sematic_search_transformer(question_embeddings, corpus_embeddings, 8)
        all_passages = model_cache['passages']
        obj = []
        for passage in p[0]:
            object = {'text': all_passages[passage['corpus_id']], 'score': passage['score']}
            obj.append(object)
    return obj


def load_embeddings():
    corpus_embeddings = []
    passages = []
    doc = Passage.objects.all()
    for d in doc:
        corpus_embeddings.append(from_numpy(d.ar_pg_embeddings))
        passages.append(d.text)
    model_cache['passages'] = passages
    return corpus_embeddings