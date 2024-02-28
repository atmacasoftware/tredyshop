from django import forms
from django.forms import inlineformset_factory

from adminpage.models import *
from blog.models import Blog, BlogCategory
from categorymodel.models import *
from orders.models import Order, ExtraditionRequestResult
from product.models import *
from trendyol.models import TrendyolOrders, TrendyolCommission

class MainCategoryForm(forms.ModelForm):
    class Meta:
        model = MainCategory
        fields = '__all__'
        exclude = ['slug', 'created_at', 'updated_at']
        widgets = {
            'is_active': forms.CheckboxInput(attrs={'class': 'custom-control-input '})
        }

    def __init__(self, *args, **kwargs):
        super(MainCategoryForm, self).__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            if field.widget.attrs.get('class'):
                field.widget.attrs['class'] += 'form-control rounded-4'
            else:
                field.widget.attrs['class'] = 'form-control rounded-4'


class SubCategoryForm(forms.ModelForm):
    class Meta:
        model = SubCategory
        fields = '__all__'
        exclude = ['slug', 'maincategory', 'created_at', 'updated_at']
        widgets = {
            'is_active': forms.CheckboxInput(attrs={'class': 'custom-control-input '})
        }

    def __init__(self, *args, **kwargs):
        super(SubCategoryForm, self).__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            if field.widget.attrs.get('class'):
                field.widget.attrs['class'] += ' form-control rounded-4'
            else:
                field.widget.attrs['class'] = 'form-control rounded-4'


class SubBottomCategoryForm(forms.ModelForm):
    class Meta:
        model = SubBottomCategory
        fields = '__all__'
        exclude = ['slug', 'maincategory', 'subcategory', 'created_at', 'updated_at']
        widgets = {
            'is_active': forms.CheckboxInput(attrs={'class': 'custom-control-input '})
        }

    def __init__(self, *args, **kwargs):
        super(SubBottomCategoryForm, self).__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            if field.widget.attrs.get('class'):
                field.widget.attrs['class'] += ' form-control rounded-4'
            else:
                field.widget.attrs['class'] = 'form-control rounded-4'


class SiteSettingsForm(forms.ModelForm):
    class Meta:
        model = SiteSetting
        fields = '__all__'
        exclude = ['create_at', 'update_at']
        widgets = {
            'google_analytics': forms.TextInput(attrs={'class': 'codeeditor '})
        }

    def __init__(self, *args, **kwargs):
        super(SiteSettingsForm, self).__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            if field.widget.attrs.get('class'):
                field.widget.attrs['class'] += ' form-control rounded-4'
            else:
                field.widget.attrs['class'] = 'form-control rounded-4'

class IssuedInvoicesAddForm(forms.ModelForm):
    edited_date = forms.DateField(widget=forms.TextInput(attrs={'type': 'date'}))

    class Meta:
        model = IssuedInvoices
        fields = '__all__'
        exclude = ['tax_amount','price_amount','created_at','is_cancelling', 'updated_at']
        widgets = {
            'tax_number': forms.NumberInput(attrs={'value': '11111111111'})
        }

    def __init__(self, *args, **kwargs):
        super(IssuedInvoicesAddForm, self).__init__(*args, **kwargs)
        self.fields['edited_date'].label = "Fatura Tarihi"
        for field_name, field in self.fields.items():
            if field.widget.attrs.get('class'):
                field.widget.attrs['class'] += ' form-control rounded-4'
            else:
                field.widget.attrs['class'] = 'form-control rounded-4'


class IssuedInvoicesUpdateForm(forms.ModelForm):
    edited_date = forms.DateField(widget=forms.TextInput(attrs={'type': 'date'}))

    class Meta:
        model = IssuedInvoices
        fields = '__all__'
        exclude = ['tax_amount','price_amount','created_at', 'updated_at']
        widgets = {
            'tax_number': forms.NumberInput(attrs={'value': '11111111111'})
        }

    def __init__(self, *args, **kwargs):
        super(IssuedInvoicesUpdateForm, self).__init__(*args, **kwargs)
        self.fields['edited_date'].label = "Fatura Tarihi"
        for field_name, field in self.fields.items():
            if field.widget.attrs.get('class'):
                field.widget.attrs['class'] += ' form-control rounded-4'
            else:
                field.widget.attrs['class'] = 'form-control rounded-4'

