from ciceksepeti.models import *
from ciceksepeti.services import *
from ciceksepeti.api import *
from adminpage.models import UpdateHistory

def ciceksepetiUpdateData(stock_code, quantity, list_price, sale_price):
    data = {
        "stockCode": str(stock_code),
        "stockQuantity": int(quantity),
        "listPrice": float(list_price),
        "salesPrice": float(sale_price)
    }

    return data

def ciceksepeti_update_function(products):
    items = []
    product_data = None
    ciceksepeti = Ciceksepeti.objects.all()
    result = 'success'

    if products.count() > 0:
        for p in products:
            listprice = p.product.ciceksepeti_price
            saleprice = p.product.ciceksepeti_price
            if p.product.is_ciceksepeti_discountprice:
                saleprice = p.product.ciceksepeti_discountprice

            if p.product.quantity > 2:
                items.append(
                    ciceksepetiUpdateData(stock_code=p.product.stock_code, quantity=p.product.quantity, list_price=listprice,
                                       sale_price=saleprice)
                )
            else:
                items.append(
                    ciceksepetiUpdateData(stock_code=p.product.stock_code, quantity=0, list_price=listprice,
                                       sale_price=saleprice)
                )

            product_data = {
                "items": items
            }
        try:
            api = CiceksepetiApiClient(api_key=ciceksepeti.last().apikey,
                                       supplier_id=ciceksepeti.last().saticiid)
            service = ProductIntegrationService(api)
            response = service.update_stok_price(items=product_data)
            UpdateHistory.objects.create(history_type="Çiceksepeti Stok&Fiyat Güncelleme")
            return response
        except:
            return 'error'

def ciceksepeti_stok_fiyat_guncelle():
    product_count = CiceksepetiUrunler.objects.filter(yayin_durumu=True).count()
    i = 0
    while i / 200 <= round(product_count / 200):
        products = CiceksepetiUrunler.objects.filter(yayin_durumu=True)[i:i + 200]
        ciceksepeti_update_function(products)
        i += 200