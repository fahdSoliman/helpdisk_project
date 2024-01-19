from django.urls import path
from . import views



urlpatterns = [
    path('panel/', views.view_qa_panel, name='view_k'), # view home QA app panel **

    path('data_source/', views.view_data_sources, name='view_data'),                  # view all data source and related text **
    path('data_source/add/', views.add_data_source, name='add_data'),                 # add data source to extract the text **
    path('data_source/del/<int:id>/', views.delete_data_source, name='delete_data'),  # delete data source with all related objects
    path('data_source/edit/<int:id>/', views.edit_data_source, name='edit_data'),     # edit knowledge, edit full text **

    path('data_source/passages/<int:id>/', views.view_passages, name='view_passages'),              # view all passages of specific data source **
    path('data_source/passages/edit/<int:id>/', views.edit_passage, name='edit_passage'),           # edit passage **
    path('data_source/passages/delete/<int:id>/', views.delete_passage, name='delete_passage'),     # delete Passage

    path('knowledge/manual_split/<int:id>/', views.manual_split,name='manual_split'),
    path('knowledge/split/<int:id>',views.sentences_split, name='sentences_split'),             # using Stanza for sentences splitting document
    path('knowledge/translate/', views.translate_all, name='translate_all'),                    # Facebook translate all passages to en
    path('knowledge/translate/<int:id>/', views.translate_this, name='translate_this'),         # Facebook translate specific passage to en
    path('knowledge/embeddings/', views.generate_embeddings, name='generate_embeddings'),       # generate embedding for passages 

    path('init/init_araELECTRA/', views.init_QA, name='init_araElectra'),   # load araELECTRA and page to test it **
    path('init/init_LFQA/', views.view_qa_panel, name='init_lfqa'),         # load BART_LFQA LLM model and page to test it **

    path('test/araELECTRA/', views.test_qa, name='test_electra'),       # send test for araELECTRA , !!we need add another one for lfqa 
    path('test/LFQA/', views.test_qa, name='test_lfqa'),                # send test for BART_LFQA , !!we need add another one for lfqa

    path('knowledge/update_context/', views.update_context, name='update_context'), # we dont need it anymore

    path('api/araELECTRA/predict/', views.give_answer, name='predict_electra'), # API endpoint for AraELECETRA
    path('api/LFQA/predict/', views.give_answer, name='predict_lfqa'), # API endpoint for BART_LFQA
]
