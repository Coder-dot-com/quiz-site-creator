from django import forms
from uuid import uuid4

from .models import TextElement, CharInputElement, TextInputElement, EmailInputElement, NumberInputElement, MultipleChoiceElement, MultipleChoiceChoice, SingleChoiceElement, SingleChoiceChoice, AgreeDisagree, AgreeDisagreeRow, UserQuiz, SatisfiedUnsatisfied, SatisfiedUnsatisfiedRow, ReviewStars, Dropdown
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
        self.fields['required'].widget = forms.CheckboxInput(attrs={'field_title': "Tick to make this question required", 'class': ' border-dark ', 'checked': 'checked'},)

    class Meta:
        model = CharInputElement
        fields = ['title',  'required']


class TextInputElementForm(CharInputElementForm):
    class Meta:
        model = TextInputElement
        fields = ['title',  'required']

class DropdownForm(CharInputElementForm):
    class Meta:
        model = Dropdown
        fields = ['title',  'required']


class EmailInputElementForm(CharInputElementForm):
    class Meta:
        model = EmailInputElement
        fields = ['title',  'required']


class NumberInputElementForm(CharInputElementForm):
    class Meta:
        model = NumberInputElement
        fields = ['title',  'required']

class ReviewStarsForm(CharInputElementForm):
    class Meta:
        model = ReviewStars
        fields = ['title',  'required']

class MultipleChoiceElementForm(CharInputElementForm):
    class Meta:
        model = MultipleChoiceElement
        fields = ['title',  'required']

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
        fields = ['title',  'required']



class SingleChoiceChoiceForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['choice'].widget = forms.TextInput(attrs={'field_title': "Enter a name for your choice", 'maxlength': 100, 'class': 'w-100 form-control border-dark'},)

    class Meta:
        model = SingleChoiceChoice
        fields = ['choice', ]


class AgreeDisagreeElementForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['title'].widget = forms.TextInput(attrs={'field_title': "Enter a title for your agree disagree section", 'maxlength': 100, 'class': 'w-100 form-control border-dark'},)
        self.fields['title'].required = False

    class Meta:
        model = AgreeDisagree
        fields = ['title', ]

class AgreeDisagreeRowForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['title'].widget = forms.TextInput(attrs={'field_title': "Enter your question here", 'maxlength': 10000, 'class': 'w-100 form-control border-dark'},)
        self.fields['required'].widget = forms.CheckboxInput(attrs={'field_title': "Tick to make this question required", 'class': ' border-dark ', 'checked': 'checked'},)

    class Meta:
        model = AgreeDisagreeRow
        fields = ['title', 'required']


class QuizConfirmationForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

 
    quiz_confirmation_content = forms.CharField(widget=CKEditorUploadingWidget())

    class Meta:
        model = UserQuiz
        fields = ['quiz_confirmation_content', ]


class SatisfiedUnsatisfiedElementForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['title'].widget = forms.TextInput(attrs={'field_title': "Enter a title for your satisfied unsatisfied section", 'maxlength': 100, 'class': 'w-100 form-control border-dark'},)
        self.fields['title'].required = False

    class Meta:
        model = SatisfiedUnsatisfied
        fields = ['title', ]

class SatisfiedUnsatisfiedRowForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['title'].widget = forms.TextInput(attrs={'field_title': "Enter your question here", 'maxlength': 10000, 'class': 'w-100 form-control border-dark'},)
        self.fields['required'].widget = forms.CheckboxInput(attrs={'field_title': "Tick to make this question required", 'class': ' border-dark ', 'checked': 'checked'},)

    class Meta:
        model = SatisfiedUnsatisfiedRow
        fields = ['title', 'required']