from django import forms
from adminpage.models import Trendyol

class TrendyolAddForm(forms.ModelForm):
    class Meta:
        model = Trendyol
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super(TrendyolAddForm, self).__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            if field.widget.attrs.get('class'):
                field.widget.attrs['class'] += ' form-control rounded-4'
            else:
                field.widget.attrs['class'] = 'form-control rounded-4'


class TrendyolUpdateForm(forms.ModelForm):
    class Meta:
        model = Trendyol
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super(TrendyolUpdateForm, self).__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            if field.widget.attrs.get('class'):
                field.widget.attrs['class'] += ' form-control rounded-4'
            else:
                field.widget.attrs['class'] = 'form-control rounded-4'