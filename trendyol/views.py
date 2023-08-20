from django.shortcuts import render, redirect
from trendyol.models import *
from django.contrib.auth.decorators import login_required
import requests
# Create your views here.

@login_required(login_url="/yonetim-paneli/")
def trendyol(request):
    if 'category_add' in request.POST:
        url = 'https://api.trendyol.com/sapigw/product-categories'
        response = requests.request("GET", url)
        for first in response.json()['categories']:
            if TrendyolFirstCategory.objects.filter(id=first['id']).count() < 1:
                data1 = TrendyolFirstCategory.objects.create(id=first['id'], name=first['name'],
                                                             parentId=first['parentId'])
                if first['subCategories'] != []:
                    data1.is_subcategory = True
                    data1.save()

            if first['subCategories'] != []:
                for second in first['subCategories']:
                    if TrendyolSecondCategory.objects.filter(id=second['id']).count() < 1:
                        data2 = TrendyolSecondCategory.objects.create(id=second['id'], name=second['name'],
                                                                      parentId=second['parentId'])

                        if second['subCategories'] != []:
                            data2.is_subcategory = True
                            data2.save()

                    if second['subCategories'] != []:
                        for third in second['subCategories']:
                            if TrendyolThirdCategory.objects.filter(id=third['id']).count() < 1:
                                data3 = TrendyolThirdCategory.objects.create(id=third['id'], name=third['name'],
                                                                             parentId=third['parentId'])
                                if third['subCategories'] != []:
                                    data3.is_subcategory = True
                                    data3.save()

                            if third['subCategories'] != []:
                                for four in third['subCategories']:
                                    if TrendyolFourCategory.objects.filter(id=four['id']).count() < 1:
                                        data4 = TrendyolFourCategory.objects.create(id=four['id'], name=four['name'],
                                                                                    parentId=four['parentId'])
                                        if four['subCategories'] != []:
                                            data4.is_subcategory = True
                                            data4.save()

                                    if four['subCategories'] != []:
                                        for five in four['subCategories']:
                                            if TrendyolFiveCategory.objects.filter(id=five['id']).count() < 1:
                                                data5 = TrendyolFiveCategory.objects.create(id=five['id'],
                                                                                            name=five['name'],
                                                                                            parentId=five['parentId'])
                                                if five['subCategories'] != []:
                                                    data5.is_subcategory = True
                                                    data5.save()

                                            if five['subCategories'] != []:
                                                for six in five['subCategories']:
                                                    if TrendyolSixCategory.objects.filter(id=six['id']).count() < 1:
                                                        data5 = TrendyolSixCategory.objects.create(id=six['id'],
                                                                                                   name=six['name'],
                                                                                                   parentId=six[
                                                                                                       'parentId'])
                                                        if six['subCategories'] != []:
                                                            data5.is_subcategory = True
                                                            data5.save()
        return redirect('trendyol')
    if 'brand_add' in request.POST:
        url = 'https://api.trendyol.com/sapigw/brands'
        response = requests.request("GET", url)
        try:
            for brand in response.json()['brands']:
                if TrendyolBrand.objects.filter(id=brand['id']).count() < 1:
                    TrendyolBrand.objects.create(id=brand['id'], name=brand['name'])
        except:
            pass
        return redirect('trendyol')

    return render(request, "backend/pages/trendyol/trendyol.html")


@login_required(login_url="/yonetim-paneli/")
def trendyol_product(request):
    return render(request, "backend/pages/trendyol/trendyol_product.html")