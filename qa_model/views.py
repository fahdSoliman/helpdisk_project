from django.http import JsonResponse
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required, permission_required
from django.contrib import messages
from django.utils.html import strip_tags
from django.views.decorators.csrf import csrf_protect
from api.authentication import TokenAuthentication
from rest_framework.decorators import api_view, authentication_classes, permission_classes

from .models import DataURL, Passage
from .forms import DataForm, PassageForm
from .language_model import QnAGenerator,  model_cache
from .services import process_file, process_url, extract_passages, translate_to_ar, translate_to_en
from .table import DataURLTable, PassagesTable

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


def view_data_sources(request):
    data_urls = DataURLTable(DataURL.objects.all())

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
            print('test ok')
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
    passages = PassagesTable(Passage.objects.filter(knowledge=obj))
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

def generate_embeddings(request):
    return redirect('')


###########

## LLMs views

def init_QA(request):
    if 'generator' not in model_cache:
        model_cache['generator'] = QnAGenerator()
    generator = model_cache['generator']
    context = generator.context
    question = "ما هو أسمي؟"

    variables = {
        "context": context,
        "question": question
    }
    return render(request, 'knowledge/init.html', variables)

@csrf_protect
def test_qa(request):
    if request.method == "POST":
        question = request.POST.get('question')
        generator = model_cache['generator']
        context = generator.context
        answer = generator.predict(question)
        print(answer)
        variables = {
            "context": context,
            "question": question,
            "answer": answer['answer'],
            "score": answer['score']

        }
    return render(request, 'knowledge/init.html', variables)


def update_context(request):
    # q = DataURL.objects.all()
    # text = ""
    # for q_instance in q:
    #     with open(q_instance.file.path, 'r', encoding='utf-8' ) as f:
    #         text += f.read()
    #     # text.append()
    # # print(text)
    # generator = model_cache['generator']
    # generator.update_text(text)

    return redirect('init_qa')




## API for Botpress...

@api_view(['POST'])
# @permission_classes([isBotpressPermission])
@authentication_classes([TokenAuthentication])
def give_answer(request):
    if request.method == 'POST':
        question = request.POST.get('q')
        if 'generator' not in model_cache:
            model_cache['generator'] = QnAGenerator()
        generator = model_cache['generator']
        answer = generator.predict(question)
        return JsonResponse(answer)
    return JsonResponse({'error': 'Invalid request method'})



