import decimal
import xml.etree.ElementTree as ET
from urllib.request import urlopen, Request, FancyURLopener
from xml.dom import minidom

from unidecode import unidecode
from categorymodel.models import SubCategory, SubBottomCategory, MainCategory
from product.models import Color, Size, ApiProduct
from django.contrib import messages
from adminpage.models import *


def customPrice(starter, finish, price):
    while finish < 15000:
        if float(price) >= starter and float(price) < finish:
            price = finish - 0.10
            return decimal.Decimal(price)

        starter += 10
        finish += 10


def tredyshopPrice(urun_maliyeti, kdv):
    tredyshop = TredyShopFiyatAyarla.objects.all().last()
    kar_marjlari = TredyShopKarMarji.objects.filter(tredyshop=tredyshop)
    duzeltilmis_satis_fiyati = 0
    for kar_marji in kar_marjlari:
        if urun_maliyeti >= kar_marji.baslangic and urun_maliyeti <= kar_marji.bitis:
            maliyet = 0
            kdv_hesabi = 0
            marj = 1 + (kar_marji.kar_maji / 100)
            if kdv == "Giyim":
                kdv_hesabi = tredyshop.kdv1 / 100 * marj
            else:
                kdv_hesabi = tredyshop.kdv2 / 100 * marj
            urun = urun_maliyeti * marj
            komisyon_hesabi = tredyshop.commission / 100 * marj
            kargo_hesabi = tredyshop.kargo * marj
            satis_fiyati = kargo_hesabi + (urun * kdv_hesabi) + (urun * komisyon_hesabi) + urun
            duzeltilmis_satis_fiyati = customPrice(0, 10, satis_fiyati)
    return duzeltilmis_satis_fiyati


def trendyolPrice(urun_maliyeti, kdv, indirim=False):
    trendyol = TrendyolFiyatAyarla.objects.all().last()
    kar_marjlari = TrendyolKarMarji.objects.filter(trendyol=trendyol)
    duzeltilmis_satis_fiyati = 0

    indirim = 0
    if indirim == True:
        indirim = trendyol.indirim

    for kar_marji in kar_marjlari:
        if urun_maliyeti >= kar_marji.baslangic and urun_maliyeti <= kar_marji.bitis:
            maliyet = 0
            kdv_hesabi = 0
            marj = 1 + (kar_marji.kar_maji / 100)
            if kdv == "Giyim":
                kdv_hesabi = trendyol.kdv1 / 100 * marj
            else:
                kdv_hesabi = trendyol.kdv2 / 100 * marj
            urun = urun_maliyeti * marj
            komisyon_hesabi = trendyol.commission / 100 * marj
            hizmet_bedeli = trendyol.service * marj
            kargo_hesabi = trendyol.kargo * marj
            satis_fiyati = kargo_hesabi + (urun * kdv_hesabi) + (
                    urun * komisyon_hesabi) + urun + hizmet_bedeli - indirim
            duzeltilmis_satis_fiyati = customPrice(0, 10, satis_fiyati)
    return duzeltilmis_satis_fiyati

def ciceksepetiPrice(urun_maliyeti, kdv, indirim=False):
    ciceksepeti = CiceksepetiFiyatAyarla.objects.all().last()
    kar_marjlari = CiceksepetiKarMarji.objects.filter(ciceksepeti=ciceksepeti)
    duzeltilmis_satis_fiyati = 0

    indirim = 0
    if indirim == True:
        indirim = ciceksepeti.indirim

    for kar_marji in kar_marjlari:
        if urun_maliyeti >= kar_marji.baslangic and urun_maliyeti <= kar_marji.bitis:
            maliyet = 0
            kdv_hesabi = 0
            marj = 1 + (kar_marji.kar_maji / 100)
            if kdv == "Giyim":
                kdv_hesabi = ciceksepeti.kdv1 / 100 * marj
            else:
                kdv_hesabi = ciceksepeti.kdv2 / 100 * marj
            urun = urun_maliyeti * marj
            komisyon_hesabi = ciceksepeti.commission / 100 * marj
            hizmet_bedeli = ciceksepeti.service * marj
            kargo_hesabi = ciceksepeti.kargo * marj
            satis_fiyati = kargo_hesabi + (urun * kdv_hesabi) + (
                    urun * komisyon_hesabi) + urun + hizmet_bedeli - indirim
            duzeltilmis_satis_fiyati = customPrice(0, 10, satis_fiyati)
    return duzeltilmis_satis_fiyati

