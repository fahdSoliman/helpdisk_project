from django import forms
from .models import DataURL, Passage, QA




class QA_Form(forms.ModelForm):
    class Meta:
        model=QA
        fields = [
            'question',
            'ar_question',
            'answer',
            'ar_answer',
            'score'
        ]

class DataForm(forms.ModelForm):
    class Meta:
        model = DataURL
        fields = '__all__'


class PassageForm(forms.ModelForm):
    class Meta:
        model = Passage
        fields = [
            'knowledge',
            'text',
            'translate',
            'translated'
        ]