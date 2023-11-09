from django.http import HttpResponse
from rest_framework.decorators import api_view
from rest_framework.renderers import JSONRenderer
from rest_framework.views import APIView
from rest_framework.response import Response
from apis.serializers import *
from mainpage.models import Slider
from product.models import ApiProduct
from categorymodel.models import *


class SliderApiView(APIView):
    def get(self, request):
        try:
            slider = Slider.objects.filter(is_publish=True)
            serializer = SliderSerializer(slider, many=True)
            return Response({'data': serializer.data})
        except Slider.DoesNotExist:
            return Response({'msg': 'Slider bulunamadı.'})

    def post(self, request):
        return Response({'msg': 'Bu apide post methodu çalışmamaktadır.'})


class AllProductApiView(APIView):
    def get(self, request):
        try:
            product = ApiProduct.objects.all()
            serializer = ProductSerializer(product, many=True)
            return Response({'items': serializer.data})
        except Slider.DoesNotExist:
            return Response({'msg': 'Ürün bulunmamaktadır.'})

    def post(self, request):
        return Response({'msg': 'Bu apide post methodu çalışmamaktadır.'})


class ProductApiView(APIView):
    def get(self, request):
        try:
            product = ApiProduct.objects.filter(is_publish=True, dropshipping="Modaymış")
            serializer = ProductSerializer(product, many=True)
            return Response({'data': serializer.data})
        except Slider.DoesNotExist:
            return Response({'msg': 'Ürün bulunmamaktadır.'})

    def post(self, request):
        return Response({'msg': 'Bu apide post methodu çalışmamaktadır.'})


class SecondCategoryApiView(APIView):
    def get(self, request):
        try:
            category = SubCategory.objects.filter(maincategory_id=1, is_active=True)
            serializer = SecondCategorySerializer(category, many=True)
            json_data = JSONRenderer().render({'data': serializer.data})
            return HttpResponse(json_data, content_type='application/json')
        except Slider.DoesNotExist:
            return Response({'msg': 'Kategori bulunmamaktadır.'})

    def post(self, request):
        return Response({'msg': 'Bu apide post methodu çalışmamaktadır.'})


class ThirdCategoryApiView(APIView):
    def get(self, request):
        try:
            sub_id = self.request.query_params.get('sub_id')
            category = SubBottomCategory.objects.filter(subcategory_id=sub_id, is_active=True)
            serializer = ThirdCategorySerializer(category, many=True)

            return Response({'data': serializer.data})
        except Slider.DoesNotExist:
            return Response({'msg': 'Kategori bulunmamaktadır.'})

    def post(self, request):
        return Response({'msg': 'Bu apide post methodu çalışmamaktadır.'})


class FlashDealProductApiView(APIView):
    def get(self, request):
        try:
            flash_deals = []
            products = ApiProduct.objects.filter(is_publish=True, dropshipping="Modaymış")
            for product in products:
                if product.is_discountprice:
                    if 100 - ((product.discountprice * 100) / product.price) >= 0:
                        flash_deals.append(product)
            serializer = ProductSerializer(flash_deals, many=True)
            return Response({'data': serializer.data})
        except Slider.DoesNotExist:
            return Response({'msg': 'Ürün bulunmamaktadır.'})

    def post(self, request):
        return Response({'msg': 'Bu apide post methodu çalışmamaktadır.'})


class NewProductApiView(APIView):
    def get(self, request):
        try:
            products = ApiProduct.objects.filter(is_publish=True, subcategory__title__isnull=False, dropshipping="Modaymış").order_by(
                "-create_at")[:18]
            serializer = ProductSerializer(products, many=True)
            return Response({'data': serializer.data})
        except Slider.DoesNotExist:
            return Response({'msg': 'Ürün bulunmamaktadır.'})

    def post(self, request):
        return Response({'msg': 'Bu apide post methodu çalışmamaktadır.'})


class MostLikeroductApiView(APIView):
    def get(self, request):
        try:
            products = ApiProduct.objects.all().filter(is_publish=True, dropshipping="Modaymış",
                                                       subcategory__title__isnull=False,
                                                       reviewrating__rating__gte=4, reviewrating__rating__lte=6)[:16]

            if products.count() < 4:
                products = ApiProduct.objects.filter(is_publish=True, subcategory__title__isnull=False, dropshipping="Modaymış").order_by("?")[:16]

            serializer = ProductSerializer(products, many=True)
            return Response({'data': serializer.data})
        except Slider.DoesNotExist:
            return Response({'msg': 'Ürün bulunmamaktadır.'})

    def post(self, request):
        return Response({'msg': 'Bu apide post methodu çalışmamaktadır.'})


class MostPointProductApiView(APIView):
    def get(self, request):
        try:
            reviewrating = ReviewRating.objects.all()
            products = ApiProduct.objects.filter(is_publish=True, subcategory__title__isnull=False, dropshipping="Modaymış",
                                                 reviewrating__in=reviewrating).annotate(
                rating_count=Count('id')).order_by(
                '-rating_count')

            if products.count() < 16:
                products = ApiProduct.objects.filter(is_publish=True, subcategory__title__isnull=False,  dropshipping="Modaymış").order_by("?")[:16]
            else:
                products = products[:16]

            serializer = ProductSerializer(products, many=True)
            return Response({'data': serializer.data})
        except Slider.DoesNotExist:
            return Response({'msg': 'Ürün bulunmamaktadır.'})

    def post(self, request):
        return Response({'msg': 'Bu apide post methodu çalışmamaktadır.'})


