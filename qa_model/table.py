import django_tables2 as Tables
from .models import DataURL, Passage
from django_tables2.utils import A

class DataURLTable(Tables.Table):
    edit_doc = Tables.LinkColumn('edit_data', text='edit', args=[A("pk")])
    delete = Tables.LinkColumn('delete_data', text='delete', args=[A('pk')])
    passages = Tables.LinkColumn('view_passages', text='view', args=[A("pk")])
    gen_passages = Tables.LinkColumn('sentences_split', text='extract', args=[A('pk')])
    class Meta:
        model=DataURL
        fields = ('id', 'title','get_text_trancated', 'data_type', 'pub_date')
    # # def render_delete(self):
    # #     return format_html()
    # def render_text(self):
    #     return Truncator(self.text).words(20)



class PassagesTable(Tables.Table):
    knowledge = Tables.Column(verbose_name='المصدر')
    text = Tables.Column(verbose_name='النص')
    get_translate_truncated = Tables.Column(verbose_name='الترجمة')
    translate_this = Tables.LinkColumn('translate_this', verbose_name='ترجم', text='ترجم', args=[A('pk')])
    edit = Tables.LinkColumn('edit_passage',verbose_name='تعديل', text='تعديل', args=[A('pk')])
    delete = Tables.LinkColumn('delete_passage',verbose_name='حذف' , text='حذف', args=[A('pk')])
    split = Tables.LinkColumn('manual_split', verbose_name='تقسيم', text='قسم',args=[A('pk')])

    # class Meta:
    #     model = Passage
    #     fields = ('knowledge', 'text', 'get_translate_truncated')
