from django.urls import path
from categorymodel.views import *

urlpatterns = [
    path('ajax-select-subcategory/', SubCategoryList.as_view()),
    path('ajax-select-subbottomcategory/', SubBottomCategoryList.as_view()),
    path('ana-kategoriler/<str:slug>/', MainCategory, name="first_category"),
    path('alt-kategoriler/<str:slug>/', SubCategory, name="second_category"),
    path('en-alt-kategoriler/<str:slug>/', SubBottomCategory, name="third_category"),
    path('ajax/subbottomcategory/', load_all_subbottomcategories, name="load_all_subbottomcategories"),
]
