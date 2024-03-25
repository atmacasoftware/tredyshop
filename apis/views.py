from django.http import HttpResponse
from rest_framework.decorators import api_view
from rest_framework.renderers import JSONRenderer
from rest_framework.views import APIView
from rest_framework.response import Response
from apis.serializers import *
from product.models import Product
from categorymodel.models import *

class AllProductApiView(APIView):
    def get(self, request):
        try:
            product = Product.objects.all()
            serializer = ProductSerializer(product, many=True)
            return Response({'items': serializer.data})
        except Product.DoesNotExist:
            return Response({'msg': 'Ürün bulunmamaktadır.'})

    def post(self, request):
        return Response({'msg': 'Bu apide post methodu çalışmamaktadır.'})


class ProductApiView(APIView):
    def get(self, request):
        try:
            product = Product.objects.filter(is_publish=True, dropshipping="Modaymış")
            serializer = ProductSerializer(product, many=True)
            return Response({'data': serializer.data})
        except Product.DoesNotExist:
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
        except SubCategory.DoesNotExist:
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
        except SubBottomCategory.DoesNotExist:
            return Response({'msg': 'Kategori bulunmamaktadır.'})

    def post(self, request):
        return Response({'msg': 'Bu apide post methodu çalışmamaktadır.'})


class FlashDealProductApiView(APIView):
    def get(self, request):
        try:
            flash_deals = []
            products = Product.objects.filter(is_publish=True, dropshipping="Modaymış")
            for product in products:
                if product.is_discountprice:
                    if 100 - ((product.discountprice * 100) / product.price) >= 0:
                        flash_deals.append(product)
            serializer = ProductSerializer(flash_deals, many=True)
            return Response({'data': serializer.data})
        except Product.DoesNotExist:
            return Response({'msg': 'Ürün bulunmamaktadır.'})

    def post(self, request):
        return Response({'msg': 'Bu apide post methodu çalışmamaktadır.'})


class NewProductApiView(APIView):
    def get(self, request):
        try:
            products = Product.objects.filter(is_publish=True, subcategory__title__isnull=False, subbottomcategory__title__isnull=False).order_by(
                "-create_at")[:12]
            serializer = ProductSerializer(products, many=True)
            return Response({'data': serializer.data})
        except Product.DoesNotExist:
            return Response({'msg': 'Ürün bulunmamaktadır.'})

    def post(self, request):
        return Response({'msg': 'Bu apide post methodu çalışmamaktadır.'})


class MostLikeroductApiView(APIView):
    def get(self, request):
        try:
            products = Product.objects.all().filter(is_publish=True, subcategory__title__isnull=False, subbottomcategory__title__isnull=False,
                                                      reviewrating__rating__gte=4,reviewrating__rating__lte=6)[:12]

            if products.count() < 4:
                products = Product.objects.filter(is_publish=True, subcategory__title__isnull=False,  subbottomcategory__title__isnull=False).order_by("?")[:12]

            serializer = ProductSerializer(products, many=True)
            return Response({'data': serializer.data})
        except Product.DoesNotExist:
            return Response({'msg': 'Ürün bulunmamaktadır.'})

    def post(self, request):
        return Response({'msg': 'Bu apide post methodu çalışmamaktadır.'})


class MostPointProductApiView(APIView):
    def get(self, request):
        try:
            reviewrating = ReviewRating.objects.all()
            products = Product.objects.filter(is_publish=True, subcategory__title__isnull=False, subbottomcategory__title__isnull=False,
                                                 reviewrating__in=reviewrating).annotate(
                rating_count=Count('id')).order_by(
                '-product__rating_count')

            if products.count() < 16:
                products = Product.objects.filter(is_publish=True, subcategory__title__isnull=False, subbottomcategory__title__isnull=False).order_by("?")[:10]
            else:
                products = products[:16]

            serializer = ProductSerializer(products, many=True)
            return Response({'data': serializer.data})
        except Product.DoesNotExist:
            return Response({'msg': 'Ürün bulunmamaktadır.'})

    def post(self, request):
        return Response({'msg': 'Bu apide post methodu çalışmamaktadır.'})


class UstGiyimUrunleriApiView(APIView):
    def get(self, request):
        try:
            product = Product.objects.filter(is_publish=True, subcategory_id=1, subbottomcategory__title__isnull=False)[:10]
            serializer = ProductSerializer(product, many=True)
            return Response({'data': serializer.data})
        except Product.DoesNotExist:
            return Response({'msg': 'Ürün bulunmamaktadır.'})

    def post(self, request):
        return Response({'msg': 'Bu apide post methodu çalışmamaktadır.'})


class AltGiyimUrunleriApiView(APIView):
    def get(self, request):
        try:
            product = Product.objects.filter(is_publish=True, subcategory_id=2, subbottomcategory__title__isnull=False)[:10]
            serializer = ProductSerializer(product, many=True)
            return Response({'data': serializer.data})
        except Product.DoesNotExist:
            return Response({'msg': 'Ürün bulunmamaktadır.'})

    def post(self, request):
        return Response({'msg': 'Bu apide post methodu çalışmamaktadır.'})