def modaymissaveXML2db():
    with urlopen('https://www.modaymis.com/1.xml') as f:
        modaymis = ET.parse(f)
        modaymis_products = modaymis.findall("Product")
        for product in modaymis_products:
            id = product.get("Id")
            modelcode = product.get("ModelCode")
            sku = product.get("Sku")
            name = product.get("Name").split("-")[0].rstrip()
            title = product.get("Name")
            manufacturer = product.get("Manufacturer")
            description = product.get("FullDescription")
            stok = product.get("StockQuantity")
            price = product.get("Price").replace(",", ".")
            tredyshop_price = None
            pttavm_price = None
            sub_category = ''
            sub_category_id = None
            bottom_category = ''
            bottom_category_id = None
            kapak = None
            beden = None
            beden_array = []
            combination_stock = None
            combination_stock_array = []
            beden_quantity = {}

            for p in product.iter("Combinations"):
                for c in p.iter("Combination"):
                    combination_stock = c.get("StockQuantity")
                    combination_sku = c.get("Sku")
                    combination_gtin = c.get("Gtin")
                    combination_stock_array.append(combination_stock)

                    if ApiProduct.objects.filter(barcode=combination_gtin).count() < 1:
                        tredyshop_price = tredyshopPrice(float(price), "Giyim")
                        trendyol_price = trendyolPrice(float(price), "Giyim")
                        ciceksepeti_price = ciceksepetiPrice(float(price), "Giyim")

                        for a in c.iter("Attributes"):
                            for ac in a.iter("Attribute"):
                                combination_attribute_name = ac.get("Name")
                                combination_attribute_value = ac.get("Value")
                                if combination_attribute_name == 'Beden':
                                    beden = combination_attribute_value
                        beden_id = None
                        for s in Size.objects.all():
                            if beden is not None:
                                if beden.replace(" ", "").replace(",", ".").lower() == s.name.replace(" ", "").replace(",",
                                                                                                               ".").lower():
                                    beden_id = s.id

                        for p in product.iter("Categories"):
                            for c in p.iter('Category'):
                                sub_category = unidecode(c.get("Path").split(">>")[0].capitalize(), 'utf-8')
                                bottom_category = unidecode(c.get("Path").split(">>")[1], 'utf-8')
                                break;
                        for sc in SubCategory.objects.all():
                            if sub_category.lower().replace(" ", "").replace("ı", "i").replace("ö", "o").replace("ü",
                                                                                                                 "u").replace(
                                "İ",
                                "I").replace(
                                "ş", "s") == sc.title.lower().replace(
                                " ", "").replace("ı", "i").replace("ö", "o").replace("ü", "u").replace("İ",
                                                                                                       "I").replace("ş",
                                                                                                                    "s"):
                                sub_category_id = sc.id
                        for p in product.iter("Specifications"):
                            for s in p.iter("Specification"):
                                if s.get("Name") == 'Kategori':
                                    bottom_category = unidecode(s.get("Value"), 'utf-8')
                                    if bottom_category == 'Pijama Takimi':
                                        bottom_category = 'Pijama'
                                    if bottom_category == 'Sortlu Takim':
                                        bottom_category = 'Eşofman Takımı'
                                    if bottom_category == 'Atlet':
                                        bottom_category = 'Atlet-Bustiyer'
                                    if bottom_category == 'Babet-Sandalet':
                                        bottom_category = 'Babet-Sandalet-Terlik'
                                    if bottom_category == 'Terlik-Panduf':
                                        bottom_category = 'Babet-Sandalet-Terlik'
                                    if bottom_category == 'Ceket-Mont':
                                        bottom_category = 'Ceket-Mont-Kaban'
                                    if bottom_category == 'Bustiyer':
                                        bottom_category = 'Atlet-Büstiyer'
                                    if bottom_category == 'Babet-Sandalet':
                                        bottom_category = 'Babet-Sandalet-Terlik'
                                if s.get("Name") == 'Renk':
                                    renk = s.get("Value")
                                if s.get("Name") == 'Beden Seçiniz':
                                    size = s.get("Value")
                        for c in Color.objects.all():
                            if renk is not None:
                                if renk.replace(" ", "").replace("İ", "I").replace("ı", "i").replace("ö", "o").replace(
                                        "ü",
                                        "u") == c.name.replace(
                                    " ", "").replace("İ", "I").replace("ı", "i").replace("ö", "o").replace("ü", "u"):
                                    renk_id = c.id

                        data = ApiProduct.objects.create(xml_id=id, category_id=1, dropshipping="Modaymış",
                                                         subcategory_id=sub_category_id,
                                                         barcode=combination_gtin, model_code=sku,
                                                         stock_code=combination_sku,
                                                         brand_id=9, title=title, description=name,
                                                         price=tredyshop_price,
                                                         trendyol_price=trendyol_price,
                                                         ciceksepeti_price=ciceksepeti_price,
                                                         quantity=combination_stock, detail=description,
                                                         status=True, color_id=renk_id, size_id=beden_id,
                                                         age_group="Yetişkin")
                        data.save()

                        for sb in SubBottomCategory.objects.all():
                            if bottom_category.lower().replace(" ", "").replace("ı", "i").replace("ö", "o").replace("ü",
                                                                                                                    "u").replace(
                                "ş", "s").replace("İ", "I") == sb.title.lower().replace(" ", "").replace("ı",
                                                                                                         "i").replace(
                                "ö",
                                "o").replace(
                                "ü", "u").replace("ş", "s").replace("İ", "I"):
                                bottom_category_id = sb.id
                        data.subbottomcategory_id = bottom_category_id
                        data.save()

                        image_list = []
                        for p in product.iter('Pictures'):
                            for i in p.iter("Picture"):
                                image_list.append(i.get("Path"))

                        if len(image_list) > 0 and len(image_list) <= 1:
                            data.image_url1 = image_list[0]

                        if len(image_list) > 1 and len(image_list) <= 2:
                            data.image_url1 = image_list[0]
                            data.image_url2 = image_list[1]

                        if len(image_list) > 2 and len(image_list) <= 3:
                            data.image_url1 = image_list[0]
                            data.image_url2 = image_list[1]
                            data.image_url3 = image_list[2]

                        if len(image_list) > 3 and len(image_list) <= 4:
                            data.image_url1 = image_list[0]
                            data.image_url2 = image_list[1]
                            data.image_url3 = image_list[2]
                            data.image_url4 = image_list[3]

                        if len(image_list) > 4 and len(image_list) <= 5:
                            data.image_url1 = image_list[0]
                            data.image_url2 = image_list[1]
                            data.image_url3 = image_list[2]
                            data.image_url4 = image_list[3]
                            data.image_url5 = image_list[4]

                        if len(image_list) > 5 and len(image_list) <= 6:
                            data.image_url1 = image_list[0]
                            data.image_url2 = image_list[1]
                            data.image_url3 = image_list[2]
                            data.image_url4 = image_list[3]
                            data.image_url5 = image_list[4]
                            data.image_url6 = image_list[5]

                        if len(image_list) > 6 and len(image_list) <= 7:
                            data.image_url1 = image_list[0]
                            data.image_url2 = image_list[1]
                            data.image_url3 = image_list[2]
                            data.image_url4 = image_list[3]
                            data.image_url5 = image_list[4]
                            data.image_url6 = image_list[5]
                            data.image_url7 = image_list[6]

                        if len(image_list) > 7:
                            data.image_url1 = image_list[0]
                            data.image_url2 = image_list[1]
                            data.image_url3 = image_list[2]
                            data.image_url4 = image_list[3]
                            data.image_url5 = image_list[4]
                            data.image_url6 = image_list[5]
                            data.image_url7 = image_list[6]
                            data.image_url8 = image_list[7]
                        data.save()
        UpdateHistory.objects.create(history_type="Modaymış Yeni Ürün Ekleme")


def updateModaymisSaveXML2db():
    with urlopen('https://www.modaymis.com/1.xml') as f:
        modaymis = ET.parse(f)
        modaymis_products = modaymis.findall("Product")
        for product in modaymis_products:
            name = product.get("Name").split("-")[0].rstrip()
            price = product.get("Price").replace(",", ".")
            description = product.get("FullDescription")
            beden = None
            combination_stock_array = []
            beden_id = None
            beden_id_array = []
            renk_id = None

            for p in product.iter("Combinations"):
                for c in p.iter("Combination"):
                    combination_stock = c.get("StockQuantity")
                    combination_gtin = c.get("Gtin")
                    combination_stock_array.append(combination_stock)

                    if ApiProduct.objects.filter(barcode=combination_gtin).count() > 0:
                        exist_product = ApiProduct.objects.get(barcode=combination_gtin)
                        exist_product.is_publish = True
                        exist_product.save()
                        tredyshop_price = None
                        trendyol_price = None

                        renk = exist_product.color.name
                        tredyshop_price = tredyshopPrice(float(price), "Giyim")
                        trendyol_price = trendyolPrice(float(price), "Giyim", True)
                        ciceksepeti_price = ciceksepetiPrice(float(price), "Giyim", True)

                        exist_product.price = tredyshop_price
                        exist_product.trendyol_price = trendyol_price
                        exist_product.ciceksepeti_price = ciceksepeti_price
                        exist_product.quantity = combination_stock
                        exist_product.detail = description
                        exist_product.brand.id = 9
                        exist_product.save()

                        for a in c.iter("Attributes"):
                            for ac in a.iter("Attribute"):
                                combination_attribute_name = ac.get("Name")
                                combination_attribute_value = ac.get("Value")
                                if combination_attribute_name == 'Beden':
                                    beden = combination_attribute_value
                        for c in Color.objects.all():
                            if renk is not None:
                                if renk.lower().replace(" ", "").replace("İ", "I").replace("ı", "i").replace("ö",
                                                                                                             "o").replace(
                                    "ü",
                                    "u") == c.name.lower().replace(
                                    " ", "").replace("İ", "I").replace("ı", "i").replace("ö", "o").replace("ü", "u"):
                                    renk_id = c.id
                        for s in Size.objects.all():
                            if beden is not None:
                                if beden.lower().replace(" ", "").replace(",", ".") == s.name.lower().replace(" ",
                                                                                                              "").replace(
                                    ",", "."):
                                    beden_id_array.append(s.id)
                                    beden_id = s.id
                        exist_product.save()
        UpdateHistory.objects.create(history_type="Modaymış Güncelleme")


def notActiveModaymisProduct():
    with urlopen('https://www.modaymis.com/1.xml') as f:
        modaymis = ET.parse(f)
        modaymis_products = modaymis.findall("Product")
        combination_gtin_list = []
        current_product_list = []
        all_products = ApiProduct.objects.filter(dropshipping="Modaymış")
        for ap in all_products:
            current_product_list.append(ap.barcode)
        for product in modaymis_products:
            for p in product.iter("Combinations"):
                for c in p.iter("Combination"):
                    combination_gtin = c.get("Gtin")
                    combination_gtin_list.append(combination_gtin)

        list_a = current_product_list
        list_b = combination_gtin_list
        difference = list(set(list_a) - set(list_b))

        for d in difference:
            for ap in all_products:
                if ap.barcode == d:
                    ap.is_publish = False
                    ap.quantity = 0
                    ap.save()
        UpdateHistory.objects.create(history_type="Modaymış Aktif Olmayan Ürün")


