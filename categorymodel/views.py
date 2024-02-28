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

def load_categories(request):
    categories = SubBottomCategory.objects.all()
    return render(request,
                  '../templates/backend/yonetim/partials/load_subbottomcategories.html', {'category': categories})

def load_all_subbottomcategories(request):
    subbottomcategories = SubBottomCategory.objects.all()
    return render(request,
                  '../templates/backend/yonetim/partials/load_subbottomcategories.html', {'category': subbottomcategories})