from django import forms
from uuid import uuid4

from .models import TextElement, CharInputElement, TextInputElement, EmailInputElement, NumberInputElement, MultipleChoiceElement, MultipleChoiceChoice, SingleChoiceElement, SingleChoiceChoice, AgreeDisagree, AgreeDisagreeRow, UserQuiz
from ckeditor_uploader.widgets import CKEditorUploadingWidget

class TextElementForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    content = forms.CharField(widget=CKEditorUploadingWidget())
    class Meta:
        model = TextElement
        fields = ['content', ]



class CharInputElementForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['title'].widget = forms.TextInput(attrs={'field_title': "Enter a title for your question", 'maxlength': 100, 'class': 'w-100 form-control border-dark '},)

    class Meta:
        model = CharInputElement
        fields = ['title', ]


class TextInputElementForm(CharInputElementForm):
    class Meta:
        model = TextInputElement
        fields = ['title', ]


class EmailInputElementForm(CharInputElementForm):
    class Meta:
        model = EmailInputElement
        fields = ['title', ]


class NumberInputElementForm(CharInputElementForm):
    class Meta:
        model = NumberInputElement
        fields = ['title', ]

class MultipleChoiceElementForm(CharInputElementForm):
    class Meta:
        model = MultipleChoiceElement
        fields = ['title', ]

class MultipleChoiceChoiceForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['choice'].widget = forms.TextInput(attrs={'field_title': "Enter a name for your choice", 'maxlength': 100, 'class': 'w-100 form-control border-dark'},)

    class Meta:
        model = MultipleChoiceChoice
        fields = ['choice', ]

class SingleChoiceElementForm(CharInputElementForm):
    class Meta:
        model = SingleChoiceElement
        fields = ['title', ]



class SingleChoiceChoiceForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['choice'].widget = forms.TextInput(attrs={'field_title': "Enter a name for your choice", 'maxlength': 100, 'class': 'w-100 form-control border-dark'},)

    class Meta:
        model = SingleChoiceChoice
        fields = ['choice', ]


class AgreeDisagreeElementForm(CharInputElementForm):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['title'].widget = forms.TextInput(attrs={'field_title': "Enter a title for your agree disagree section", 'maxlength': 100, 'class': 'w-100 form-control border-dark '},)

    class Meta:
        model = AgreeDisagree
        fields = ['title', ]

class AgreeDisagreeRowForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['title'].widget = forms.TextInput(attrs={'field_title': "Enter your question here", 'maxlength': 10000, 'class': 'w-100 form-control border-dark'},)

    class Meta:
        model = AgreeDisagreeRow
        fields = ['title', ]


class QuizConfirmationForm(forms.ModelForm):

    class Meta:
        model = UserQuiz
        fields = ['quiz_confirmation_content', ]