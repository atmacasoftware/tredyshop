from django.urls import path
from apis.views import *

urlpatterns = [
    path('apits/products/', ProductApiView.as_view()),
    path('apits/all/products/', AllProductApiView.as_view()),
    path('apits/secondcategory/', SecondCategoryApiView.as_view()),
    path('apits/thirdcategory/', ThirdCategoryApiView.as_view()),
    path('apits/flash-deal/', FlashDealProductApiView.as_view()),
    path('apits/new-product/', NewProductApiView.as_view()),
    path('apits/en-begenilenler/', MostLikeroductApiView.as_view()),
    path('apits/en-cok-yorumlananlar/', MostPointProductApiView.as_view()),
    path('apits/ust-giyim-urunleri/', UstGiyimUrunleriApiView.as_view()),
    path('apits/alt-giyim-urunleri/', AltGiyimUrunleriApiView.as_view()),
    path('apits/esofman-urunleri/', EsofmanUrunleriApiView.as_view()),
    path('apits/elbise-urunleri/', ElbiseUrunleriApiView.as_view()),
    path('apits/ayakkabi-urunleri/', AyakkabiUrunleriApiView.as_view()),
    path('apits/aksesuar-urunleri/', AksesuarUrunleriApiView.as_view()),
    path('apits/ic-giyim-urunleri/', IcGiyimUrunleriApiView.as_view()),
    path('apits/en-cok-satilan/', MostSellerApiView.as_view()),
    path('apits/super-firsatlar/', FlashDealsApiView.as_view()),
    path('apits/header-kategoriler/', FrontendHeaderCategoryApiView.as_view()),
    path('apits/banner/', BannerApiView.as_view()),
]
