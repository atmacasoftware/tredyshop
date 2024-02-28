from django.http import HttpResponse
from rest_framework.decorators import api_view
from rest_framework.renderers import JSONRenderer
from rest_framework.views import APIView
from rest_framework.response import Response
from apis.serializers import *
from product.models import ApiProduct
from categorymodel.models import *

class AllProductApiView(APIView):
    def get(self, request):
        try:
            product = ApiProduct.objects.all()
            serializer = ProductSerializer(product, many=True)
            return Response({'items': serializer.data})
        except ApiProduct.DoesNotExist:
            return Response({'msg': 'Ürün bulunmamaktadır.'})

    def post(self, request):
        return Response({'msg': 'Bu apide post methodu çalışmamaktadır.'})


class ProductApiView(APIView):
    def get(self, request):
        try:
            product = ApiProduct.objects.filter(is_publish=True, dropshipping="Modaymış")
            serializer = ProductSerializer(product, many=True)
            return Response({'data': serializer.data})
        except ApiProduct.DoesNotExist:
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
            products = ApiProduct.objects.filter(is_publish=True, dropshipping="Modaymış")
            for product in products:
                if product.is_discountprice:
                    if 100 - ((product.discountprice * 100) / product.price) >= 0:
                        flash_deals.append(product)
            serializer = ProductSerializer(flash_deals, many=True)
            return Response({'data': serializer.data})
        except ApiProduct.DoesNotExist:
            return Response({'msg': 'Ürün bulunmamaktadır.'})

    def post(self, request):
        return Response({'msg': 'Bu apide post methodu çalışmamaktadır.'})


class NewProductApiView(APIView):
    def get(self, request):
        try:
            products = ProductModelGroup.objects.filter(product__is_publish=True, product__subcategory__title__isnull=False, product__subbottomcategory__title__isnull=False, product__dropshipping="Modaymış").order_by(
                "-product__create_at")[:12]
            serializer = ProductModelGroupSerializer(products, many=True)
            return Response({'data': serializer.data})
        except ProductModelGroup.DoesNotExist:
            return Response({'msg': 'Ürün bulunmamaktadır.'})

    def post(self, request):
        return Response({'msg': 'Bu apide post methodu çalışmamaktadır.'})


class MostLikeroductApiView(APIView):
    def get(self, request):
        try:
            products = ProductModelGroup.objects.all().filter(product__is_publish=True, product__dropshipping="Modaymış",
                                                       product__subcategory__title__isnull=False, product__subbottomcategory__title__isnull=False,
                                                       product__reviewrating__rating__gte=4, product__reviewrating__rating__lte=6)[:12]

            if products.count() < 4:
                products = ProductModelGroup.objects.filter(product__is_publish=True, product__subcategory__title__isnull=False,  product__subbottomcategory__title__isnull=False, product__dropshipping="Modaymış").order_by("?")[:12]

            serializer = ProductModelGroupSerializer(products, many=True)
            return Response({'data': serializer.data})
        except ProductModelGroup.DoesNotExist:
            return Response({'msg': 'Ürün bulunmamaktadır.'})

    def post(self, request):
        return Response({'msg': 'Bu apide post methodu çalışmamaktadır.'})


class MostPointProductApiView(APIView):
    def get(self, request):
        try:
            reviewrating = ReviewRating.objects.all()
            products = ProductModelGroup.objects.filter(product__is_publish=True, product__subcategory__title__isnull=False, product__subbottomcategory__title__isnull=False, product__dropshipping="Modaymış",
                                                 product__reviewrating__in=reviewrating).annotate(
                product__rating_count=Count('id')).order_by(
                '-product__rating_count')

            if products.count() < 16:
                products = ProductModelGroup.objects.filter(product__is_publish=True, product__subcategory__title__isnull=False, product__subbottomcategory__title__isnull=False,  product__dropshipping="Modaymış").order_by("?")[:10]
            else:
                products = products[:16]

            serializer = ProductModelGroupSerializer(products, many=True)
            return Response({'data': serializer.data})
        except ProductModelGroup.DoesNotExist:
            return Response({'msg': 'Ürün bulunmamaktadır.'})

    def post(self, request):
        return Response({'msg': 'Bu apide post methodu çalışmamaktadır.'})


class UstGiyimUrunleriApiView(APIView):
    def get(self, request):
        try:
            product = ProductModelGroup.objects.filter(product__is_publish=True,product__subcategory_id=1, product__subbottomcategory__title__isnull=False)[:10]
            serializer = ProductModelGroupSerializer(product, many=True)
            return Response({'data': serializer.data})
        except ProductModelGroup.DoesNotExist:
            return Response({'msg': 'Ürün bulunmamaktadır.'})

    def post(self, request):
        return Response({'msg': 'Bu apide post methodu çalışmamaktadır.'})