class EsofmanUrunleriApiView(APIView):
    def get(self, request):
        try:
            product = Product.objects.filter(is_publish=True, subcategory_id=3, subbottomcategory__title__isnull=False)[:10]
            serializer = ProductSerializer(product, many=True)
            return Response({'data': serializer.data})
        except Product.DoesNotExist:
            return Response({'msg': 'Ürün bulunmamaktadır.'})

    def post(self, request):
        return Response({'msg': 'Bu apide post methodu çalışmamaktadır.'})


class ElbiseUrunleriApiView(APIView):
    def get(self, request):
        try:
            product = Product.objects.filter(is_publish=True, subcategory_id=4, subbottomcategory__title__isnull=False)[:10]
            serializer = ProductSerializer(product, many=True)
            return Response({'data': serializer.data})
        except Product.DoesNotExist:
            return Response({'msg': 'Ürün bulunmamaktadır.'})

    def post(self, request):
        return Response({'msg': 'Bu apide post methodu çalışmamaktadır.'})


class AyakkabiUrunleriApiView(APIView):
    def get(self, request):
        try:
            product = Product.objects.filter(is_publish=True, subcategory_id=5, subbottomcategory__title__isnull=False)[:10]
            serializer = ProductSerializer(product, many=True)
            return Response({'data': serializer.data})
        except Product.DoesNotExist:
            return Response({'msg': 'Ürün bulunmamaktadır.'})

    def post(self, request):
        return Response({'msg': 'Bu apide post methodu çalışmamaktadır.'})


class AksesuarUrunleriApiView(APIView):
    def get(self, request):
        try:
            product = Product.objects.filter(is_publish=True, subcategory_id=6, subbottomcategory__title__isnull=False)[:10]
            serializer = ProductSerializer(product, many=True)
            return Response({'data': serializer.data})
        except Product.DoesNotExist:
            return Response({'msg': 'Ürün bulunmamaktadır.'})

    def post(self, request):
        return Response({'msg': 'Bu apide post methodu çalışmamaktadır.'})


class IcGiyimUrunleriApiView(APIView):
    def get(self, request):
        try:
            product = Product.objects.filter(is_publish=True, subcategory_id=7, subbottomcategory__title__isnull=False)[:10]
            serializer = ProductSerializer(product, many=True)
            return Response({'data': serializer.data})
        except Product.DoesNotExist:
            return Response({'msg': 'Ürün bulunmamaktadır.'})

    def post(self, request):
        return Response({'msg': 'Bu apide post methodu çalışmamaktadır.'})


class MostSellerApiView(APIView):
    def get(self, request):
        try:
            product = Product.objects.filter(is_publish=True, subcategory__title__isnull=False, subbottomcategory__title__isnull=False).order_by("-sell_count")[:12]
            serializer = ProductSerializer(product, many=True)
            return Response({'data': serializer.data})
        except Product.DoesNotExist:
            return Response({'msg': 'Ürün bulunmamaktadır.'})

    def post(self, request):
        return Response({'msg': 'Bu apide post methodu çalışmamaktadır.'})


class FlashDealsApiView(APIView):
    def get(self, request):
        try:
            flash_deals = []
            products = Product.objects.filter(is_publish=True, subcategory__title__isnull=False, subbottomcategory__title__isnull=False)
            for product in products:
                if product.is_discountprice:
                    if 100 - ((product.discountprice * 100) / product.price) >= 0:
                        flash_deals.append(product)

            serializer = ProductSerializer(flash_deals, many=True)
            return Response({'data': serializer.data})
        except Product.DoesNotExist:
            return Response({'msg': 'Ürün bulunmamaktadır.'})

    def post(self, request):
        return Response({'msg': 'Bu apide post methodu çalışmamaktadır.'})


class FrontendHeaderCategoryApiView(APIView):
    def get(self, request):
        try:
            category = FrontentHeaderCategory.objects.filter(is_publish=True).order_by('order')
            serializer = FrontendHeaderCategorySerializer(category, many=True)
            return Response({'items': serializer.data})
        except FrontentHeaderCategory.DoesNotExist:
            return Response({'msg': 'Ürün bulunmamaktadır.'})

    def post(self, request):
        return Response({'msg': 'Bu apide post methodu çalışmamaktadır.'})

class BannerApiView(APIView):
    def get(self, request):
        try:
            banner = Banner.objects.filter(is_publish=True).order_by('order')
            serializer = BannerSerializer(banner, many=True)
            return Response({'items': serializer.data})
        except Banner.DoesNotExist:
            return Response({'msg': 'Ürün bulunmamaktadır.'})

    def post(self, request):
        return Response({'msg': 'Bu apide post methodu çalışmamaktadır.'})
