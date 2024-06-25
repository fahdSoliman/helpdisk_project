import json
import time
from django.http import HttpResponse, JsonResponse
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required, permission_required
from django.contrib import messages
from django.views.decorators.csrf import csrf_protect
from api.authentication import TokenAuthentication
from rest_framework.decorators import api_view, authentication_classes, permission_classes

from .models import DataURL, Passage, QA
from .forms import DataForm, PassageForm, QA_Form
from .services import process_file, process_url, extract_passages, extract_passages_lang_chain, retrieve_answer_electra, translate_to_ar, translate_to_en, init_AraELECTRA_Models, init_BART_LFQA_Models, abstract_answer_bart
from .semantic import sent_embeddings, semantic_search, semantic_search_arabic, semantic_search_qa, semantic_search_electra
from .table import DataURLTable, PassagesTable, LogsTable


## some views with templates for management qa datasets 

def view_qa_panel(request):
    knowledge_count = DataURL.objects.all().count()
    knowledge_last = DataURL.objects.all().order_by('-updated').first()
    web_count = DataURL.objects.filter(data_type='web').count()
    pdf_count = DataURL.objects.filter(data_type='pdf').count()
    passage_count = Passage.objects.all().count()
    context = {
        'knowledge_count': knowledge_count,
        'knowledge_last': knowledge_last,
        'web_count': web_count,
        'pdf_count': pdf_count,
        'total_source': web_count + pdf_count,
        'passage_count': passage_count
    }
    return render(request, 'knowledge/panel.html', context)


def view_logs(request):
    logs_data = LogsTable(QA.objects.all().order_by('id'))
    context = {
        'logs_data': logs_data
    }
    return render(request, 'knowledge/view_logs.html', context)


def edit_qa(request, id):
    instance = QA.objects.get(id=id)
    if request.method == 'POST':
        qa_form = QA_Form(request.POST, instance=instance)
        if qa_form.is_valid():
            qa_form.save()
            messages.success(request, f'تم تعديل سجل سؤال/جواب بنجاح')
            return redirect('logs')
    else:
        qa_form = QA_Form(instance=instance)
    context = {
        'qa_form': qa_form
    }
    return render(request, 'knowledge/edit_qa.html', context)

def download_db(request):
    qas = QA.objects.all()

    qa_data = []
    for qa in qas:
        qa_dict = {
            'id': qa.id,
            'question': qa.question,
            'ar_question': qa.ar_question,
            'answer': qa.answer,
            'ar_answer': qa.ar_answer,
            'score': qa.score,
            'related_text': [{'id': passage.id, 'text': passage.text, 'translate': passage.translate} for passage in qa.passages.all()]
        }
        qa_data.append(qa_dict)

    json_data = json.dumps(qa_data, ensure_ascii=False)

    response = HttpResponse(json_data, content_type='application/json')
    response['Content-Disposition'] = 'attachment; filename="data.json"'
    return response


def view_data_sources(request):
    data_urls = DataURLTable(DataURL.objects.all().order_by('id'))

    context = {
        'data_urls': data_urls,
    }
    return render(request, 'knowledge/view_data_source.html', context)


def delete_data_source(request, id):
    DataURL.objects.filter(id=id).delete()

    return redirect('view_data')


def add_data_source(request):
    if request.method == 'POST':
        data_form = DataForm(request.POST)
        if data_form.is_valid():
            # print('test ok')
            data_form.save()
            data = request.POST.copy()
            if data.get('data_type') == 'web':
                process_url(data.get('url'),data_form.instance)
            elif data.get("data_type") == 'pdf':
                process_file(data.get('url'), data_form.instance)
            messages.success(request, f'تم اضافة مصدر معلومات بنجاح')
            return redirect('view_k')
    else:
        data_form = DataForm()
    
    context = {
        'data_form': data_form
    }

    return render(request, 'knowledge/add_data.html', context)


def edit_data_source(request, id):
    instance = get_object_or_404(DataURL, id=id)
    if request.method == 'POST':
        data_form = DataForm(request.POST, instance=instance)
        if data_form.is_valid():
            data_form.save()
            messages.success(request, f'تم تعديل المعلومات بنجاح')
            return redirect('view_data')
    else:
        data_form = DataForm(instance=instance)
    context = {
        'data_form': data_form
    }
    return render(request, 'knowledge/edit_knowledge.html', context)




# passage views

def view_passages(request, id):
    obj = DataURL.objects.filter(id=id).first()
    passages = PassagesTable(Passage.objects.filter(knowledge=obj).order_by('id'))
    context = {
        'passages': passages,
    }
    return render(request, 'knowledge/passages.html', context)


