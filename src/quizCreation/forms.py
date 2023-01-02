from django import forms
from ckeditor.widgets import CKEditorWidget

from .models import TextElement

class TextElementForm(forms.ModelForm):
    content = forms.CharField(widget=CKEditorWidget())
    class Meta:
        model = TextElement
        fields = ['content', ]
