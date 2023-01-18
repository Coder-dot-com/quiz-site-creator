from django import forms
from ckeditor.widgets import CKEditorWidget
from uuid import uuid4

from .models import TextElement


class TextElementForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['content'].widget = CKEditorWidget(attrs={'id': uuid4()})
    class Meta:
        model = TextElement
        fields = ['content', ]