from django import forms
from adminpage.models import *
from categorymodel.models import *
from mainpage.models import Slider
from orders.models import Order, ExtraditionRequestResult
from product.models import ApiProduct
from trendyol.models import TrendyolOrders


class SliderForm(forms.ModelForm):
    class Meta:
        model = Slider
        fields = '__all__'
        exclude = ['slug', 'created_at', 'updated_at']

    def __init__(self, *args, **kwargs):
        super(SliderForm, self).__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            if field.widget.attrs.get('class'):
                field.widget.attrs['class'] += ' form-control'
            else:
                field.widget.attrs['class'] = 'form-control'

class BannerOneForm(forms.ModelForm):
    class Meta:
        model = BannerOne
        fields = '__all__'
        exclude = ['created_at', 'updated_at']

    def __init__(self, *args, **kwargs):
        super(BannerOneForm, self).__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            if field.widget.attrs.get('class'):
                field.widget.attrs['class'] += ' form-control'
            else:
                field.widget.attrs['class'] = 'form-control'


class BannerTwoForm(forms.ModelForm):
    class Meta:
        model = BannerTwo
        fields = '__all__'
        exclude = ['created_at', 'updated_at']

    def __init__(self, *args, **kwargs):
        super(BannerTwoForm, self).__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            if field.widget.attrs.get('class'):
                field.widget.attrs['class'] += ' form-control'
            else:
                field.widget.attrs['class'] = 'form-control'

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
        exclude = ['tax_amount','price_amount','created_at', 'updated_at']

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
        exclude = ['tax_amount','price_amount','created_at', 'updated_at']

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
        exclude = ['tax_amount','price_amount','created_at', 'updated_at']

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
        exclude = ['tax_amount','price_amount','created_at', 'updated_at']

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


class AboutUsForm(forms.ModelForm):
    class Meta:
        model = Hakkimizda
        fields = '__all__'
        exclude = ['category_count', 'product_count', 'created_at', 'updated_at']

    def __init__(self, *args, **kwargs):
        super(AboutUsForm, self).__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            if field.widget.attrs.get('class'):
                field.widget.attrs['class'] += ' form-control'
            else:
                field.widget.attrs['class'] = 'form-control'


class OrderForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = '__all__'
        exclude = ['created_at', 'updated_at']

    def __init__(self, *args, **kwargs):
        super(OrderForm, self).__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            if field.widget.attrs.get('class'):
                field.widget.attrs['class'] += ' form-control'
            else:
                field.widget.attrs['class'] = 'form-control'


class ExtraditionRequestResultForm(forms.ModelForm):
    class Meta:
        model = ExtraditionRequestResult
        fields = '__all__'
        exclude = ['extraditionrequest', 'created_at', 'updated_at']

    def __init__(self, *args, **kwargs):
        super(ExtraditionRequestResultForm, self).__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            if field.widget.attrs.get('class'):
                field.widget.attrs['class'] += ' form-control'
            else:
                field.widget.attrs['class'] = 'form-control'


class ProductForm(forms.ModelForm):
    class Meta:
        model = ApiProduct
        fields = ['title', 'model_code','barcode', 'stock_code', 'xml_id', 'dropshipping', 'category','subcategory', 'subbottomcategory', 'brand',
                  'description', 'trendyol_category_id', 'image_url1', 'image_url2', 'image_url3', 'image_url4', 'image_url5',
                  'image_url6', 'image_url7', 'image_url8', 'price', 'discountprice', 'quantity', 'trendyol_price', 'hepsiburada_price', 'pttavm_price',
                  'is_discountprice', 'color', 'size', 'fabrictype', 'height','waist','pattern','armtype', 'collartype',
                  'weavingtype', 'material', 'environment','legtype','pocket', 'age_group', 'sex', 'is_publish', 'is_active', 'is_publish_trendyol', 'sell_count', 'slug', 'detail'
                  ]
        exclude = ['created_at', 'updated_at','status']

    def __init__(self, *args, **kwargs):
        super(ProductForm, self).__init__(*args, **kwargs)
        self.fields['subcategory'].queryset = SubCategory.objects.none()
        self.fields['subbottomcategory'].queryset = SubBottomCategory.objects.none()
        if 'category' in self.data:
            try:
                category_id = int(self.data.get('category'))
                self.fields['subcategory'].queryset = SubCategory.objects.filter(maincategory_id=category_id).order_by(
                    'title')
            except (ValueError, TypeError):
                pass
        elif self.instance.pk:
            self.fields['subcategory'].queryset = self.instance.category.subcategories.order_by('title')

        if 'subcategory' in self.data:
            try:
                subcategory_id = int(self.data.get('subcategory'))
                self.fields['subbottomcategory'].queryset = SubBottomCategory.objects.filter(subcategory_id=subcategory_id).order_by(
                    'title')
            except (ValueError, TypeError):
                pass
        elif self.instance.pk:
            self.fields['subbottomcategory'].queryset = self.instance.subcategory.subbottomcategories.order_by('title')

        for field_name, field in self.fields.items():
            if field.widget.attrs.get('class'):
                field.widget.attrs['class'] += 'form-control'
            else:
                field.widget.attrs['class'] = 'form-control'


class TrendyolOrderForm(forms.ModelForm):
    order_date = forms.DateField(widget=forms.TextInput(attrs={'type': 'date'}),label="Sipariş Tarihi")
    class Meta:
        model = TrendyolOrders
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super(TrendyolOrderForm, self).__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            if field.widget.attrs.get('class'):
                field.widget.attrs['class'] += ' form-control'
            else:
                field.widget.attrs['class'] = 'form-control'