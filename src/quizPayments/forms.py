from django import forms
from .models import Product
from ckeditor_uploader.widgets import CKEditorUploadingWidget



class ProductCreateForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for visible in self.visible_fields():
            visible.field.widget.attrs['class'] = 'form-control input-default w-100 '

    description = forms.CharField(widget=CKEditorUploadingWidget())
        
    class Meta:
        model = Product
        fields = ['name', 'price', 'currency', 'require_shipping_information', 'description',]