class UstGiyimUrunleriApiView(APIView):
    def get(self, request):
        try:
            product = ApiProduct.objects.raw('SELECT * FROM product_apiproduct WHERE subcategory_id = 1 GROUP BY model_code')[1:16]
            serializer = ProductSerializer(product, many=True)
            return Response({'data': serializer.data})
        except Slider.DoesNotExist:
            return Response({'msg': 'Ürün bulunmamaktadır.'})

    def post(self, request):
        return Response({'msg': 'Bu apide post methodu çalışmamaktadır.'})


class AltGiyimUrunleriApiView(APIView):
    def get(self, request):
        try:
            product = ApiProduct.objects.raw('SELECT * FROM product_apiproduct WHERE subcategory_id = 2 GROUP BY model_code')[1:16]

            serializer = ProductSerializer(product, many=True)
            return Response({'data': serializer.data})
        except Slider.DoesNotExist:
            return Response({'msg': 'Ürün bulunmamaktadır.'})

    def post(self, request):
        return Response({'msg': 'Bu apide post methodu çalışmamaktadır.'})


class EsofmanUrunleriApiView(APIView):
    def get(self, request):
        try:
            product = ApiProduct.objects.raw('SELECT * FROM product_apiproduct WHERE subcategory_id = 3 GROUP BY model_code')[1:16]
            serializer = ProductSerializer(product, many=True)
            return Response({'data': serializer.data})
        except Slider.DoesNotExist:
            return Response({'msg': 'Ürün bulunmamaktadır.'})

    def post(self, request):
        return Response({'msg': 'Bu apide post methodu çalışmamaktadır.'})


class ElbiseUrunleriApiView(APIView):
    def get(self, request):
        try:
            product = ApiProduct.objects.raw('SELECT * FROM product_apiproduct WHERE subcategory_id = 4 GROUP BY model_code')[1:16]
            serializer = ProductSerializer(product, many=True)
            return Response({'data': serializer.data})
        except Slider.DoesNotExist:
            return Response({'msg': 'Ürün bulunmamaktadır.'})

    def post(self, request):
        return Response({'msg': 'Bu apide post methodu çalışmamaktadır.'})


class AyakkabiUrunleriApiView(APIView):
    def get(self, request):
        try:
            product = ApiProduct.objects.raw('SELECT * FROM product_apiproduct WHERE subcategory_id = 5 GROUP BY model_code')[1:16]
            serializer = ProductSerializer(product, many=True)
            return Response({'data': serializer.data})
        except Slider.DoesNotExist:
            return Response({'msg': 'Ürün bulunmamaktadır.'})

    def post(self, request):
        return Response({'msg': 'Bu apide post methodu çalışmamaktadır.'})


class AksesuarUrunleriApiView(APIView):
    def get(self, request):
        try:
            product = ApiProduct.objects.raw('SELECT * FROM product_apiproduct WHERE subcategory_id = 6 GROUP BY model_code')[1:16]
            serializer = ProductSerializer(product, many=True)
            return Response({'data': serializer.data})
        except Slider.DoesNotExist:
            return Response({'msg': 'Ürün bulunmamaktadır.'})

    def post(self, request):
        return Response({'msg': 'Bu apide post methodu çalışmamaktadır.'})


class IcGiyimUrunleriApiView(APIView):
    def get(self, request):
        try:
            product = ApiProduct.objects.raw('SELECT * FROM product_apiproduct WHERE subcategory_id = 7 GROUP BY model_code')[1:16]
            serializer = ProductSerializer(product, many=True)
            return Response({'data': serializer.data})
        except Slider.DoesNotExist:
            return Response({'msg': 'Ürün bulunmamaktadır.'})

    def post(self, request):
        return Response({'msg': 'Bu apide post methodu çalışmamaktadır.'})


class MostSellerApiView(APIView):
    def get(self, request):
        try:
            product = ApiProduct.objects.filter(is_publish=True, subcategory__title__isnull=False, dropshipping="Modaymış").order_by("-sell_count")[:16]
            serializer = ProductSerializer(product, many=True)
            return Response({'data': serializer.data})
        except Slider.DoesNotExist:
            return Response({'msg': 'Ürün bulunmamaktadır.'})

    def post(self, request):
        return Response({'msg': 'Bu apide post methodu çalışmamaktadır.'})


class FlashDealsApiView(APIView):
    def get(self, request):
        try:
            flash_deals = []
            products = ApiProduct.objects.filter(is_publish=True, subcategory__title__isnull=False, dropshipping="Modaymış")
            for product in products:
                if product.is_discountprice == True:
                    if 100 - ((product.discountprice * 100) / product.price) >= 0:
                        flash_deals.append(product)

            serializer = ProductSerializer(flash_deals, many=True)
            return Response({'data': serializer.data})
        except Slider.DoesNotExist:
            return Response({'msg': 'Ürün bulunmamaktadır.'})

    def post(self, request):
        return Response({'msg': 'Bu apide post methodu çalışmamaktadır.'})