class AltGiyimUrunleriApiView(APIView):
    def get(self, request):
        try:
            product = ProductModelGroup.objects.filter(product__is_publish=True,product__subcategory_id=2, product__subbottomcategory__title__isnull=False)[:10]
            serializer = ProductModelGroupSerializer(product, many=True)
            return Response({'data': serializer.data})
        except ProductModelGroup.DoesNotExist:
            return Response({'msg': 'Ürün bulunmamaktadır.'})

    def post(self, request):
        return Response({'msg': 'Bu apide post methodu çalışmamaktadır.'})


class EsofmanUrunleriApiView(APIView):
    def get(self, request):
        try:
            product = ProductModelGroup.objects.filter(product__is_publish=True,product__subcategory_id=3, product__subbottomcategory__title__isnull=False)[:10]
            serializer = ProductModelGroupSerializer(product, many=True)
            return Response({'data': serializer.data})
        except ProductModelGroup.DoesNotExist:
            return Response({'msg': 'Ürün bulunmamaktadır.'})

    def post(self, request):
        return Response({'msg': 'Bu apide post methodu çalışmamaktadır.'})


class ElbiseUrunleriApiView(APIView):
    def get(self, request):
        try:
            product = ProductModelGroup.objects.filter(product__is_publish=True, product__subcategory_id=4, product__subbottomcategory__title__isnull=False)[:10]
            serializer = ProductModelGroupSerializer(product, many=True)
            return Response({'data': serializer.data})
        except ProductModelGroup.DoesNotExist:
            return Response({'msg': 'Ürün bulunmamaktadır.'})

    def post(self, request):
        return Response({'msg': 'Bu apide post methodu çalışmamaktadır.'})


class AyakkabiUrunleriApiView(APIView):
    def get(self, request):
        try:
            product = ProductModelGroup.objects.filter(product__is_publish=True, product__subcategory_id=5, product__subbottomcategory__title__isnull=False)[:10]
            serializer = ProductModelGroupSerializer(product, many=True)
            return Response({'data': serializer.data})
        except ProductModelGroup.DoesNotExist:
            return Response({'msg': 'Ürün bulunmamaktadır.'})

    def post(self, request):
        return Response({'msg': 'Bu apide post methodu çalışmamaktadır.'})


class AksesuarUrunleriApiView(APIView):
    def get(self, request):
        try:
            product = ProductModelGroup.objects.filter(product__is_publish=True, product__subcategory_id=6, product__subbottomcategory__title__isnull=False)[:10]
            serializer = ProductModelGroupSerializer(product, many=True)
            return Response({'data': serializer.data})
        except ProductModelGroup.DoesNotExist:
            return Response({'msg': 'Ürün bulunmamaktadır.'})

    def post(self, request):
        return Response({'msg': 'Bu apide post methodu çalışmamaktadır.'})


class IcGiyimUrunleriApiView(APIView):
    def get(self, request):
        try:
            product = ProductModelGroup.objects.filter(product__is_publish=True, product__subcategory_id=7, product__subbottomcategory__title__isnull=False)[:10]
            serializer = ProductModelGroupSerializer(product, many=True)
            return Response({'data': serializer.data})
        except ProductModelGroup.DoesNotExist:
            return Response({'msg': 'Ürün bulunmamaktadır.'})

    def post(self, request):
        return Response({'msg': 'Bu apide post methodu çalışmamaktadır.'})


class MostSellerApiView(APIView):
    def get(self, request):
        try:
            product = ProductModelGroup.objects.filter(product__is_publish=True, product__subcategory__title__isnull=False, product__subbottomcategory__title__isnull=False, product__dropshipping="Modaymış").order_by("-product__sell_count")[:12]
            serializer = ProductModelGroupSerializer(product, many=True)
            return Response({'data': serializer.data})
        except ProductModelGroup.DoesNotExist:
            return Response({'msg': 'Ürün bulunmamaktadır.'})

    def post(self, request):
        return Response({'msg': 'Bu apide post methodu çalışmamaktadır.'})


class FlashDealsApiView(APIView):
    def get(self, request):
        try:
            flash_deals = []
            products = ProductModelGroup.objects.filter(product__is_publish=True, product__subcategory__title__isnull=False, product__subbottomcategory__title__isnull=False, product__dropshipping="Modaymış")
            for product in products:
                if product.product.is_discountprice:
                    if 100 - ((product.get_product_discountprice() * 100) / product.get_product_price()) >= 0:
                        flash_deals.append(product)

            serializer = ProductModelGroupSerializer(flash_deals, many=True)
            return Response({'data': serializer.data})
        except ProductModelGroup.DoesNotExist:
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
