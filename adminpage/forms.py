from django import forms
from adminpage.models import *
from categorymodel.models import *


class MainCategoryForm(forms.ModelForm):
    class Meta:
        model = MainCategory
        fields = '__all__'
        exclude = ['slug', 'created_at', 'updated_at']

    def __init__(self, *args, **kwargs):
        super(MainCategoryForm, self).__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            if field.widget.attrs.get('class'):
                field.widget.attrs['class'] += ' form-control'
            else:
                field.widget.attrs['class'] = 'form-control'


class SubCategoryForm(forms.ModelForm):
    class Meta:
        model = SubCategory
        fields = '__all__'
        exclude = ['slug', 'maincategory', 'created_at', 'updated_at']

    def __init__(self, *args, **kwargs):
        super(SubCategoryForm, self).__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            if field.widget.attrs.get('class'):
                field.widget.attrs['class'] += ' form-control'
            else:
                field.widget.attrs['class'] = 'form-control'


class SubBottomCategoryForm(forms.ModelForm):
    class Meta:
        model = SubBottomCategory
        fields = '__all__'
        exclude = ['slug', 'maincategory', 'subcategory', 'created_at', 'updated_at']

    def __init__(self, *args, **kwargs):
        super(SubBottomCategoryForm, self).__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            if field.widget.attrs.get('class'):
                field.widget.attrs['class'] += ' form-control'
            else:
                field.widget.attrs['class'] = 'form-control'

class IssuedInvoicesAddForm(forms.ModelForm):
    edited_date = forms.DateField(widget=forms.TextInput(attrs={'type': 'date'}))

    class Meta:
        model = IssuedInvoices
        fields = '__all__'
        exclude = ['created_at', 'updated_at']

    def __init__(self, *args, **kwargs):
        super(IssuedInvoicesAddForm, self).__init__(*args, **kwargs)
        self.fields['edited_date'].label = "Fatura Tarihi"
        for field_name, field in self.fields.items():
            if field.widget.attrs.get('class'):
                field.widget.attrs['class'] += ' form-control'
            else:
                field.widget.attrs['class'] = 'form-control'


class IssuedInvoicesUpdateForm(forms.ModelForm):
    edited_date = forms.DateField(widget=forms.TextInput(attrs={'type': 'date'}))

    class Meta:
        model = IssuedInvoices
        fields = '__all__'
        exclude = ['created_at', 'updated_at']

    def __init__(self, *args, **kwargs):
        super(IssuedInvoicesUpdateForm, self).__init__(*args, **kwargs)
        self.fields['edited_date'].label = "Fatura Tarihi"
        for field_name, field in self.fields.items():
            if field.widget.attrs.get('class'):
                field.widget.attrs['class'] += ' form-control'
            else:
                field.widget.attrs['class'] = 'form-control'


class InvoicesReceivedAddForm(forms.ModelForm):
    class Meta:
        model = InvoicesReceived
        fields = '__all__'
        exclude = ['created_at', 'updated_at']

    def __init__(self, *args, **kwargs):
        super(InvoicesReceivedAddForm, self).__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            if field.widget.attrs.get('class'):
                field.widget.attrs['class'] += ' form-control'
            else:
                field.widget.attrs['class'] = 'form-control'


class InvoicesReceivedUpdateForm(forms.ModelForm):
    class Meta:
        model = InvoicesReceived
        fields = '__all__'
        exclude = ['created_at', 'updated_at']

    def __init__(self, *args, **kwargs):
        super(InvoicesReceivedUpdateForm, self).__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            if field.widget.attrs.get('class'):
                field.widget.attrs['class'] += ' form-control'
            else:
                field.widget.attrs['class'] = 'form-control'


class TrendyolAddForm(forms.ModelForm):
    class Meta:
        model = Trendyol
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super(TrendyolAddForm, self).__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            if field.widget.attrs.get('class'):
                field.widget.attrs['class'] += ' form-control'
            else:
                field.widget.attrs['class'] = 'form-control'


class TrendyolUpdateForm(forms.ModelForm):
    class Meta:
        model = Trendyol
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super(TrendyolUpdateForm, self).__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            if field.widget.attrs.get('class'):
                field.widget.attrs['class'] += ' form-control'
            else:
                field.widget.attrs['class'] = 'form-control'