def xml_dunyasi_gsm():
    site = "https://www.xmldunyasi.com/export/36d3421bd4097179cd37850bbd3a683ajBkRIbLdLW84Po09w=="
    hdr = {
        'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.11 (KHTML, like Gecko) Chrome/23.0.1271.64 Safari/537.11',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
        'Accept-Charset': 'ISO-8859-1,utf-8;q=0.7,*;q=0.3',
        'Accept-Encoding': 'none',
        'Accept-Language': 'en-US,en;q=0.8',
        'Connection': 'keep-alive'}

    req = Request(site, headers=hdr)

    page = urlopen(req)
    xmldunyasi = ET.parse(page)
    for p in xmldunyasi.getroot():
        for product in p.iter('product'):
            top_category = product.find('top_category').text
            if top_category == 'Telefon Kılıfı':
                barcode = product.find('barcode').text
                if ApiProduct.objects.filter(barcode=barcode).count() < 1:
                    id = product.find('id').text
                    name = product.find('name').text
                    price = float(product.find('price').text)
                    quantity = int(product.find('quantity').text)
                    active = product.find('active').text
                    product_code = product.find('productCode').text
                    description = product.find('description').text
                    detail = product.find('detail').text
                    try:
                        image1 = product.find('image1').text
                    except:
                        image1 = None
                    try:
                        image2 = product.find('image2').text
                    except:
                        image2 = None
                    try:
                        image3 = product.find('image3').text
                    except:
                        image3 = None
                    try:
                        image4 = product.find('image4').text
                    except:
                        image4 = None
                    try:
                        image5 = product.find('image5').text
                    except:
                        image5 = None
                    try:
                        image6 = product.find('image6').text
                    except:
                        image6 = None
                    try:
                        image7 = product.find('image7').text
                    except:
                        image7 = None
                    try:
                        image8 = product.find('image8').text
                    except:
                        image8 = None
                    category = MainCategory.objects.get(category_no="4")
                    subcategory = SubCategory.objects.get(category_no="27")
                    subbottomcategory = SubBottomCategory.objects.get(category_no="5000")
                    stock_code = f"TS5000CEP{id}"
                    tredyshop_price = tredyshopPrice(price, "Diğer")
                    trendyol_price = trendyolPrice(price, "Diğer")
                    status = True
                    if active == "0":
                        status = False
                    ApiProduct.objects.create(xml_id=id, barcode=barcode, stock_code=stock_code, title=name, description=description,
                                              image_url1=image1, image_url2=image2, image_url3=image3, quantity=quantity, detail=detail,
                                              image_url4=image4, image_url5=image5, image_url6=image6, image_url7=image7, brand_id=10,
                                              image_url8=image8, is_publish=status, model_code=product_code,
                                              category=category, subcategory=subcategory, price=tredyshop_price, trendyol_price=trendyol_price,
                                              subbottomcategory=subbottomcategory, dropshipping="XML Dünyası")
            if top_category == 'Ekran Koruyucular':
                barcode = product.find('barcode').text
                if ApiProduct.objects.filter(barcode=barcode).count() < 1:
                    id = product.find('id').text
                    name = product.find('name').text
                    price = float(product.find('price').text)
                    quantity = int(product.find('quantity').text)
                    active = product.find('active').text
                    product_code = product.find('productCode').text
                    description = product.find('description').text
                    detail = product.find('detail').text
                    try:
                        image1 = product.find('image1').text
                    except:
                        image1 = None
                    try:
                        image2 = product.find('image2').text
                    except:
                        image2 = None
                    try:
                        image3 = product.find('image3').text
                    except:
                        image3 = None
                    try:
                        image4 = product.find('image4').text
                    except:
                        image4 = None
                    try:
                        image5 = product.find('image5').text
                    except:
                        image5 = None
                    try:
                        image6 = product.find('image6').text
                    except:
                        image6 = None
                    try:
                        image7 = product.find('image7').text
                    except:
                        image7 = None
                    try:
                        image8 = product.find('image8').text
                    except:
                        image8 = None
                    category = MainCategory.objects.get(category_no="4")
                    subcategory = SubCategory.objects.get(category_no="26")
                    subbottomcategory = SubBottomCategory.objects.get(category_no="5050")
                    stock_code = f"TS5000CEP{id}"
                    tredyshop_price = tredyshopPrice(price, "Diğer")
                    trendyol_price = trendyolPrice(price, "Diğer")
                    status = True
                    if active == "0":
                        status = False
                    ApiProduct.objects.create(xml_id=id, barcode=barcode, stock_code=stock_code, title=name, description=description,
                                              image_url1=image1, image_url2=image2, image_url3=image3, quantity=quantity, detail=detail,
                                              image_url4=image4, image_url5=image5, image_url6=image6, image_url7=image7, brand_id=10,
                                              image_url8=image8, is_publish=status, model_code=product_code,
                                              category=category, subcategory=subcategory, price=tredyshop_price, trendyol_price=trendyol_price,
                                              subbottomcategory=subbottomcategory, dropshipping="XML Dünyası")
            if top_category == 'Tablet Kılıfları':
                barcode = product.find('barcode').text
                if ApiProduct.objects.filter(barcode=barcode).count() < 1:
                    id = product.find('id').text
                    name = product.find('name').text
                    price = float(product.find('price').text)
                    quantity = int(product.find('quantity').text)
                    active = product.find('active').text
                    product_code = product.find('productCode').text
                    description = product.find('description').text
                    detail = product.find('detail').text
                    try:
                        image1 = product.find('image1').text
                    except:
                        image1 = None
                    try:
                        image2 = product.find('image2').text
                    except:
                        image2 = None
                    try:
                        image3 = product.find('image3').text
                    except:
                        image3 = None
                    try:
                        image4 = product.find('image4').text
                    except:
                        image4 = None
                    try:
                        image5 = product.find('image5').text
                    except:
                        image5 = None
                    try:
                        image6 = product.find('image6').text
                    except:
                        image6 = None
                    try:
                        image7 = product.find('image7').text
                    except:
                        image7 = None
                    try:
                        image8 = product.find('image8').text
                    except:
                        image8 = None
                    category = MainCategory.objects.get(category_no="4")
                    subcategory = SubCategory.objects.get(category_no="2000")
                    subbottomcategory = SubBottomCategory.objects.get(category_no="5100")
                    stock_code = f"TS6000TABLET{id}"
                    tredyshop_price = tredyshopPrice(price, "Diğer")
                    trendyol_price = trendyolPrice(price, "Diğer")
                    status = True
                    if active == "0":
                        status = False
                    ApiProduct.objects.create(xml_id=id, barcode=barcode, stock_code=stock_code, title=name, description=description,
                                              image_url1=image1, image_url2=image2, image_url3=image3, quantity=quantity, detail=detail,
                                              image_url4=image4, image_url5=image5, image_url6=image6, image_url7=image7, brand_id=10,
                                              image_url8=image8, is_publish=status, model_code=product_code,
                                              category=category, subcategory=subcategory, price=tredyshop_price, trendyol_price=trendyol_price,
                                              subbottomcategory=subbottomcategory, dropshipping="XML Dünyası")
    UpdateHistory.objects.create(history_type="XML Dünyası Yeni Ürün Ekleme")

