from django import forms
from .models import DataURL, Passage




class DataForm(forms.ModelForm):
    class Meta:
        model = DataURL
        fields = '__all__'


class PassageForm(forms.ModelForm):
    class Meta:
        model = Passage
        fields = '__all__'