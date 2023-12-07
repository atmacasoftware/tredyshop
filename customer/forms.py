from django import forms
from customer.models import *
from orders.models import ExtraditionRequest


class AddressForm(forms.ModelForm):
    tc = forms.IntegerField(widget=forms.NumberInput(attrs={'type': 'number', 'max_length': 11, "required": 'false'}),
                            label="T.C. Kimlik Numarası")

    mobile = forms.CharField(widget=forms.TextInput(attrs={'type': 'text', 'placeholder': "(555) 555-5555", 'min': 11}),
                             label="Cep Telefonu")

    class Meta:
        model = CustomerAddress
        fields = '__all__'
        exclude = ['user', 'created_at', 'updated_at', 'is_active']
        widgets = {
            'address': forms.Textarea(attrs={'rows': 2, 'cols': 15}),
        }

    def __init__(self, *args, **kwargs):
        super(AddressForm, self).__init__(*args, **kwargs)
        self.fields['county'].queryset = County.objects.none()
        self.fields['tc'].required = False
        if 'city' in self.data:
            try:
                city_id = int(self.data.get('city'))
                self.fields['county'].queryset = County.objects.filter(city_id=city_id).order_by('title')
            except (ValueError, TypeError):
                pass  # invalid input from the client; ignore and fallback to empty City queryset
        elif self.instance.pk:
            self.fields['county'].queryset = self.instance.city.county_set.order_by('title')

        for field_name, field in self.fields.items():
            if field.widget.attrs.get('class'):
                field.widget.attrs['class'] += 'form-control'
            else:
                field.widget.attrs['class'] = 'form-control'


class ExtraditionRequestForm(forms.ModelForm):
    class Meta:
        model = ExtraditionRequest
        fields = '__all__'
        exclude = ['user','created_at', 'updated_at']

    def __init__(self, *args, **kwargs):
        super(ExtraditionRequestForm, self).__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            if field.widget.attrs.get('class'):
                field.widget.attrs['class'] += ' form-control'
            else:
                field.widget.attrs['class'] = 'form-control'