class InvoicesReceivedAddForm(forms.ModelForm):
    class Meta:
        model = InvoicesReceived
        fields = '__all__'
        exclude = ['tax_amount','price_amount','is_cancelling','created_at', 'updated_at']

    def __init__(self, *args, **kwargs):
        super(InvoicesReceivedAddForm, self).__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            if field.widget.attrs.get('class'):
                field.widget.attrs['class'] += ' form-control rounded-4'
            else:
                field.widget.attrs['class'] = 'form-control rounded-4'


class InvoicesReceivedUpdateForm(forms.ModelForm):
    class Meta:
        model = InvoicesReceived
        fields = '__all__'
        exclude = ['tax_amount','price_amount','created_at', 'updated_at']

    def __init__(self, *args, **kwargs):
        super(InvoicesReceivedUpdateForm, self).__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            if field.widget.attrs.get('class'):
                field.widget.attrs['class'] += ' form-control rounded-4'
            else:
                field.widget.attrs['class'] = 'form-control rounded-4'

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


class HepsiburadaForm(forms.ModelForm):
    class Meta:
        model = Hepsiburada
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super(HepsiburadaForm, self).__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            if field.widget.attrs.get('class'):
                field.widget.attrs['class'] += ' form-control rounded-4'
            else:
                field.widget.attrs['class'] = 'form-control rounded-4'

class AboutUsForm(forms.ModelForm):
    class Meta:
        model = Hakkimizda
        fields = '__all__'
        exclude = ['category_count', 'product_count', 'created_at', 'updated_at']

    def __init__(self, *args, **kwargs):
        super(AboutUsForm, self).__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            if field.widget.attrs.get('class'):
                field.widget.attrs['class'] += ' form-control rounded-4'
            else:
                field.widget.attrs['class'] = 'form-control rounded-4'


class OrderForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = '__all__'
        exclude = ['created_at', 'updated_at']

    def __init__(self, *args, **kwargs):
        super(OrderForm, self).__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            if field.widget.attrs.get('class'):
                field.widget.attrs['class'] += ' form-control rounded-4'
            else:
                field.widget.attrs['class'] = 'form-control rounded-4'


class ExtraditionRequestResultForm(forms.ModelForm):
    class Meta:
        model = ExtraditionRequestResult
        fields = '__all__'
        exclude = ['extraditionrequest', 'created_at', 'updated_at']

    def __init__(self, *args, **kwargs):
        super(ExtraditionRequestResultForm, self).__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            if field.widget.attrs.get('class'):
                field.widget.attrs['class'] += ' form-control rounded-4'
            else:
                field.widget.attrs['class'] = 'form-control rounded-4'


class ProductForm(forms.ModelForm):
    class Meta:
        model = ApiProduct
        fields = ['title','brand', 'description', 'model_code','barcode', 'stock_code', 'xml_id', 'dropshipping', 'category','subcategory', 'subbottomcategory',  'trendyol_category_id','image_url1', 'image_url2', 'image_url3', 'image_url4', 'image_url5',
                  'image_url6', 'image_url7', 'image_url8', 'price', 'discountprice', 'quantity', 'trendyol_price',
                  'is_discountprice', 'color', 'size', 'fabrictype', 'height','waist','pattern','armtype', 'collartype',
                  'weavingtype', 'material', 'environment','legtype','pocket','heeltype','heelsize', 'age_group', 'sextype','warranty', 'sleepmode','casetype','tabletmodel', 'compatible','bag_pattern', 'bijuteri_theme','is_publish', 'is_publish_trendyol', 'detail',  'slug'
                  ]
        exclude = ['created_at', 'updated_at','status']

    def __init__(self, *args, **kwargs):
        super(ProductForm, self).__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            if field.widget.attrs.get('class'):
                field.widget.attrs['class'] += 'form-control rounded-4'
            else:
                field.widget.attrs['class'] = 'form-control rounded-4'

