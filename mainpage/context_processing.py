from django.db.models import Count
from django.shortcuts import redirect

from categorymodel.models import *
from mainpage.models import *
from product.models import ReviewRating, ApiProduct


def categories(request):
    maincategories = MainCategory.objects.all().exclude(id=12)
    subcategories = SubCategory.objects.all()
    subbottomcategories = SubBottomCategory.objects.all()

    return dict(maincategories=maincategories, subcategories=subcategories,subbottomcategories=subbottomcategories)


def setting(request):
    setting = Setting.objects.all().last()
    return dict(setting=setting)

def most_search(request):

    search_keywords = MostSearchingKeyword.objects.all().order_by('-count')
    if search_keywords.count() > 5:
        search_keywords = search_keywords[:5]
    return dict(search_keywords=search_keywords)

def top_product(request):
    reviewrating = ReviewRating.objects.all()
    liked_product = ApiProduct.objects.all().filter(reviewrating__rating__gte=4, reviewrating__rating__lte=6)[:3]
    most_count = ApiProduct.objects.filter(reviewrating__in=reviewrating).annotate(rating_count=Count('id')).order_by(
        '-rating_count')[:3]
    most_selling = ApiProduct.objects.all().order_by("-sell_count")[:3]
    return dict(liked_product=liked_product, most_count=most_count, most_selling=most_selling)