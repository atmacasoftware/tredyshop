from django.shortcuts import render
from categorymodel.models import *
from product.models import *


# Create your views here.

def store_page(request, categroy_slug=None, subcategory_slug=None, brands_slug=None):
    context = {}

    brands = Brand.objects.all().filter(brands__category__slug=categroy_slug)
    products = None
    descriptions = DescriptionList.objects.all()

    if categroy_slug != None and subcategory_slug == None and brands_slug == None:
        category_s = MainCategory.objects.get(slug=categroy_slug)
        products = Product.objects.filter(category__slug=categroy_slug)
        context.update({'category_s': category_s, 'products': products})
    elif categroy_slug != None and subcategory_slug != None and brands_slug == None:
        category_s = MainCategory.objects.get(slug=categroy_slug)
        subcategory_s = SubCategory.objects.get(slug=subcategory_slug)
        products = Product.objects.filter(subcategory__slug=subcategory_slug).distinct()
        context.update({'category_s': category_s, 'subcategory_s': subcategory_s, 'products': products})
    elif categroy_slug == None and subcategory_slug == None and brands_slug != None:
        brands_s = Brand.objects.get(slug=brands_slug)
        products = Product.objects.filter(brand__slug=brands_slug)
        context.update({'brands_s': brands_s, 'products': products})


    context.update({'categroy_slug': categroy_slug, 'subcategory_slug': subcategory_slug, 'brands_slug': brands_slug,
                    'brands': brands, 'descriptions': descriptions})

    return render(request, 'frontend/pages/store.html', context)