def xml_dunyasi_gsm_update():
    site = "https://www.xmldunyasi.com/export/36d3421bd4097179cd37850bbd3a683ajBkRIbLdLW84Po09w=="
    hdr = {
        'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.11 (KHTML, like Gecko) Chrome/23.0.1271.64 Safari/537.11',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
        'Accept-Charset': 'ISO-8859-1,utf-8;q=0.7,*;q=0.3',
        'Accept-Encoding': 'none',
        'Accept-Language': 'en-US,en;q=0.8',
        'Connection': 'keep-alive'}

    req = Request(site, headers=hdr)

    page = urlopen(req)
    xmldunyasi = ET.parse(page)
    for p in xmldunyasi.getroot():
        for product in p.iter('product'):
            top_category = product.find('top_category').text
            if top_category == 'Telefon Kılıfı':
                barcode = product.find('barcode').text
                if ApiProduct.objects.filter(barcode=barcode).count() > 0:
                    urun = ApiProduct.objects.get(barcode=barcode)
                    id = product.find('id').text
                    name = product.find('name').text
                    price = float(product.find('price').text)
                    quantity = int(product.find('quantity').text)
                    if quantity > 20000:
                        quantity = 100
                    active = product.find('active').text
                    product_code = product.find('productCode').text
                    description = product.find('description').text
                    detail = product.find('detail').text
                    try:
                        image1 = product.find('image1').text
                    except:
                        image1 = None
                    try:
                        image2 = product.find('image2').text
                    except:
                        image2 = None
                    try:
                        image3 = product.find('image3').text
                    except:
                        image3 = None
                    try:
                        image4 = product.find('image4').text
                    except:
                        image4 = None
                    try:
                        image5 = product.find('image5').text
                    except:
                        image5 = None
                    try:
                        image6 = product.find('image6').text
                    except:
                        image6 = None
                    try:
                        image7 = product.find('image7').text
                    except:
                        image7 = None
                    try:
                        image8 = product.find('image8').text
                    except:
                        image8 = None

                    stock_code = f"TS5000CEP{id}"
                    tredyshop_price = tredyshopPrice(price, "Diğer")
                    trendyol_price = trendyolPrice(price, "Diğer")
                    status = True
                    if active == "0":
                        status = False
                    urun.xml_id = id
                    urun.barcode = barcode
                    urun.stock_code = stock_code
                    urun.title = name
                    urun.description = description
                    urun.detail = detail
                    urun.quantity = quantity
                    urun.image_url1 = image1
                    urun.image_url2 = image2
                    urun.image_url3 = image3
                    urun.image_url4 = image4
                    urun.image_url5 = image5
                    urun.image_url6 = image6
                    urun.image_url7 = image7
                    urun.image_url8 = image8
                    urun.is_publish = status
                    urun.model_code = product_code
                    urun.price = tredyshop_price
                    urun.trendyol_price = trendyol_price
                    urun.save()
            if top_category == 'Ekran Koruyucular':
                barcode = product.find('barcode').text
                if ApiProduct.objects.filter(barcode=barcode).count() > 0:
                    urun = ApiProduct.objects.get(barcode=barcode)
                    id = product.find('id').text
                    name = product.find('name').text
                    price = float(product.find('price').text)
                    quantity = int(product.find('quantity').text)
                    if quantity > 20000:
                        quantity = 100
                    active = product.find('active').text
                    product_code = product.find('productCode').text
                    description = product.find('description').text
                    detail = product.find('detail').text
                    try:
                        image1 = product.find('image1').text
                    except:
                        image1 = None
                    try:
                        image2 = product.find('image2').text
                    except:
                        image2 = None
                    try:
                        image3 = product.find('image3').text
                    except:
                        image3 = None
                    try:
                        image4 = product.find('image4').text
                    except:
                        image4 = None
                    try:
                        image5 = product.find('image5').text
                    except:
                        image5 = None
                    try:
                        image6 = product.find('image6').text
                    except:
                        image6 = None
                    try:
                        image7 = product.find('image7').text
                    except:
                        image7 = None
                    try:
                        image8 = product.find('image8').text
                    except:
                        image8 = None

                    stock_code = f"TS5000CEP{id}"
                    tredyshop_price = tredyshopPrice(price, "Diğer")
                    trendyol_price = trendyolPrice(price, "Diğer")
                    status = True
                    if active == "0":
                        status = False

                    urun.xml_id = id
                    urun.barcode = barcode
                    urun.stock_code = stock_code
                    urun.title = name
                    urun.description = description
                    urun.detail = detail
                    urun.quantity = quantity
                    urun.image_url1 = image1
                    urun.image_url2 = image2
                    urun.image_url3 = image3
                    urun.image_url4 = image4
                    urun.image_url5 = image5
                    urun.image_url6 = image6
                    urun.image_url7 = image7
                    urun.image_url8 = image8
                    urun.is_publish = status
                    urun.model_code = product_code
                    urun.price = tredyshop_price
                    urun.trendyol_price = trendyol_price
                    urun.save()
            if top_category == 'Tablet Kılıfları':
                barcode = product.find('barcode').text
                if ApiProduct.objects.filter(barcode=barcode).count() > 0:
                    urun = ApiProduct.objects.get(barcode=barcode)
                    id = product.find('id').text
                    name = product.find('name').text
                    price = float(product.find('price').text)
                    quantity = int(product.find('quantity').text)
                    if quantity > 20000:
                        quantity = 100
                    active = product.find('active').text
                    product_code = product.find('productCode').text
                    description = product.find('description').text
                    detail = product.find('detail').text
                    try:
                        image1 = product.find('image1').text
                    except:
                        image1 = None
                    try:
                        image2 = product.find('image2').text
                    except:
                        image2 = None
                    try:
                        image3 = product.find('image3').text
                    except:
                        image3 = None
                    try:
                        image4 = product.find('image4').text
                    except:
                        image4 = None
                    try:
                        image5 = product.find('image5').text
                    except:
                        image5 = None
                    try:
                        image6 = product.find('image6').text
                    except:
                        image6 = None
                    try:
                        image7 = product.find('image7').text
                    except:
                        image7 = None
                    try:
                        image8 = product.find('image8').text
                    except:
                        image8 = None

                    stock_code = f"TS6000TABLET{id}"
                    tredyshop_price = tredyshopPrice(price, "Diğer")
                    trendyol_price = trendyolPrice(price, "Diğer")
                    status = True
                    if active == "0":
                        status = False
                    urun.xml_id = id
                    urun.barcode = barcode
                    urun.stock_code = stock_code
                    urun.title = name
                    urun.description = description
                    urun.detail = detail
                    urun.quantity = quantity
                    urun.image_url1 = image1
                    urun.image_url2 = image2
                    urun.image_url3 = image3
                    urun.image_url4 = image4
                    urun.image_url5 = image5
                    urun.image_url6 = image6
                    urun.image_url7 = image7
                    urun.image_url8 = image8
                    urun.is_publish = status
                    urun.model_code = product_code
                    urun.price = tredyshop_price
                    urun.trendyol_price = trendyol_price
                    urun.save()
    UpdateHistory.objects.create(history_type="XML Dünyası Ürün Güncelleme")

def xml_dunyasi_gsm_not_active():
    site = "https://www.xmldunyasi.com/export/36d3421bd4097179cd37850bbd3a683ajBkRIbLdLW84Po09w=="
    hdr = {
        'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.11 (KHTML, like Gecko) Chrome/23.0.1271.64 Safari/537.11',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
        'Accept-Charset': 'ISO-8859-1,utf-8;q=0.7,*;q=0.3',
        'Accept-Encoding': 'none',
        'Accept-Language': 'en-US,en;q=0.8',
        'Connection': 'keep-alive'}

    req = Request(site, headers=hdr)

    page = urlopen(req)
    xmldunyasi = ET.parse(page)

    current_product_list = []
    combination_gtin_list = []
    all_products = ApiProduct.objects.filter(dropshipping="XML Dünyası")
    for ap in all_products:
        current_product_list.append(ap.barcode)

    for p in xmldunyasi.getroot():
        for product in p.iter('product'):
            combination_gtin_list.append(product.find('barcode').text)

    list_a = current_product_list
    list_b = combination_gtin_list
    difference = list(set(list_a) - set(list_b))

    for d in difference:
        for ap in all_products:
            if ap.barcode == d:
                ap.is_publish = False
                ap.quantity = 0
                ap.save()

    UpdateHistory.objects.create(history_type="XML Dünyası Aktif Olmayan Ürünler Bulundu")

