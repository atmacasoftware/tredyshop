import decimal
import xml.etree.ElementTree as ET
from urllib.request import urlopen, Request, FancyURLopener
from xml.dom import minidom
from unidecode import unidecode
from categorymodel.models import SubCategory, SubBottomCategory, MainCategory
from product.models import Color, Size, Product, ProductVariant
from django.contrib import messages
from adminpage.models import *


def getUrl(url):
    site = url
    hdr = {
        'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.11 (KHTML, like Gecko) Chrome/23.0.1271.64 Safari/537.11',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
        'Accept-Charset': 'ISO-8859-1,utf-8;q=0.7,*;q=0.3',
        'Accept-Encoding': 'none',
        'Accept-Language': 'en-US,en;q=0.8',
        'Connection': 'keep-alive'}

    req = Request(site, headers=hdr)
    return req


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
                kdv_hesabi = (tredyshop.kdv1 / 100) * urun_maliyeti
            else:
                kdv_hesabi = (tredyshop.kdv2 / 100) * urun_maliyeti
            urun = urun_maliyeti * marj
            komisyon_hesabi = (tredyshop.commission / 100) * urun_maliyeti
            baslangic_maliyeti = urun_maliyeti + kdv_hesabi + komisyon_hesabi + tredyshop.kargo
            satis_fiyati = baslangic_maliyeti * marj
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
                kdv_hesabi = (trendyol.kdv1 / 100) * urun_maliyeti
            else:
                kdv_hesabi = (trendyol.kdv2 / 100) * urun_maliyeti

            komisyon_hesabi = (trendyol.commission / 100) * urun_maliyeti
            baslangic_maliyeti = urun_maliyeti + kdv_hesabi + komisyon_hesabi + trendyol.service + trendyol.kargo
            satis_fiyati = baslangic_maliyeti * marj
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
                kdv_hesabi = (ciceksepeti.kdv1 / 100) * urun_maliyeti
            else:
                kdv_hesabi = (ciceksepeti.kdv2 / 100) * urun_maliyeti

            komisyon_hesabi = (ciceksepeti.commission / 100) * urun_maliyeti
            baslangic_maliyeti = urun_maliyeti + kdv_hesabi + komisyon_hesabi + ciceksepeti.service + ciceksepeti.kargo
            satis_fiyati = baslangic_maliyeti * marj
            duzeltilmis_satis_fiyati = customPrice(0, 10, satis_fiyati)
    return duzeltilmis_satis_fiyati


