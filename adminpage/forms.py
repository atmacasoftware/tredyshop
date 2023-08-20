from django import forms
from adminpage.models import *

class IssuedInvoicesAddForm(forms.ModelForm):
    edited_date = forms.DateField(widget=forms.TextInput(attrs={'type': 'date'}))

    class Meta:
        model = IssuedInvoices
        fields = '__all__'
        exclude = ['created_at', 'updated_at']

    def __init__(self, *args, **kwargs):
        super(IssuedInvoicesAddForm, self).__init__(*args, **kwargs)
        self.fields['edited_date'].label = "Fatura Düzenlenme Tarihi"
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
        self.fields['edited_date'].label = "Fatura Düzenlenme Tarihi"
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