def xml_dunyasi_diger():
    site = "https://www.xmldunyasi.com/export/354c45c32dbc0bed18387304c07fcb10vLaw1m1QXpuKERPteA=="
    hdr = {
        'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.11 (KHTML, like Gecko) Chrome/23.0.1271.64 Safari/537.11',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
        'Accept-Charset': 'ISO-8859-1,utf-8;q=0.7,*;q=0.3',
        'Accept-Encoding': 'none',
        'Accept-Language': 'en-US,en;q=0.8',
        'Connection': 'keep-alive'}

    req = Request(site, headers=hdr)
    color_list = Color.objects.all()
    page = urlopen(req)
    xmldunyasi = ET.parse(page)
    for p in xmldunyasi.getroot():
        for product in p.iter('product'):
            top_category = product.find('sub_category_').text
            if top_category == "Bijuteri Bileklik":
                barcode = product.find('barcode').text
                if ApiProduct.objects.filter(barcode=barcode).count() < 1:
                    id = product.find('id').text
                    name = product.find('name').text
                    price = float(product.find('price').text)
                    quantity = int(product.find('quantity').text)
                    active = product.find('active').text
                    product_code = product.find('productCode').text
                    description = product.find('description').text
                    detail = product.find('detail').text
                    if detail == '' or detail == None:
                        detail = name
                    sex = None
                    for data in name.lower().split(" "):
                        if data == "kadın":
                            sex = 2
                        if data == "erkek":
                            sex = 1
                    size_id = 200
                    try:
                        image1 = product.find('image1').text
                    except:
                        image1 = None
                    try:
                        image2 = product.find('image2').text
                    except:
                        image2 = None
                    try:
                        image3 = product.find('image3').text
                    except:
                        image3 = None
                    try:
                        image4 = product.find('image4').text
                    except:
                        image4 = None
                    try:
                        image5 = product.find('image5').text
                    except:
                        image5 = None
                    try:
                        image6 = product.find('image6').text
                    except:
                        image6 = None
                    try:
                        image7 = product.find('image7').text
                    except:
                        image7 = None
                    try:
                        image8 = product.find('image8').text
                    except:
                        image8 = None
                    category = MainCategory.objects.get(category_no="1")
                    subcategory = SubCategory.objects.get(category_no="6")
                    subbottomcategory = SubBottomCategory.objects.get(category_no="2001")
                    stock_code = f"TS5000AKSESUAR{id}"
                    tredyshop_price = tredyshopPrice(price, "Diğer")
                    trendyol_price = trendyolPrice(price, "Diğer")
                    status = True
                    if active == "0":
                        status = False
                    ApiProduct.objects.create(xml_id=id, barcode=barcode, stock_code=stock_code, title=name,
                                              description=description, size_id=size_id,
                                              image_url1=image1, image_url2=image2, image_url3=image3, quantity=quantity,
                                              detail=detail,
                                              image_url4=image4, image_url5=image5, image_url6=image6, image_url7=image7,
                                              brand_id=10, sextype_id=sex,
                                              image_url8=image8, is_publish=status, model_code=product_code,
                                              category=category, subcategory=subcategory, price=tredyshop_price,
                                              trendyol_price=trendyol_price,
                                              subbottomcategory=subbottomcategory, dropshipping="XML Dünyası Diğer")
            if top_category == "Bijuteri Kolye":
                barcode = product.find('barcode').text
                if ApiProduct.objects.filter(barcode=barcode).count() < 1:
                    id = product.find('id').text
                    name = product.find('name').text
                    price = float(product.find('price').text)
                    quantity = int(product.find('quantity').text)
                    active = product.find('active').text
                    product_code = product.find('productCode').text
                    description = product.find('description').text
                    detail = product.find('detail').text
                    if detail == '' or detail == None:
                        detail = name
                    sex = None
                    for data in name.lower().split(" "):
                        if data == "kadın":
                            sex = 2
                        if data == "erkek":
                            sex = 1
                    size_id = 200
                    try:
                        image1 = product.find('image1').text
                    except:
                        image1 = None
                    try:
                        image2 = product.find('image2').text
                    except:
                        image2 = None
                    try:
                        image3 = product.find('image3').text
                    except:
                        image3 = None
                    try:
                        image4 = product.find('image4').text
                    except:
                        image4 = None
                    try:
                        image5 = product.find('image5').text
                    except:
                        image5 = None
                    try:
                        image6 = product.find('image6').text
                    except:
                        image6 = None
                    try:
                        image7 = product.find('image7').text
                    except:
                        image7 = None
                    try:
                        image8 = product.find('image8').text
                    except:
                        image8 = None
                    category = MainCategory.objects.get(category_no="1")
                    subcategory = SubCategory.objects.get(category_no="6")
                    subbottomcategory = SubBottomCategory.objects.get(category_no="2000")
                    stock_code = f"TS5000AKSESUAR{id}"
                    tredyshop_price = tredyshopPrice(price, "Diğer")
                    trendyol_price = trendyolPrice(price, "Diğer")
                    status = True
                    if active == "0":
                        status = False
                    ApiProduct.objects.create(xml_id=id, barcode=barcode, stock_code=stock_code, title=name,
                                              description=description, size_id=size_id,
                                              image_url1=image1, image_url2=image2, image_url3=image3, quantity=quantity,
                                              detail=detail,
                                              image_url4=image4, image_url5=image5, image_url6=image6, image_url7=image7,
                                              brand_id=10,sextype_id=sex,
                                              image_url8=image8, is_publish=status, model_code=product_code,
                                              category=category, subcategory=subcategory, price=tredyshop_price,
                                              trendyol_price=trendyol_price,
                                              subbottomcategory=subbottomcategory, dropshipping="XML Dünyası Diğer")
            if top_category == "Erkek Küpe":
                barcode = product.find('barcode').text
                if ApiProduct.objects.filter(barcode=barcode).count() < 1:
                    id = product.find('id').text
                    name = product.find('name').text
                    price = float(product.find('price').text)
                    quantity = int(product.find('quantity').text)
                    active = product.find('active').text
                    product_code = product.find('productCode').text
                    description = product.find('description').text
                    detail = product.find('detail').text
                    if detail == '' or detail == None:
                        detail = name
                    size_id = 200
                    sex = None
                    for data in name.lower().split(" "):
                        if data == "kadın":
                            sex = 2
                        if data == "erkek":
                            sex = 1
                    try:
                        image1 = product.find('image1').text
                    except:
                        image1 = None
                    try:
                        image2 = product.find('image2').text
                    except:
                        image2 = None
                    try:
                        image3 = product.find('image3').text
                    except:
                        image3 = None
                    try:
                        image4 = product.find('image4').text
                    except:
                        image4 = None
                    try:
                        image5 = product.find('image5').text
                    except:
                        image5 = None
                    try:
                        image6 = product.find('image6').text
                    except:
                        image6 = None
                    try:
                        image7 = product.find('image7').text
                    except:
                        image7 = None
                    try:
                        image8 = product.find('image8').text
                    except:
                        image8 = None
                    category = MainCategory.objects.get(category_no="1")
                    subcategory = SubCategory.objects.get(category_no="6")
                    subbottomcategory = SubBottomCategory.objects.get(category_no="2002")
                    stock_code = f"TS5000AKSESUAR{id}"
                    tredyshop_price = tredyshopPrice(price, "Diğer")
                    trendyol_price = trendyolPrice(price, "Diğer")
                    status = True
                    if active == "0":
                        status = False
                    ApiProduct.objects.create(xml_id=id, barcode=barcode, stock_code=stock_code, title=name,
                                              description=description, size_id=size_id,
                                              image_url1=image1, image_url2=image2, image_url3=image3, quantity=quantity,
                                              detail=detail, sextype_id=sex,
                                              image_url4=image4, image_url5=image5, image_url6=image6, image_url7=image7,
                                              brand_id=10,
                                              image_url8=image8, is_publish=status, model_code=product_code,
                                              category=category, subcategory=subcategory, price=tredyshop_price,
                                              trendyol_price=trendyol_price,
                                              subbottomcategory=subbottomcategory, dropshipping="XML Dünyası Diğer")
    UpdateHistory.objects.create(history_type="XML Dünyası Diğer Ürün Ekleme")

def xml_dunyasi_diger_update():
    site = "https://www.xmldunyasi.com/export/354c45c32dbc0bed18387304c07fcb10vLaw1m1QXpuKERPteA=="
    hdr = {
        'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.11 (KHTML, like Gecko) Chrome/23.0.1271.64 Safari/537.11',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
        'Accept-Charset': 'ISO-8859-1,utf-8;q=0.7,*;q=0.3',
        'Accept-Encoding': 'none',
        'Accept-Language': 'en-US,en;q=0.8',
        'Connection': 'keep-alive'}

    req = Request(site, headers=hdr)
    color_list = Color.objects.all()
    page = urlopen(req)
    xmldunyasi = ET.parse(page)
    for p in xmldunyasi.getroot():
        for product in p.iter('product'):
            barcode = product.find('barcode').text
            if ApiProduct.objects.filter(barcode=barcode).count() > 0:
                urun = ApiProduct.objects.get(barcode=barcode)
                id = product.find('id').text
                name = product.find('name').text
                price = float(product.find('price').text)
                quantity = int(product.find('quantity').text)
                active = product.find('active').text
                product_code = product.find('productCode').text
                description = product.find('description').text
                detail = product.find('detail').text
                if detail == '' or detail == None:
                    detail = name
                try:
                    image1 = product.find('image1').text
                except:
                    image1 = None
                try:
                    image2 = product.find('image2').text
                except:
                    image2 = None
                try:
                    image3 = product.find('image3').text
                except:
                    image3 = None
                try:
                    image4 = product.find('image4').text
                except:
                    image4 = None
                try:
                    image5 = product.find('image5').text
                except:
                    image5 = None
                try:
                    image6 = product.find('image6').text
                except:
                    image6 = None
                try:
                    image7 = product.find('image7').text
                except:
                    image7 = None
                try:
                    image8 = product.find('image8').text
                except:
                    image8 = None
                tredyshop_price = tredyshopPrice(price, "Diğer")
                trendyol_price = trendyolPrice(price, "Diğer")
                status = True
                if active == "0":
                    status = False
                urun.xml_id = id
                urun.title = name
                urun.description = description
                urun.detail = detail
                urun.quantity = quantity
                urun.image_url1 = image1
                urun.image_url2 = image2
                urun.image_url3 = image3
                urun.image_url4 = image4
                urun.image_url5 = image5
                urun.image_url6 = image6
                urun.image_url7 = image7
                urun.image_url8 = image8
                urun.is_publish = status
                urun.model_code = product_code
                urun.price = tredyshop_price
                urun.trendyol_price = trendyol_price
                urun.save()
    UpdateHistory.objects.create(history_type="XML Dünyası Diğer Ürün Güncelleme")