class ErrorProductForm(forms.ModelForm):
    class Meta:
        model = ApiProduct
        fields = ['title', 'brand', 'description', 'model_code', 'barcode', 'stock_code', 'xml_id', 'dropshipping',
                  'category', 'subcategory', 'subbottomcategory', 'trendyol_category_id', 'image_url1', 'image_url2',
                  'image_url3', 'image_url4', 'image_url5',
                  'image_url6', 'image_url7', 'image_url8', 'price', 'discountprice', 'quantity', 'trendyol_price',
                  'is_discountprice', 'color', 'size', 'fabrictype', 'height', 'waist', 'pattern', 'armtype',
                  'collartype',
                  'weavingtype', 'material', 'environment', 'legtype', 'pocket', 'heeltype', 'heelsize', 'age_group',
                  'sextype', 'warranty', 'sleepmode', 'casetype', 'tabletmodel', 'compatible', 'bag_pattern', 'bijuteri_theme',
                  'is_publish', 'is_publish_trendyol', 'detail', 'slug'
                  ]
        exclude = ['created_at', 'updated_at','status']

    def __init__(self, *args, **kwargs):
        super(ErrorProductForm, self).__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            if field.widget.attrs.get('class'):
                field.widget.attrs['class'] += 'form-control rounded-4'
            else:
                field.widget.attrs['class'] = 'form-control rounded-4'

class TrendyolOrderForm(forms.ModelForm):
    order_date = forms.DateField(widget=forms.TextInput(attrs={'type': 'date'}),label="Sipariş Tarihi")

    class Meta:
        model = TrendyolOrders
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super(TrendyolOrderForm, self).__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            if field.widget.attrs.get('class'):
                field.widget.attrs['class'] += ' form-control rounded-4'
            else:
                field.widget.attrs['class'] = 'form-control rounded-4'


class TrendyolUpdateOrderForm(forms.ModelForm):
    class Meta:
        model = TrendyolOrders
        fields = '__all__'
        exclude = ['order_date']

    def __init__(self, *args, **kwargs):
        super(TrendyolUpdateOrderForm, self).__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            if field.widget.attrs.get('class'):
                field.widget.attrs['class'] += ' form-control rounded-4'
            else:
                field.widget.attrs['class'] = 'form-control rounded-4'

class HarcamalarForm(forms.ModelForm):
    created_at = forms.DateField(widget=forms.TextInput(attrs={'type': 'date'}),label="Harcama Tarihi")

    class Meta:
        model = Harcamalar
        fields = ["harcama_tipi","harcama_adi","harcama_tutari","harcama_notu","durum", "created_at"]
        exclude = ["updated_at"]
        widgets = {
            'harcama_notu': forms.Textarea(attrs={'rows': 2, 'cols': 15}),
        }

    def __init__(self, *args, **kwargs):
        super(HarcamalarForm, self).__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            if field.widget.attrs.get('class'):
                field.widget.attrs['class'] += ' form-control rounded-4'
            else:
                field.widget.attrs['class'] = 'form-control rounded-4'

class TrendyolCommissionForm(forms.ModelForm):

    class Meta:
        model = TrendyolCommission
        fields = "__all__"
        exclude = ["create_at","update_at"]

    def __init__(self, *args, **kwargs):
        super(TrendyolCommissionForm, self).__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            if field.widget.attrs.get('class'):
                field.widget.attrs['class'] += ' form-control rounded-4'
            else:
                field.widget.attrs['class'] = 'form-control rounded-4'


class IzinForm(forms.ModelForm):
    class Meta:
        model = Izinler
        fields = '__all__'
        exclude = ['user', 'created_at', 'updated_at']

    def __init__(self, *args, **kwargs):
        super(IzinForm, self).__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            if field.widget.attrs.get('class'):
                field.widget.attrs['class'] += 'custom-control-input'
            else:
                field.widget.attrs['class'] = 'custom-control-input'


