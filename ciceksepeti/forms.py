from django import forms
from ciceksepeti.models import *

class CicekSepetiHesapBilgileri(forms.ModelForm):
    class Meta:
        model = Ciceksepeti
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super(CicekSepetiHesapBilgileri, self).__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            if field.widget.attrs.get('class'):
                field.widget.attrs['class'] += ' form-control rounded-4'
            else:
                field.widget.attrs['class'] = 'form-control rounded-4'