def tahtakaleSaveXML2db():
    with urlopen('https://www.tahtakaletoptanticaret.com/export.xml') as f:
        tahtakale = ET.parse(f)
        tahtakale_products = tahtakale.findall("channel")
        counter = 0
        for product in tahtakale_products:
            for item in product.iter("item"):
                title = None
                description = None
                id = None
                barcode = None
                quantity = 0
                kapak = None
                price = 0
                hepsiburada_price = None
                trendyol_price = None
                pttavm_price = None
                model_number = None
                publish_status = True
                category1_no = None
                category1_id = None
                category2_no = None
                category2_id = None
                category3_id = None
                images = []
                existing = False
                for p in item:
                    for id in p.iter("id"):
                        id = f"TK-{id.text}"
                    if ApiProduct.objects.filter(xml_id=id).count() < 1:
                        existing = False
                        for t in p.iter("title"):
                            title = t.text
                        for d in p.iter("description"):
                            description = d.text
                        for b in p.iter("brand"):
                            brand = b.text
                        for b in p.iter("barcode"):
                            barcode = b.text
                        for i in p.iter("image_link"):
                            kapak = i.text
                        for q in p.iter("quantity"):
                            quantity = q.text
                        for p in p.iter("price"):
                            price = decimal.Decimal(p.text.replace(",", "."))

                            if price != None:
                                pttavm_price = None
                                trendyol_price = None
                                if float(price) < 50.00:
                                    tredyshop_price = decimal.Decimal(price) * decimal.Decimal(1.60)
                                    tredyshop_price = customPrice(0, 10, tredyshop_price)
                                    pttavm_price = tredyshop_price
                                    trendyol_price = tredyshop_price + decimal.Decimal(18.00)
                                    trendyol_price = customPrice(0, 10, trendyol_price)
                                if float(price) >= 50.00 and float(price) < 100.00:
                                    tredyshop_price = decimal.Decimal(price) * decimal.Decimal(1.40)
                                    pttavm_price = tredyshop_price
                                    trendyol_price = tredyshop_price + decimal.Decimal(18.00)
                                    trendyol_price = customPrice(0, 10, trendyol_price)
                                if float(price) >= 100.00 and float(price) < 150.00:
                                    tredyshop_price = decimal.Decimal(price) * decimal.Decimal(1.30)
                                    tredyshop_price = customPrice(0, 10, tredyshop_price)
                                    pttavm_price = price + decimal.Decimal(20.00)
                                    trendyol_price = price + decimal.Decimal(25.00)
                                    trendyol_price = customPrice(0, 10, trendyol_price)
                                if float(price) >= 150.00 and float(price) < 200.00:
                                    tredyshop_price = decimal.Decimal(price) * decimal.Decimal(1.25)
                                    tredyshop_price = customPrice(0, 10, tredyshop_price)
                                    pttavm_price = price + decimal.Decimal(20.00)
                                    trendyol_price = price + decimal.Decimal(25.00)
                                    trendyol_price = customPrice(0, 10, trendyol_price)
                                if float(price) >= 200.00:
                                    tredyshop_price = decimal.Decimal(price) * decimal.Decimal(1.15)
                                    tredyshop_price = customPrice(0, 10, tredyshop_price)
                                    pttavm_price = tredyshop_price + decimal.Decimal(20.00)
                                    trendyol_price = price + decimal.Decimal(25.00)
                                    trendyol_price = customPrice(0, 10, trendyol_price)
                                hepsiburada_price = tredyshop_price + decimal.Decimal(35.00)
                                hepsiburada_price = customPrice(0, 10, hepsiburada_price)
                        for pt in p.iter("product_type"):
                            product_type = pt.text
                            category1 = product_type.split(" &gt; ")[0]
                            category2 = None
                            try:
                                category2 = product_type.split(" &gt; ")[1]
                            except:
                                category2 = None
                            try:
                                category3 = product_type.split(" &gt; ")[2]
                            except:
                                category3 = None
                            if category1 == "Kozmetik &amp; Kişisel Bakım":
                                category1_no = "2"
                            if category1 == "Ev ve Yaşam":
                                category1_no = "3"
                            if category1 == "Hırdavat Malzemeleri":
                                category1_no = "6"
                            if category1 == "Evcil Hayvan Ürünleri":
                                category1_no = "7"
                            if category1 == "Hediyelik Eşya Ürünleri":
                                category1_no = "8"
                            if category1 == "Kişisel Güvenlik Ürünleri" or category1 == "Oto Aksesuar Ürünleri" or category1 == "Outdoor Ürünleri" or category1 == "Özel Ürünler" or category1 == "Tv Shop Ürünleri":
                                category1_no = "-1"
                            if category1 == "Oyuncak &amp; Kırtasiye":
                                category1_no = "11"
                            if category1 == "Parti &amp; Organizasyon":
                                category1_no = "9"
                            if category1 == "Promosyon Ürünleri":
                                category1_no = "10"
                            if category1 == "Spor ve Sağlık Ürünleri":
                                category1_no = "5"
                            if category1 == "Telefon - Tablet Aksesuar":
                                category1_no = "4"
                            if category1 == "Takı ve Aksesuar Ürünleri":
                                category1_no = "1"
                            if category2 == "Anneler İçin Hediye":
                                category2_no = "54"
                            if category2 == "Araç İçi Organizerler":
                                category2_no = "74"
                            if category2 == "Araç İçİ Telefon Ve Tablet Tutucular":
                                category2_no = "75"
                            if category2 == "Aydınlatma Ürünleri":
                                category2_no = "18"
                            if category2 == "Babalar İçin Hediyeler":
                                category2_no = "55"
                            if category2 == "Bahçe Aletleri":
                                category2_no = "49"
                            if category2 == "Banyo Ürünleri":
                                category2_no = "16"
                            if category2 == "Çocuklar İçin Hediyeler":
                                category2_no = "56"
                            if category2 == "Dekoratif Biblolar":
                                category2_no = "24"
                            if category2 == "Diğer Parti Malzemeleri":
                                category2_no = "66"
                            if category2 == "Elektronik Malzeme":
                                category2_no = "76"
                            if category2 == "Ev Aksesuarları":
                                category2_no = "19"
                            if category2 == "Ev Düzenleyici Organizerler":
                                category2_no = "21"
                            if category2 == "Ev Tekstili":
                                category2_no = "17"
                            if category2 == "Folyo Ve Parti Balonları":
                                category2_no = "65"
                            if category2 == "Giyim Ürünleri":
                                category2_no = "6"
                            if category2 == "Hırdavat Askılık":
                                category2_no = "47"
                            if category2 == "Hırdavat Askılık":
                                category2_no = "47"
                            if category2 == "İlginç Tv Shop Ürünleri":
                                category2_no = "77"
                            if category2 == "Kamp El Aletleri":
                                category2_no = "78"
                            if category2 == "Kedi Bakım Ürünleri":
                                category2_no = "51"
                            if category2 == "Köpek Bakım Ürünleri":
                                category2_no = "52"
                            if category2 == "Kırtasiye Malzemeleri":
                                category2_no = "41"
                            if category2 == "Kırtasiye Malzemeleri":
                                category2_no = "41"
                            if category2 == "Kişisel Bakım Ürünleri":
                                if category3 == "El ve Ayak Bakım Ürünleri":
                                    category2_no = "14"
                                if category3 == "Cilt Bakım Aletleri":
                                    category2_no = "30"
                                if category3 == "Cilt Masaj Aletleri":
                                    category2_no = "31"
                                if category3 == "Hacamat Malzemeleri":
                                    category2_no = "32"
                                if category3 == "Isınmatik Vücut Sobası":
                                    category2_no = "33"
                            if category2 == "Kişisel Güvenlik Ürünleri":
                                category2_no = "79"
                            if category2 == "Kolye Küpe Bijuteri":
                                category2_no = "6"
                                category3_id = 71
                            if category2 == "Kupa Bardak":
                                category2_no = "68"
                            if category2 == "Kuş, Hamster Ve Diğer Petler":
                                category2_no = "53"
                            if category2 == "Lamba ve Fener":
                                category2_no = "80"
                            if category2 == "Masaj Aletleri":
                                category2_no = "31"
                            if category2 == "Metal Dekoratif Levhalar":
                                category2_no = "23"
                            if category2 == "Mutfak Ürünleri":
                                category2_no = "15"
                            if category2 == "Orijinal Telefon Aksesuarları":
                                category2_no = "29"
                            if category2 == "Oto Elektronik":
                                category2_no = "81"
                            if category2 == "None":
                                category2_no = "81"
                            if category2 == "Oto Temizlik Ürünleri":
                                category2_no = "83"
                            if category2 == "Özel Gün Hediyeleri":
                                category2_no = "57"
                            if category2 == "Parti Gözlükleri":
                                category2_no = "57"
                            if category2 == "Parti Gözlükleri":
                                category2_no = "61"
                            if category2 == "Parti Kostümleri":
                                category2_no = "62"
                            if category2 == "Parti Organizasyon":
                                category2_no = "59"
                            if category2 == "Parti Organizasyon Ürünleri":
                                category2_no = "58"
                            if category2 == "Pilates Malzemeleri":
                                category2_no = "43"
                            if category2 == "Pratik Ev Aletleri":
                                category2_no = "20"
                            if category2 == "Pratik Mutfak Aletleri":
                                category2_no = "15"
                            if category2 == "Promosyon Fikirleri":
                                category2_no = "73"
                            if category2 == "Promosyon Fikirleri":
                                category2_no = "73"
                            if category2 == "Saat" or category2 == "Saat Bileklik Aksesuar":
                                category1_no = "1"
                                category2_no = "6"
                                category3_id = 72
                            if category2 == "Sağlık Bakım Kozmetik" or category2 == "Spor Ürünleri":
                                category2_no = "45"
                            if category2 == "Şaka Malzemeleri":
                                category2_no = "64"
                            if category2 == "Telefon Tutucular":
                                category2_no = "28"
                            if category2 == "Temizlik Aletleri":
                                category2_no = "84"
                            if category2 == "Tv Shop Oto":
                                category2_no = "77"
                            if category2 == "Yapay Çiçek":
                                category2_no = "22"
                            for mc in MainCategory.objects.all():
                                if category1_no == mc.category_no:
                                    if category1_no == "11":
                                        category1_id = 12
                                    category1_id = mc.id
                            for sc in SubCategory.objects.all():
                                if category2_no == sc.category_no:
                                    category2_id = sc.id
                            if category2_id == None:
                                category2_id = 82
                        for mn in p.iter("model_number"):
                            model_number = mn.text
                        for a in p.iter("availability"):
                            availability = a.text
                            if availability == 'in stock':
                                publish_status = True
                            else:
                                publish_status = False
                        for ai in p.iter("additional_image_link1"):
                            image1 = ai.text
                            if image1:
                                images.append(image1)
                        for ai in p.iter("additional_image_link2"):
                            image2 = ai.text
                            if image2:
                                images.append(image2)
                        for ai in p.iter("additional_image_link3"):
                            image3 = ai.text
                            if image3:
                                images.append(image3)
                        for ai in p.iter("additional_image_link4"):
                            image4 = ai.text
                            if image4:
                                images.append(image4)
                    else:
                        existing = True

                if existing == False:
                    data = ApiProduct.objects.create(price=tredyshop_price, amount=quantity, category_id=category1_id,
                                                     subcategory_id=category2_id, subbottomcategory_id=category3_id,
                                                     dropshipping="Tahtakale", xml_id=id, barcode=barcode,
                                                     stock_code=model_number, is_publish=publish_status,
                                                     trendyol_price=trendyol_price, hepsiburada_price=hepsiburada_price,
                                                     pttavm_price=pttavm_price, title=title, description=title,
                                                     detail=description, image_url=kapak, brand_id=8
                                                     )
                    slugtitle = title.lower().replace("ı", "i").replace(" ", "-").replace("ü", "u").replace("ö",
                                                                                                            "o").replace(
                        "İ", "i").replace("I", "i").replace("/", "-"
                                                                 "").replace("ş", "s").replace(".", "-").replace("ğ",
                                                                                                                 "g")
                    data.slug = str(slugtitle) + str(counter)
                    data.save()
                    counter += 1