class CampaingForm(forms.ModelForm):
    class Meta:
        model = Campaign
        fields = '__all__'
        exclude = ['slug', 'created_at', 'updated_at']
        widgets = {
            'start_date': forms.DateInput(
                format=('%d-%m-%Y'),
                attrs={'class': 'form-control rounded-4',
                       'placeholder': 'Başlangıç Tarihi',
                       'type': 'date'
                       }),
            'end_date': forms.DateInput(
                format=('%d-%m-%Y'),
                attrs={'class': 'form-control rounded-4',
                       'placeholder': 'Bitiş Tarihi',
                       'type': 'date'
                       }),
            'is_publish': forms.CheckboxInput(attrs={'class': 'custom-control-input '}),
        }

    def __init__(self, *args, **kwargs):
        super(CampaingForm, self).__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            if field.widget.attrs.get('class'):
                field.widget.attrs['class'] += 'form-control rounded-4 pl-3 pr-2'
            else:
                field.widget.attrs['class'] = 'form-control rounded-4 pl-3 pr-2'

class TredyShopFiyatAyarlaForm(forms.ModelForm):
    class Meta:
        model = TredyShopFiyatAyarla
        fields = '__all__'
        exclude = ['created_at', 'update_at']

    def __init__(self, *args, **kwargs):
        super(TredyShopFiyatAyarlaForm, self).__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            if field.widget.attrs.get('class'):
                field.widget.attrs['class'] += 'form-control rounded-4'
            else:
                field.widget.attrs['class'] = 'form-control rounded-4'

class TrendyolFiyatAyarlaForm(forms.ModelForm):
    class Meta:
        model = TrendyolFiyatAyarla
        fields = '__all__'
        exclude = ['created_at', 'update_at']

    def __init__(self, *args, **kwargs):
        super(TrendyolFiyatAyarlaForm, self).__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            if field.widget.attrs.get('class'):
                field.widget.attrs['class'] += 'form-control rounded-4'
            else:
                field.widget.attrs['class'] = 'form-control rounded-4'

class HepsiburadaFiyatAyarlaForm(forms.ModelForm):
    class Meta:
        model = HepsiburadaFiyatAyarla
        fields = '__all__'
        exclude = ['created_at', 'update_at']

    def __init__(self, *args, **kwargs):
        super(HepsiburadaFiyatAyarlaForm, self).__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            if field.widget.attrs.get('class'):
                field.widget.attrs['class'] += 'form-control rounded-4'
            else:
                field.widget.attrs['class'] = 'form-control rounded-4'

class CiceksepetiFiyatAyarlaForm(forms.ModelForm):
    class Meta:
        model = CiceksepetiFiyatAyarla
        fields = '__all__'
        exclude = ['created_at', 'update_at']

    def __init__(self, *args, **kwargs):
        super(CiceksepetiFiyatAyarlaForm, self).__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            if field.widget.attrs.get('class'):
                field.widget.attrs['class'] += 'form-control rounded-4'
            else:
                field.widget.attrs['class'] = 'form-control rounded-4'

class PttAvmFiyatAyarlaForm(forms.ModelForm):
    class Meta:
        model = PttAvmFiyatAyarla
        fields = '__all__'
        exclude = ['created_at', 'update_at']

    def __init__(self, *args, **kwargs):
        super(PttAvmFiyatAyarlaForm, self).__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            if field.widget.attrs.get('class'):
                field.widget.attrs['class'] += 'form-control rounded-4'
            else:
                field.widget.attrs['class'] = 'form-control rounded-4'

class TredyShopKarMarjiForm(forms.ModelForm):
    class Meta:
        model = TredyShopKarMarji
        fields = '__all__'
        exclude = ['created_at', 'update_at', 'tredyshop']

    def __init__(self, *args, **kwargs):
        super(TredyShopKarMarjiForm, self).__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            if field.widget.attrs.get('class'):
                field.widget.attrs['class'] += 'form-control rounded-4'
            else:
                field.widget.attrs['class'] = 'form-control rounded-4'

TredyShopKarMarjiFormSet =inlineformset_factory(
    TredyShopFiyatAyarla, TredyShopKarMarji, form=TredyShopKarMarjiForm,
    extra=1, can_delete=False
)