def modaymissaveXML2db():
    with urlopen('https://www.modaymis.com/1.xml') as f:
        modaymis = ET.parse(f)
        modaymis_products = modaymis.findall("Product")
        for product in modaymis_products:
            id = product.get("Id")
            if Product.objects.filter(xml_id=id).count() < 1:
                modelcode = product.get("ModelCode")
                sku = product.get("Sku")
                name = product.get("Name").split("-")[0].rstrip()
                title = product.get("Name")
                description = product.get("FullDescription")
                stok = product.get("StockQuantity")
                price = product.get("Price").replace(",", ".")
                sub_category = ''
                sub_category_id = None
                bottom_category = ''
                bottom_category_id = None
                beden = None
                beden_array = []
                combination_stock = None
                combination_stock_array = []
                tredyshop_price = tredyshopPrice(float(price), "Giyim")

                data = Product.objects.create(xml_id=id, category_id=1, dropshipping="Modaymış",
                                              subcategory_id=sub_category_id,
                                              barcode=id, model_code=sku,
                                              brand_id=9, title=title, description=name,
                                              price=tredyshop_price,
                                              quantity=stok, detail=description,
                                              is_publish=True,
                                              age_group="Yetişkin")

                for p in product.iter("Combinations"):
                    for c in p.iter("Combination"):
                        combination_stock = c.get("StockQuantity")
                        combination_sku = c.get("Sku")
                        combination_gtin = "TSHM" + str(c.get("Gtin"))
                        combination_stock_array.append(combination_stock)

                        if ProductVariant.objects.filter(barcode=combination_gtin).count() < 1:

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
                                    if beden.replace(" ", "").replace(",", ".").lower() == s.name.replace(" ",
                                                                                                          "").replace(
                                        ",",
                                        ".").lower():
                                        beden_id = s.id
                            varyant_title = title + f"{str(beden)}"
                            for p in product.iter("Categories"):
                                for c in p.iter('Category'):
                                    sub_category = unidecode(c.get("Path").split(">>")[0].capitalize(), 'utf-8')
                                    bottom_category = unidecode(c.get("Path").split(">>")[1], 'utf-8')
                                    break;
                            for sc in SubCategory.objects.all():
                                if sub_category.lower().replace(" ", "").replace("ı", "i").replace("ö", "o").replace(
                                        "ü",
                                        "u").replace(
                                    "İ",
                                    "I").replace(
                                    "ş", "s") == sc.title.lower().replace(
                                    " ", "").replace("ı", "i").replace("ö", "o").replace("ü", "u").replace("İ",
                                                                                                           "I").replace(
                                    "ş",
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
                                    if renk.replace(" ", "").replace("İ", "I").replace("ı", "i").replace("ö",
                                                                                                         "o").replace(
                                        "ü",
                                        "u") == c.name.replace(
                                        " ", "").replace("İ", "I").replace("ı", "i").replace("ö", "o").replace("ü",
                                                                                                               "u"):
                                        renk_id = c.id

                            for sb in SubBottomCategory.objects.all():
                                if bottom_category.lower().replace(" ", "").replace("ı", "i").replace("ö", "o").replace(
                                        "ü",
                                        "u").replace(
                                    "ş", "s").replace("İ", "I") == sb.title.lower().replace(" ", "").replace("ı",
                                                                                                             "i").replace(
                                    "ö",
                                    "o").replace(
                                    "ü", "u").replace("ş", "s").replace("İ", "I"):
                                    bottom_category_id = sb.id
                            data.subcategory_id = sub_category_id
                            data.subbottomcategory_id = bottom_category_id
                            data.save()

                            ProductVariant.objects.create(product=data, title=varyant_title, description=varyant_title,
                                                          color_id=renk_id, size_id=beden_id, model_code=sku,
                                                          stock_code=combination_sku, barcode=combination_gtin,
                                                          trendyol_price=trendyol_price,
                                                          ciceksepeti_price=ciceksepeti_price,
                                                          quantity=combination_stock)

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
            id = product.get("Id")
            if Product.objects.filter(barcode=id).count() > 0:
                title = product.get("Name")
                price = product.get("Price").replace(",", ".")
                combination_stock_array = []
                stok = product.get("StockQuantity")
                tredyshop_price = tredyshopPrice(float(price), "Giyim")

                get_product = Product.objects.get(barcode=id)
                get_product.price = tredyshop_price
                get_product.quantity = stok
                get_product.save()

                for p in product.iter("Combinations"):
                    for c in p.iter("Combination"):
                        combination_stock = c.get("StockQuantity")
                        combination_gtin = "TSHM" + str(c.get("Gtin"))
                        combination_stock_array.append(combination_stock)
                        if ProductVariant.objects.filter(barcode=combination_gtin).count() > 0:
                            trendyol_price = trendyolPrice(float(price), "Giyim", True)
                            ciceksepeti_price = ciceksepetiPrice(float(price), "Giyim", True)

                            exist_product = ProductVariant.objects.get(barcode=combination_gtin)
                            exist_product.is_publish = True
                            exist_product.trendyol_price = trendyol_price
                            exist_product.ciceksepeti_price = ciceksepeti_price
                            exist_product.quantity = combination_stock
                            exist_product.save()
        UpdateHistory.objects.create(history_type="Modaymış Güncelleme")


def notActiveModaymisProduct():
    with urlopen('https://www.modaymis.com/1.xml') as f:
        modaymis = ET.parse(f)
        modaymis_products = modaymis.findall("Product")
        combination_gtin_list = []
        current_product_list = []
        all_products = ProductVariant.objects.filter(product__dropshipping="Modaymış")
        for ap in all_products:
            current_product_list.append(ap.barcode)
        for product in modaymis_products:
            for p in product.iter("Combinations"):
                for c in p.iter("Combination"):
                    combination_gtin = "TSHM" + str(c.get("Gtin"))
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


def addGecelikDolabi():
    req = getUrl("https://www.gecelikdolabi.com/xmlexport/export.php?id=1267")
    page = urlopen(req)
    gecelikdolabi = ET.parse(page)
    for p in gecelikdolabi.getroot():
        barcode = str(p.find('Barkod').text)
        if Product.objects.filter(barcode=barcode).count() < 1:
            title = p.find('Baslik').text
            model_code = p.find("Barkod").text
            renk_id = None
            beden_id = None
            stok = int(p.find('Stok').text)
            xml_id = p.find("Barkod").text
            fiyat = float(p.find('Indirim').text)
            kdv = int(p.find('Kdv').text)
            detail = p.find("Aciklama").text
            tredyshop_price = tredyshopPrice(fiyat, "Giyim")
            trendyol_price = trendyolPrice(fiyat, "Giyim")
            ciceksepeti_price = ciceksepetiPrice(fiyat, "Giyim")

            try:
                resim1 = p.find("Resimler").find('Resim1').text
            except:
                resim1 = None
            try:
                resim2 = p.find("Resimler").find('Resim2').text
            except:
                resim2 = None
            try:
                resim3 = p.find("Resimler").find('Resim3').text
            except:
                resim3 = None
            try:
                resim4 = p.find("Resimler").find('Resim4').text
            except:
                resim4 = None
            try:
                resim5 = p.find("Resimler").find('Resim5').text
            except:
                resim5 = None
            try:
                resim6 = p.find("Resimler").find('Resim6').text
            except:
                resim6 = None
            try:
                resim7 = p.find("Resimler").find('Resim7').text
            except:
                resim7 = None
            try:
                resim8 = p.find("Resimler").find('Resim8').text
            except:
                resim8 = None

            data = Product.objects.create(xml_id=xml_id, title=title, barcode=barcode, model_code=model_code,
                                          dropshipping="Bella Notte", category_id=1, subcategory_id=7,
                                          subbottomcategory=None, brand_id=11, description=title, image_url1=resim1,
                                          image_url2=resim2, image_url3=resim3, image_url4=resim4, image_url5=resim5,
                                          image_url6=resim6, image_url7=resim7, image_url8=resim8, quantity=stok,
                                          age_group="Yetişkin", price=tredyshop_price, detail=detail, kdv=kdv)
            varyant = p.find("Varyantlar")
            for v in varyant:
                barkod = "TSHB" + str(v.find('VaryantBarcode').text)
                stock_kod = v.find('VaryantCode').text
                try:
                    renk = v.find('ColorName').text
                except:
                    renk = None
                beden = v.find('Value').text
                varyant_stok = int(v.find('Stok').text)
                baslik = p.find('Baslik').text + " - " + "TredyShop" + " - " + str(stock_kod)

                for s in Size.objects.all():
                    if beden is not None:
                        if beden.replace(" ", "").replace(",", ".").lower() == s.name.replace(" ", "").replace(
                                ",",
                                ".").lower():
                            beden_id = s.id
                for c in Color.objects.all():
                    if renk is not None:
                        if renk.replace(" ", "").replace("İ", "I").replace("ı", "i").replace("ö", "o").replace(
                                "ü",
                                "u") == c.name.replace(
                            " ", "").replace("İ", "I").replace("ı", "i").replace("ö", "o").replace("ü", "u"):
                            renk_id = c.id

                if ProductVariant.objects.filter(barcode=barkod).count() == 0:
                    ProductVariant.objects.create(product=data, title=baslik, description=baslik, color_id=renk_id,
                                                  size_id=beden_id, barcode=barkod, quantity=varyant_stok,
                                                  model_code=model_code, stock_code=stock_kod,
                                                  trendyol_price=trendyol_price, ciceksepeti_price=ciceksepeti_price)
    UpdateHistory.objects.create(history_type="Gecelik Dolabı Yeni Ürün Yükleme")


def updateGecelikDolabi():
    req = getUrl("https://www.gecelikdolabi.com/xmlexport/export.php?id=1267")
    page = urlopen(req)
    gecelikdolabi = ET.parse(page)
    for p in gecelikdolabi.getroot():
        barcode = str(p.find('Barkod').text)
        if Product.objects.filter(barcode=barcode).count() == 1:
            title = p.find('Baslik').text
            model_code = p.find("Barkod").text
            stok = int(p.find('Stok').text)
            fiyat = float(p.find('Indirim').text)
            kdv = int(p.find('Kdv').text)
            detail = p.find("Aciklama").text
            tredyshop_price = tredyshopPrice(fiyat, "Giyim")
            trendyol_price = trendyolPrice(fiyat, "Giyim")
            ciceksepeti_price = ciceksepetiPrice(fiyat, "Giyim")

            try:
                resim1 = p.find("Resimler").find('Resim1').text
            except:
                resim1 = None
            try:
                resim2 = p.find("Resimler").find('Resim2').text
            except:
                resim2 = None
            try:
                resim3 = p.find("Resimler").find('Resim3').text
            except:
                resim3 = None
            try:
                resim4 = p.find("Resimler").find('Resim4').text
            except:
                resim4 = None
            try:
                resim5 = p.find("Resimler").find('Resim5').text
            except:
                resim5 = None
            try:
                resim6 = p.find("Resimler").find('Resim6').text
            except:
                resim6 = None
            try:
                resim7 = p.find("Resimler").find('Resim7').text
            except:
                resim7 = None
            try:
                resim8 = p.find("Resimler").find('Resim8').text
            except:
                resim8 = None

            try:
                product = Product.objects.get(barcode=barcode)
                product.title = title
                product.description = title
                product.image_url1 = resim1
                product.image_url2 = resim2
                product.image_url3 = resim3
                product.image_url4 = resim4
                product.image_url5 = resim5
                product.image_url6 = resim6
                product.image_url7 = resim7
                product.image_url8 = resim8
                product.quantity = stok
                product.price = tredyshop_price
                product.kdv = kdv
                product.save()
                varyant = p.find("Varyantlar")

                for v in varyant:
                    barkod = "TSHB" + str(v.find('VaryantBarcode').text)
                    stock_kod = v.find('VaryantCode').text
                    varyant_stok = int(v.find('Stok').text)
                    baslik = p.find('Baslik').text + " - " + "TredyShop" + " - " + str(stock_kod)

                    try:
                        varyant = ProductVariant.objects.get(barcode=barkod)
                        varyant.title = baslik
                        varyant.description = baslik
                        varyant.model_code = model_code
                        varyant.stock_code = stock_kod
                        varyant.trendyol_price = trendyol_price
                        varyant.ciceksepeti_price = ciceksepeti_price
                        varyant.quantity = varyant_stok
                        varyant.save()

                    except Exception as e:
                        Notification.objects.create(noti_type="2", title="Güncelleme sırasında hata",
                                                    detail=f"{barcode} barkod numaralı üründe güncelleme sırasında, {e} hatası alındı.")
            except Exception as e:
                Notification.objects.create(noti_type="2", title="Güncelleme sırasında hata",
                                            detail=f"{barcode} barkod numaralı üründe güncelleme sırasında, {e} hatası alındı.")
    UpdateHistory.objects.create(history_type="Gecelik Dolabı Güncelleme")


def notActiveGecelikDolabi():
    req = getUrl("https://www.gecelikdolabi.com/xmlexport/export.php?id=1267")
    page = urlopen(req)
    gecelikdolabi = ET.parse(page)
    combination_gtin_list = []
    current_product_list = []
    all_products = ProductVariant.objects.filter(product__dropshipping="Bella Notte")
    for ap in all_products:
        current_product_list.append(ap.barcode)

    for p in gecelikdolabi.getroot():
        barcode = "TSHB" + str(p.find('Barkod').text)
        combination_gtin = barcode
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
    UpdateHistory.objects.create(history_type="Gecelik Dolabı Aktif Olmayan Ürün")


def addLeyna():
    req = getUrl("https://www.leyna.com.tr/export/1/993S4586M820")
    page = urlopen(req)
    leyna = ET.parse(page)
    for p in leyna.getroot():
        barcode = "L" + str(p.find('barcode').text)
        if barcode != "LNone":
            if Product.objects.filter(barcode=barcode).count() < 1:
                title = p.find('name').text
                model_code = p.find("productCode").text
                renk_id = None
                beden_id = None
                stok = int(p.find('quantity').text)
                xml_id = p.find("barcode").text
                fiyat = float(p.find('price').text)
                kdv = 10
                detail = p.find("detail").text
                tredyshop_price = tredyshopPrice(fiyat, "Giyim")
                trendyol_price = trendyolPrice(fiyat, "Giyim")
                ciceksepeti_price = ciceksepetiPrice(fiyat, "Giyim")
                kategori = str(p.find("category").text)
                kategori_id = None

                try:
                    resim1 = p.find('image1').text
                except:
                    resim1 = None
                try:
                    resim2 = p.find('image2').text
                except:
                    resim2 = None
                try:
                    resim3 = p.find('image3').text
                except:
                    resim3 = None
                try:
                    resim4 = p.find('image4').text
                except:
                    resim4 = None
                try:
                    resim5 = p.find('image5').text
                except:
                    resim5 = None
                try:
                    resim6 = p.find('image6').text
                except:
                    resim6 = None
                try:
                    resim7 = p.find('image7').text
                except:
                    resim7 = None
                try:
                    resim8 = p.find('image8').text
                except:
                    resim8 = None

                data = Product.objects.create(xml_id=xml_id, title=title, barcode=barcode, model_code=model_code,
                                              dropshipping="Leyna", category_id=1, subcategory_id=7,
                                              subbottomcategory=None, brand_id=11, description=title, image_url1=resim1,
                                              image_url2=resim2, image_url3=resim3, image_url4=resim4, image_url5=resim5,
                                              image_url6=resim6, image_url7=resim7, image_url8=resim8, quantity=stok,
                                              age_group="Yetişkin", price=tredyshop_price, detail=detail, kdv=kdv)
                varyant = p.find("variants")
                for v in varyant:
                    barkod = "TSHL" + str(v.find('barcode').text)
                    if barkod != "TSHLNone":
                        stock_kod = v.find('barcode').text
                        try:
                            renk = v.find('value1').text
                        except:
                            renk = None
                        beden = v.find('value2').text
                        varyant_stok = int(v.find('quantity').text)
                        baslik = title + " - " + "TredyShop"

                        for s in Size.objects.all():
                            if beden is not None:
                                if beden.replace(" ", "").replace(",", ".").lower() == s.name.replace(" ", "").replace(
                                        ",",
                                        ".").lower():
                                    beden_id = s.id
                        for c in Color.objects.all():
                            if renk is not None:
                                if renk.replace(" ", "").replace("İ", "I").replace("ı", "i").replace("ö", "o").replace(
                                        "ü",
                                        "u") == c.name.replace(
                                    " ", "").replace("İ", "I").replace("ı", "i").replace("ö", "o").replace("ü", "u"):
                                    renk_id = c.id
                        if ProductVariant.objects.filter(barcode=barkod).count() == 0:
                            ProductVariant.objects.create(product=data, title=baslik, description=baslik, color_id=renk_id,
                                                          size_id=beden_id, barcode=barkod, quantity=varyant_stok,
                                                          model_code=model_code, stock_code=stock_kod,
                                                          trendyol_price=trendyol_price, ciceksepeti_price=ciceksepeti_price)
    UpdateHistory.objects.create(history_type="Leyna Yeni Ürün Yükleme")


def updateLeyna():
    req = getUrl("https://www.leyna.com.tr/export/1/993S4586M820")
    page = urlopen(req)
    leyna = ET.parse(page)
    for p in leyna.getroot():
        barcode = "L" + str(p.find('barcode').text)
        if barcode != "LNone":
            if Product.objects.filter(barcode=barcode).count() == 1:
                title = p.find('name').text
                model_code = p.find("productCode").text
                renk_id = None
                beden_id = None
                stok = int(p.find('quantity').text)
                xml_id = p.find("barcode").text
                fiyat = float(p.find('price').text)
                kdv = 10
                detail = p.find("detail").text
                tredyshop_price = tredyshopPrice(fiyat, "Giyim")
                trendyol_price = trendyolPrice(fiyat, "Giyim")
                ciceksepeti_price = ciceksepetiPrice(fiyat, "Giyim")
                kategori = str(p.find("category").text)
                kategori_id = None

                try:
                    resim1 = p.find('image1').text
                except:
                    resim1 = None
                try:
                    resim2 = p.find('image2').text
                except:
                    resim2 = None
                try:
                    resim3 = p.find('image3').text
                except:
                    resim3 = None
                try:
                    resim4 = p.find('image4').text
                except:
                    resim4 = None
                try:
                    resim5 = p.find('image5').text
                except:
                    resim5 = None
                try:
                    resim6 = p.find('image6').text
                except:
                    resim6 = None
                try:
                    resim7 = p.find('image7').text
                except:
                    resim7 = None
                try:
                    resim8 = p.find('image8').text
                except:
                    resim8 = None

                try:
                    product = Product.objects.get(barcode=barcode)
                    product.resim1 = resim1
                    product.resim2 = resim2
                    product.resim3 = resim3
                    product.resim4 = resim4
                    product.resim5 = resim5
                    product.resim6 = resim6
                    product.resim7 = resim7
                    product.resim8 = resim8
                    product.quantity = stok
                    product.model_code = model_code
                    product.price = tredyshop_price
                    product.save()

                    varyant = p.find("variants")
                    for v in varyant:
                        barkod = "TSHL" + str(v.find('barcode').text)
                        stock_kod = v.find('barcode').text
                        varyant_stok = int(v.find('quantity').text)
                        baslik = title + " - " + "TredyShop"
                        if barkod != "TSHLNone":
                            try:
                                productvariant = ProductVariant.objects.get(barcode=barkod)
                                productvariant.quantity = varyant_stok
                                productvariant.title = baslik
                                productvariant.stock_code = stock_kod
                                productvariant.model_code = model_code
                                productvariant.trendyol_price = trendyol_price
                                productvariant.ciceksepeti_price = ciceksepeti_price
                                productvariant.save()
                            except Exception as e:
                                Notification.objects.create(noti_type="2", title="Güncelleme sırasında hata",
                                                            detail=f"{barkod} barkod numaralı üründe güncelleme sırasında, {e} hatası alındı.")
                except Exception as e:
                    Notification.objects.create(noti_type="2", title="Güncelleme sırasında hata",
                                            detail=f"{barcode} barkod numaralı üründe güncelleme sırasında, {e} hatası alındı.")
    UpdateHistory.objects.create(history_type="Leyna ürün güncelleme")

def notActiveLeyna():
    req = getUrl("https://www.leyna.com.tr/export/1/993S4586M820")
    page = urlopen(req)
    leyna = ET.parse(page)
    combination_gtin_list = []
    current_product_list = []
    all_products = ProductVariant.objects.filter(product__dropshipping="Leyna")
    for ap in all_products:
        current_product_list.append(ap.barcode)

    for p in leyna.getroot():
        barcode = "TSHL" + str(p.find('Barkod').text)
        combination_gtin = barcode
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
    UpdateHistory.objects.create(history_type="Leyna Aktif Olmayan Ürün")