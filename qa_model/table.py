import django_tables2 as Tables
from .models import DataURL, Passage, QA
from django_tables2.utils import A


class LogsTable(Tables.Table):
    no = Tables.Column(empty_values=(), verbose_name='تسلسل')
    question_truncated = Tables.Column(verbose_name="السؤال")
    ar_question_truncated = Tables.Column(verbose_name="السؤال مترجم")
    answer_truncated = Tables.Column(verbose_name="الجواب")
    ar_answer_truncated = Tables.Column(verbose_name="الجواب مترجم")
    score = Tables.Column(verbose_name="score")
    edit_qa = Tables.LinkColumn('edit_qa', verbose_name="تعديل" ,text='عدّل', args=[A("pk")])

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.row_counter = 0


    def render_no(self):
        self.row_counter += 1
        return self.row_counter
    
    class Meta:
        model=QA
        fields = ('no', 'question_truncated', 'ar_question_truncated', 'answer_truncated', 'ar_answer_truncated', 'score')


class DataURLTable(Tables.Table):
    no = Tables.Column(empty_values=(), verbose_name='تسلسل')
    url = Tables.URLColumn(text='رابط', verbose_name="الرابط")
    title = Tables.Column(verbose_name="العنوان")
    get_text_trancated = Tables.Column(verbose_name="النص")
    data_type = Tables.Column(verbose_name="نوع المصدر")
    pub_date = Tables.Column(verbose_name="تاريخ الاضافة")
    edit_doc = Tables.LinkColumn('edit_data', verbose_name="تعديل" ,text='عدّل', args=[A("pk")])
    passages = Tables.LinkColumn('view_passages', verbose_name="الفقرات" ,text='اعرض', args=[A("pk")])
    gen_passages = Tables.LinkColumn('sentences_split', verbose_name="stanza" ,text='استخرج', args=[A('pk')])
    lang_chain = Tables.LinkColumn('langchain_split', verbose_name="langChain" ,text='استخرج', args=[A('pk')])
    delete = Tables.LinkColumn('delete_data', verbose_name="del", text='delete', args=[A('pk')])

    

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.row_counter = 0


    def render_no(self):
        self.row_counter += 1
        return self.row_counter
    

    class Meta:
        model=DataURL
        fields = ('no', 'url', 'title', 'get_text_trancated', 'data_type', 'pub_date')



class PassagesTable(Tables.Table):
    knowledge = Tables.Column(verbose_name='المصدر')
    text = Tables.Column(verbose_name='النص')
    get_translate_truncated = Tables.Column(verbose_name='الترجمة')
    translate_this = Tables.LinkColumn('translate_this', verbose_name='ترجم', text='ترجم', args=[A('pk')])
    edit = Tables.LinkColumn('edit_passage',verbose_name='تعديل', text='تعديل', args=[A('pk')])
    delete = Tables.LinkColumn('delete_passage',verbose_name='حذف' , text='حذف', args=[A('pk')])
    split = Tables.LinkColumn('manual_split', verbose_name='تقسيم', text='قسم',args=[A('pk')])
    embeddings = Tables.LinkColumn('generate_embeddings', verbose_name='embeddings', text='embedd', args=[A('pk')])

    # class Meta:
    #     model = Passage
    #     fields = ('knowledge', 'text', 'get_translate_truncated')