class TrendyolKarMarjiForm(forms.ModelForm):
    class Meta:
        model = TrendyolKarMarji
        fields = '__all__'
        exclude = ['created_at', 'update_at', 'trendyol']

    def __init__(self, *args, **kwargs):
        super(TrendyolKarMarjiForm, self).__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            if field.widget.attrs.get('class'):
                field.widget.attrs['class'] += 'form-control rounded-4'
            else:
                field.widget.attrs['class'] = 'form-control rounded-4'

TrendyolKarMarjiFormSet =inlineformset_factory(
    TrendyolFiyatAyarla, TrendyolKarMarji, form=TrendyolKarMarjiForm,
    extra=1, can_delete=False
)

class HepsiburadaKarMarjiForm(forms.ModelForm):
    class Meta:
        model = HepsiburadaKarMarji
        fields = '__all__'
        exclude = ['created_at', 'update_at', 'hepsiburada']

    def __init__(self, *args, **kwargs):
        super(HepsiburadaKarMarjiForm, self).__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            if field.widget.attrs.get('class'):
                field.widget.attrs['class'] += 'form-control rounded-4'
            else:
                field.widget.attrs['class'] = 'form-control rounded-4'

HepsiburadaKarMarjiFormSet =inlineformset_factory(
    HepsiburadaFiyatAyarla, HepsiburadaKarMarji, form=HepsiburadaKarMarjiForm,
    extra=1, can_delete=False
)

class CiceksepetiKarMarjiForm(forms.ModelForm):
    class Meta:
        model = CiceksepetiKarMarji
        fields = '__all__'
        exclude = ['created_at', 'update_at', 'amazon']

    def __init__(self, *args, **kwargs):
        super(CiceksepetiKarMarjiForm, self).__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            if field.widget.attrs.get('class'):
                field.widget.attrs['class'] += 'form-control rounded-4'
            else:
                field.widget.attrs['class'] = 'form-control rounded-4'

CiceksepetiKarMarjiFormSet =inlineformset_factory(
    CiceksepetiFiyatAyarla, CiceksepetiKarMarji, form=CiceksepetiKarMarjiForm,
    extra=1, can_delete=False
)

class PttAvmKarMarjiForm(forms.ModelForm):
    class Meta:
        model = PttAvmKarMarji
        fields = '__all__'
        exclude = ['created_at', 'update_at', 'pttavm']

    def __init__(self, *args, **kwargs):
        super(PttAvmKarMarjiForm, self).__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            if field.widget.attrs.get('class'):
                field.widget.attrs['class'] += 'form-control rounded-4'
            else:
                field.widget.attrs['class'] = 'form-control rounded-4'

PttAvmKarMarjiFormSet =inlineformset_factory(
    PttAvmFiyatAyarla, PttAvmKarMarji, form=PttAvmKarMarjiForm,
    extra=1, can_delete=False
)


class BlogCategoryForm(forms.ModelForm):
    class Meta:
        model = BlogCategory
        fields = '__all__'
        exclude = ['user','slug', 'created_at', 'updated_at']

    def __init__(self, *args, **kwargs):
        super(BlogCategoryForm, self).__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            if field.widget.attrs.get('class'):
                field.widget.attrs['class'] += ' form-control rounded-4'
            else:
                field.widget.attrs['class'] = 'form-control rounded-4'

class BlogForm(forms.ModelForm):
    class Meta:
        model = Blog
        fields = '__all__'
        exclude = ['user', 'slug','is_active', 'created_at', 'updated_at', 'blog_views']
        widgets = {
            'is_publish': forms.CheckboxInput(attrs={'class': 'custom-control-input '})
        }

    def __init__(self, *args, **kwargs):
        super(BlogForm, self).__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            if field.widget.attrs.get('class'):
                field.widget.attrs['class'] += ' form-control'
            else:
                field.widget.attrs['class'] = 'form-control'

class TaskDetailForm(forms.ModelForm):
    class Meta:
        model = Task
        fields = ['detail']

    def __init__(self, *args, **kwargs):
        super(TaskDetailForm, self).__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            if field.widget.attrs.get('class'):
                field.widget.attrs['class'] += ' form-control'
            else:
                field.widget.attrs['class'] = 'form-control'