def updateTahtakaleSaveXML2db():
    with urlopen('https://www.tahtakaletoptanticaret.com/export.xml') as f:
        tahtakale = ET.parse(f)
        tahtakale_products = tahtakale.findall("channel")
        counter = 0
        for product in tahtakale_products:
            for item in product.iter("item"):
                title = None
                description = None
                id = None
                barcode = None
                quantity = 0
                kapak = None
                price = 0
                hepsiburada_price = None
                trendyol_price = None
                pttavm_price = None
                model_number = None
                publish_status = True
                category1_no = None
                category1_id = None
                category2_no = None
                category2_id = None
                category3_id = None
                existing = False

                for p in item:
                    for id in p.iter("id"):
                        id = f"TK-{id.text}"
                    if ApiProduct.objects.filter(xml_id=id).exists():
                        try:
                            product = ApiProduct.objects.get(xml_id=id)
                            for t in p.iter("title"):
                                title = t.text
                                product.title = title
                            for d in p.iter("description"):
                                description = d.text
                                product.description = description
                            for b in p.iter("barcode"):
                                barcode = b.text
                                product.barcode = barcode
                            for i in p.iter("image_link"):
                                kapak = i.text
                                product.image_url = kapak
                            for q in p.iter("quantity"):
                                quantity = q.text
                                product.amount = quantity
                            for p in p.iter("price"):
                                price = decimal.Decimal(p.text.replace(",", "."))
                                if price != None:
                                    pttavm_price = None
                                    trendyol_price = None
                                    if float(price) < 50.00:
                                        tredyshop_price = decimal.Decimal(price) * decimal.Decimal(1.60)
                                        tredyshop_price = customPrice(0, 10, tredyshop_price)
                                        pttavm_price = tredyshop_price
                                        trendyol_price = tredyshop_price + decimal.Decimal(15.00)
                                        trendyol_price = customPrice(0, 10, trendyol_price)
                                    if float(price) >= 50.00 and float(price) < 100.00:
                                        tredyshop_price = decimal.Decimal(price) * decimal.Decimal(1.40)
                                        tredyshop_price = customPrice(0, 10, tredyshop_price)
                                        pttavm_price = tredyshop_price
                                        trendyol_price = tredyshop_price + decimal.Decimal(18.00)
                                        trendyol_price = customPrice(0, 10, trendyol_price)
                                    if float(price) >= 100.00 and float(price) < 150.00:
                                        tredyshop_price = decimal.Decimal(price) * decimal.Decimal(1.30)
                                        tredyshop_price = customPrice(0, 10, tredyshop_price)
                                        pttavm_price = tredyshop_price + decimal.Decimal(20.00)
                                        trendyol_price = tredyshop_price + decimal.Decimal(25.00)
                                    if float(price) >= 150.00 and float(price) < 200.00:
                                        tredyshop_price = decimal.Decimal(price) * decimal.Decimal(1.25)
                                        tredyshop_price = customPrice(0, 10, tredyshop_price)
                                        pttavm_price = tredyshop_price + decimal.Decimal(20.00)
                                        trendyol_price = tredyshop_price + decimal.Decimal(25.00)
                                    if float(price) >= 200.00:
                                        tredyshop_price = decimal.Decimal(price) * decimal.Decimal(1.15)
                                        tredyshop_price = customPrice(0, 10, tredyshop_price)
                                        pttavm_price = tredyshop_price + decimal.Decimal(20.00)
                                        trendyol_price = tredyshop_price + decimal.Decimal(25.00)
                                        trendyol_price = customPrice(0, 10, trendyol_price)
                                    hepsiburada_price = tredyshop_price + decimal.Decimal(35.00)
                                    hepsiburada_price = customPrice(0, 10, hepsiburada_price)
                                    product.price = tredyshop_price
                                    product.hepsiburada_price = hepsiburada_price
                                    product.trendyol_price = trendyol_price
                                    product.pttavm_price = pttavm_price
                            for pt in p.iter("product_type"):
                                product_type = pt.text
                                category1 = product_type.split(" &gt; ")[0]
                                category2 = None
                                try:
                                    category2 = product_type.split(" &gt; ")[1]
                                except:
                                    category2 = None
                                try:
                                    category3 = product_type.split(" &gt; ")[2]
                                except:
                                    category3 = None
                                if category1 == "Kozmetik &amp; Kişisel Bakım":
                                    category1_no = "2"
                                if category1 == "Ev ve Yaşam":
                                    category1_no = "3"
                                if category1 == "Hırdavat Malzemeleri":
                                    category1_no = "6"
                                if category1 == "Evcil Hayvan Ürünleri":
                                    category1_no = "7"
                                if category1 == "Hediyelik Eşya Ürünleri":
                                    category1_no = "8"
                                if category1 == "Kişisel Güvenlik Ürünleri" or category1 == "Oto Aksesuar Ürünleri" or category1 == "Outdoor Ürünleri" or category1 == "Özel Ürünler" or category1 == "Tv Shop Ürünleri":
                                    category1_no = "-1"
                                if category1 == "Oyuncak &amp; Kırtasiye":
                                    category1_no = "11"
                                if category1 == "Parti &amp; Organizasyon":
                                    category1_no = "9"
                                if category1 == "Promosyon Ürünleri":
                                    category1_no = "10"
                                if category1 == "Spor ve Sağlık Ürünleri":
                                    category1_no = "5"
                                if category1 == "Telefon - Tablet Aksesuar":
                                    category1_no = "4"
                                if category1 == "Takı ve Aksesuar Ürünleri":
                                    category1_no = "1"
                                if category2 == "Anneler İçin Hediye":
                                    category2_no = "54"
                                if category2 == "Araç İçi Organizerler":
                                    category2_no = "74"
                                if category2 == "Araç İçİ Telefon Ve Tablet Tutucular":
                                    category2_no = "75"
                                if category2 == "Aydınlatma Ürünleri":
                                    category2_no = "18"
                                if category2 == "Babalar İçin Hediyeler":
                                    category2_no = "55"
                                if category2 == "Bahçe Aletleri":
                                    category2_no = "49"
                                if category2 == "Banyo Ürünleri":
                                    category2_no = "16"
                                if category2 == "Çocuklar İçin Hediyeler":
                                    category2_no = "56"
                                if category2 == "Dekoratif Biblolar":
                                    category2_no = "24"
                                if category2 == "Diğer Parti Malzemeleri":
                                    category2_no = "66"
                                if category2 == "Elektronik Malzeme":
                                    category2_no = "76"
                                if category2 == "Ev Aksesuarları":
                                    category2_no = "19"
                                if category2 == "Ev Düzenleyici Organizerler":
                                    category2_no = "21"
                                if category2 == "Ev Tekstili":
                                    category2_no = "17"
                                if category2 == "Folyo Ve Parti Balonları":
                                    category2_no = "65"
                                if category2 == "Giyim Ürünleri":
                                    category2_no = "6"
                                if category2 == "Hırdavat Askılık":
                                    category2_no = "47"
                                if category2 == "Hırdavat Askılık":
                                    category2_no = "47"
                                if category2 == "İlginç Tv Shop Ürünleri":
                                    category2_no = "77"
                                if category2 == "Kamp El Aletleri":
                                    category2_no = "78"
                                if category2 == "Kedi Bakım Ürünleri":
                                    category2_no = "51"
                                if category2 == "Köpek Bakım Ürünleri":
                                    category2_no = "52"
                                if category2 == "Kırtasiye Malzemeleri":
                                    category2_no = "41"
                                if category2 == "Kırtasiye Malzemeleri":
                                    category2_no = "41"
                                if category2 == "Kişisel Bakım Ürünleri":
                                    if category3 == "El ve Ayak Bakım Ürünleri":
                                        category2_no = "14"
                                    if category3 == "Cilt Bakım Aletleri":
                                        category2_no = "30"
                                    if category3 == "Cilt Masaj Aletleri":
                                        category2_no = "31"
                                    if category3 == "Hacamat Malzemeleri":
                                        category2_no = "32"
                                    if category3 == "Isınmatik Vücut Sobası":
                                        category2_no = "33"
                                if category2 == "Kişisel Güvenlik Ürünleri":
                                    category2_no = "79"
                                if category2 == "Kolye Küpe Bijuteri":
                                    category2_no = "6"
                                    category3_id = 71
                                if category2 == "Kupa Bardak":
                                    category2_no = "68"
                                if category2 == "Kuş, Hamster Ve Diğer Petler":
                                    category2_no = "53"
                                if category2 == "Lamba ve Fener":
                                    category2_no = "80"
                                if category2 == "Masaj Aletleri":
                                    category2_no = "31"
                                if category2 == "Metal Dekoratif Levhalar":
                                    category2_no = "23"
                                if category2 == "Mutfak Ürünleri":
                                    category2_no = "15"
                                if category2 == "Orijinal Telefon Aksesuarları":
                                    category2_no = "29"
                                if category2 == "Oto Elektronik":
                                    category2_no = "81"
                                if category2 == "None":
                                    category2_no = "81"
                                if category2 == "Oto Temizlik Ürünleri":
                                    category2_no = "83"
                                if category2 == "Özel Gün Hediyeleri":
                                    category2_no = "57"
                                if category2 == "Parti Gözlükleri":
                                    category2_no = "57"
                                if category2 == "Parti Gözlükleri":
                                    category2_no = "61"
                                if category2 == "Parti Kostümleri":
                                    category2_no = "62"
                                if category2 == "Parti Organizasyon":
                                    category2_no = "59"
                                if category2 == "Parti Organizasyon Ürünleri":
                                    category2_no = "58"
                                if category2 == "Pilates Malzemeleri":
                                    category2_no = "43"
                                if category2 == "Pratik Ev Aletleri":
                                    category2_no = "20"
                                if category2 == "Pratik Mutfak Aletleri":
                                    category2_no = "15"
                                if category2 == "Promosyon Fikirleri":
                                    category2_no = "73"
                                if category2 == "Promosyon Fikirleri":
                                    category2_no = "73"
                                if category2 == "Saat" or category2 == "Saat Bileklik Aksesuar":
                                    category1_no = "1"
                                    category2_no = "6"
                                    category3_id = 72
                                if category2 == "Sağlık Bakım Kozmetik" or category2 == "Spor Ürünleri":
                                    category2_no = "45"
                                if category2 == "Şaka Malzemeleri":
                                    category2_no = "64"
                                if category2 == "Telefon Tutucular":
                                    category2_no = "28"
                                if category2 == "Temizlik Aletleri":
                                    category2_no = "84"
                                if category2 == "Tv Shop Oto":
                                    category2_no = "77"
                                if category2 == "Yapay Çiçek":
                                    category2_no = "22"
                                for mc in MainCategory.objects.all():
                                    if category1_no == mc.category_no:
                                        if category1_no == "11":
                                            category1_id = 12
                                        category1_id = mc.id
                                for sc in SubCategory.objects.all():
                                    if category2_no == sc.category_no:
                                        category2_id = sc.id
                                if category2_id == None:
                                    category2_id = 82
                            for mn in p.iter("model_number"):
                                model_number = mn.text
                            for a in p.iter("availability"):
                                availability = a.text
                                if availability == 'in stock':
                                    publish_status = True
                                else:
                                    publish_status = False
                            product.category_id = category1_id
                            product.subcategory_id = category2_id
                            product.subbottomcategory_id = category3_id
                            product.save()
                            for ai in p.iter("additional_image_link1"):
                                image1 = ai.text

                            for ai in p.iter("additional_image_link2"):
                                image2 = ai.text

                            for ai in p.iter("additional_image_link3"):
                                image3 = ai.text

                            for ai in p.iter("additional_image_link4"):
                                image4 = ai.text

                        except:
                            print(id, "Birden Fazla Mevcut")