def edit_passage(request, id):
    obj = Passage.objects.filter(id=id).first()
    if request.method =='POST':
        passage_form = PassageForm(request.POST, instance=obj)
        if passage_form.is_valid():
            passage_form.save()
            messages.success(request, f'تم التعديل بنجاح')
            id = int(obj.knowledge.id)
            print("id: " + str(id))
            return redirect('view_passages',id)
    else:
        passage_form = PassageForm(instance=obj)
    context = {
        'passage_form': passage_form,
        'obj': obj.knowledge.id
    }
    return render(request, 'knowledge/edit_passage.html', context)

def delete_passage(request, id):
    obj = Passage.objects.filter(id=id).first()
    id = obj.knowledge.id
    obj.delete()
    return redirect('view_passages', id)


# NLP views

def manual_split(request, id):
    obj = Passage.objects.filter(id=id).first()
    base = DataURL.objects.filter(id=obj.knowledge.id).first()
    if request.method =='POST':
        passage_form = PassageForm(request.POST, instance=obj)
        if passage_form.is_valid():
            data = request.POST.copy()
            # print(data)
            new_passage = data.get('new_passage')
            passage_form.save()
            Passage.objects.create(knowledge=base, text=new_passage)
            messages.success(request, f'تم التقسيم بنجاح')
            return redirect('view_passages', base.id)
    else: 
        passage_form = PassageForm(instance=obj)
    context = {
        'passage_form': passage_form
    }
    return render(request, 'knowledge/manual_split.html', context)


def sentences_split(request, id):
    obj = DataURL.objects.filter(id=id).first()
    passages = extract_passages(str(obj.get_text_clean()))
    for p in passages:
        Passage.objects.create(knowledge=obj, text=p)
    messages.success(request, f'تم توليد الفقرات بنجاح')
    return redirect('view_data')

def lang_chain_splitter(request, id):
    obj = DataURL.objects.filter(id=id).first()
    passages = extract_passages_lang_chain(str(obj.get_text_clean()))
    for p in passages:
        Passage.objects.create(knowledge=obj, text=p)
    messages.success(request, f'تم توليد الفقرات بنجاح')
    return redirect('view_data')

def translate_all(request):

    return redirect('')


def translate_this(request, id):
    obj = Passage.objects.filter(id=id).first()
    en_text = translate_to_en(obj.text)
    obj.translate = en_text
    obj.translated = True
    obj.save()
    id = obj.knowledge.id
    return redirect('view_passages', id)

def generate_embeddings(request, id):
    passage = Passage.objects.filter(id = id).first()
    if passage.text:
        embeddings = sent_embeddings(passage.text)
        passage.ar_pg_embeddings = embeddings
    if passage.translate:
        embeddings_translate = sent_embeddings(passage.translate)
        passage.en_pg_embeddings = embeddings_translate
        
    passage.save()
    id = passage.knowledge.id
    return redirect('view_passages', id)




###########
## LLMs views # ARA-ELECTRA

@csrf_protect
def init_AraELECTRA(request):
    init_AraELECTRA_Models()
    passages = "هنا سيتم عرض الفقرات المتعلقة بالسؤال"
    question = "كمثال: كم يتطلب ايام عمل لتسجيل عنوان النطاق على مخدم الاسماء؟"
    if request.method == 'POST':
        question = request.POST.get('question')
        start = time.time()
        question_embeddings = sent_embeddings(question)
        passages = semantic_search_electra(question_embeddings=question_embeddings)
        retrieved_text = " \n ".join(p.text for p in passages)
        answer = retrieve_answer_electra(question, retrieved_text)
        end = time.time()
        variables = {
            "retrieved_text": retrieved_text,
            "question": question,
            "answer": answer['answer'],
            "score": answer['score'],
            "time": end - start
        }
        return render(request, 'knowledge/init_araElectra.html', variables)
    variables = {
        "retrieved_text": passages,
        "question": question
    }
    return render(request, 'knowledge/init_araElectra.html', variables)


##########################
## view for BART_LFQA LLM

