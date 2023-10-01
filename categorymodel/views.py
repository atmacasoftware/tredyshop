from django.http import JsonResponse
from django.shortcuts import render
from categorymodel.models import *
# Create your views here.
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated

class SubCategoryList(APIView):
    permission_classes = [IsAuthenticated,]
    def post(self, request, format = None):
        category = request.data['category']
        subcategory = {}
        if category:
            subcategory = MainCategory.objects.get(id=category).subcategories.all()
            subcategory = {p.title:p.id for p in subcategory}
        return JsonResponse(data=subcategory, safe=False)

class SubBottomCategoryList(APIView):
    permission_classes = [IsAuthenticated,]
    def post(self, request, format = None):
        subcategory = request.data['category']
        subbottomcategory = {}
        if subcategory:
            subbottomcategory = SubCategory.objects.get(id=subcategory).subbottomcategories.all()
            subbottomcategory = {p.title:p.id for p in subbottomcategory}
        return JsonResponse(data=subbottomcategory, safe=False)


def load_subcategories(request):
    category_id = request.GET.get('category')
    subcategories = SubCategory.objects.filter(maincategory_id=category_id)
    return render(request, 'frontend/partials/ajax/load_subcategories.html', {'category': subcategories})

def load_subbottomcategories(request):
    subcategory_id = request.GET.get('subcategory')
    subbottomcategories = SubBottomCategory.objects.filter(subcategory_id=subcategory_id)
    return render(request, 'frontend/partials/ajax/load_subbottomcategories.html', {'category': subbottomcategories})