def init_LFQA(request):
    init_BART_LFQA_Models()
    passages = [{"text": "هنا سيتم عرض الفقرات المتعلقة بالسؤال"}]
    question = "كمثال: كم يتطلب ايام عمل لتسجيل عنوان النطاق على مخدم الاسماء؟"
    if request.method == 'POST':
        question = request.POST.get('question')
        start = time.time()
        question_embeddings = sent_embeddings(question)
        find_q = semantic_search_qa(question_embeddings=question_embeddings)
        if find_q:
            variables = {
                "retrieved_text": find_q[0].passages.values('text'),
                "question": find_q[0].ar_question,
                "answer": find_q[0].ar_answer,
                "q_score": find_q[0].q_score
            }
            return render(request, 'knowledge/init_lfqa.html', variables)
        
        start_translate1 = time.time()
        en_question = translate_to_en(question)
        end_translate1 = time.time()

        passages = semantic_search_arabic(question_embeddings)
        start_abstraction = time.time()
        answer = abstract_answer_bart(en_question, passages)
        end_abstraction = time.time()
        start_translate2 = time.time()
        ar_answer_list = translate_to_ar(answer)
        ar_answer = ' '.join(ar_answer_list)
        end_translate2 = time.time()
        end = time.time()
        # QA_instance = QA.objects.create(
        #     question = en_question,
        #     ar_question = question,
        #     answer = answer,
        #     ar_answer = ar_answer
        # )
        # QA_instance.passages.set(passages)
        # QA_instance.save()
        variables = {
            "retrieved_text": passages,
            "question": question,
            "answer": ar_answer,
            "en_answer": answer,
            "translate1": end_translate1 - start_translate1,
            "abstact": end_abstraction - start_abstraction,
            "translate2": end_translate2 - start_translate2,
            "time": end - start
        }
        return render(request, 'knowledge/init_lfqa.html', variables)
    variables = {
        "retrieved_text": passages,
        "question": question
    }
    return render(request, 'knowledge/init_lfqa.html', variables)


########################
# semantic search testing

@csrf_protect
def init_semantic_search(request):
    if request.method == 'POST':
        question = request.POST['question']
        algorithm = request.POST['algorithm']
        ar_pg_embeddings = sent_embeddings(question)
        # we could do that in other function
        documents = semantic_search(ar_pg_embeddings, algorithm)
        context = {
            'question': question,
            'most_similar': documents 
        }
        return render(request, 'knowledge/test_semantic_search.html', context)
    return render(request, 'knowledge/test_semantic_search.html')



## API for Botpress...
@api_view(['POST'])
# @permission_classes([isBotpressPermission])
@authentication_classes([TokenAuthentication])
def give_answer_araElectra(request):
    if request.method == 'POST':
        question = str(request.data.get('question'))
        print(question)
        print(request.data)
        question_embeddings = sent_embeddings(question)
        passages = semantic_search_electra(question_embeddings=question_embeddings)
        if len(passages) == 0:
            return JsonResponse({'answer': '0'})
        retrieved_text = " \n ".join(p.text for p in passages)
        answer = retrieve_answer_electra(question, retrieved_text)
        if answer['score'] < 0.3:
            return JsonResponse({'answer': '0'})
        return JsonResponse(answer)
    return JsonResponse({'error': 'Invalid request method'})


@api_view(['POST'])
# @permission_classes([isBotpressPermission])
@authentication_classes([TokenAuthentication])
def give_answer_bart_lfqa(request):
    if request.method == 'POST':
        question = request.data.get('question')
        question_embeddings = sent_embeddings(question)

        qa_find = semantic_search_qa(question_embeddings)
        if qa_find:
            return JsonResponse({
                'answer': qa_find[0].ar_answer,
                'score': qa_find[0].score,
                'qa_instance': qa_find[0].id
            })
        passages = semantic_search_arabic(question_embeddings)
        if len(passages) == 0:
            return JsonResponse({'answer': '0'})
        
        
        en_question = translate_to_en(question)
        answer = abstract_answer_bart(en_question, passages)
        ar_answer_list = translate_to_ar(answer)
        ar_answer = ' '.join(ar_answer_list)
        QA_instance = QA.objects.create(
            question = en_question,
            ar_question = question,
            answer = answer,
            ar_answer = ar_answer,
            ar_q_embeddings = question_embeddings
        )
        QA_instance.passages.set(passages)
        QA_instance.save()
        return JsonResponse({'answer': ar_answer,
                             'score': QA_instance.score,
                             'qa_instance': QA_instance.id
                             })
    return JsonResponse({'error': 'Invalid request method'})

@api_view(['POST'])
# @permission_classes([isBotpressPermission])
@authentication_classes([TokenAuthentication])
def qa_rate(request):
    if request.method == 'POST':
        qa_id = request.data.get('qa_id')
        qa_user_rate = request.data.get('qa_user_rate')
        qa_instance = QA.objects.get(id=qa_id)
        qa_instance.score =+ int(qa_user_rate)
        qa_instance.save()
        return JsonResponse({'qa_id': qa_instance.id,
                             'qa_score': qa_instance.score})
    return JsonResponse({'error': 'Invalid request method'})
