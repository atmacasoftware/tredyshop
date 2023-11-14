import decimal
import xml.etree.ElementTree as ET
from urllib.request import urlopen
from unidecode import unidecode
from categorymodel.models import SubCategory, SubBottomCategory, MainCategory
from product.models import Color, Size, ApiProduct, UpdateHistory
from django.contrib import messages



def customPrice(starter, finish, price):
    while finish < 10000:
        if float(price) >= starter and float(price) < finish:
            price = finish - 0.10
            return decimal.Decimal(price)

        starter += 10
        finish += 10


def modaymissaveXML2db():
    with urlopen('https://www.modaymis.com/1.xml') as f:
        modaymis = ET.parse(f)
        modaymis_products = modaymis.findall("Product")
        for product in modaymis_products:
            id = product.get("Id")
            modelcode = product.get("ModelCode")
            sku = product.get("Sku")
            name = product.get("Name").split("-")[0].rstrip()
            keywords = name.split(" ")
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
                        if float(price) < 50.00:
                            tredyshop_price = decimal.Decimal(price) + decimal.Decimal(90)
                            tredyshop_price = customPrice(0, 10, tredyshop_price)
                            pttavm_price = tredyshop_price
                            trendyol_price = tredyshop_price + decimal.Decimal(20)
                            trendyol_price = customPrice(0, 10, trendyol_price)
                        if float(price) >= 50.00 and float(price) < 100.00:
                            tredyshop_price = decimal.Decimal(price) + decimal.Decimal(115)
                            tredyshop_price = customPrice(0, 10, tredyshop_price)
                            pttavm_price = tredyshop_price
                            trendyol_price = tredyshop_price + decimal.Decimal(20)
                            trendyol_price = customPrice(0, 10, trendyol_price)
                        if float(price) >= 100.00 and float(price) < 150.00:
                            tredyshop_price = decimal.Decimal(price) + decimal.Decimal(130)
                            tredyshop_price = customPrice(0, 10, tredyshop_price)
                            pttavm_price = tredyshop_price
                            trendyol_price = tredyshop_price + decimal.Decimal(20)
                            trendyol_price = customPrice(0, 10, trendyol_price)
                        if float(price) >= 150.00 and float(price) < 200.00:
                            tredyshop_price = decimal.Decimal(price) + decimal.Decimal(120)
                            tredyshop_price = customPrice(0, 10, tredyshop_price)
                            pttavm_price = tredyshop_price
                            trendyol_price = tredyshop_price + decimal.Decimal(45) + decimal.Decimal(20)
                            trendyol_price = customPrice(0, 10, trendyol_price)
                        if float(price) >= 200.00 and float(price) < 300.00:
                            tredyshop_price = decimal.Decimal(price) + decimal.Decimal(140)
                            tredyshop_price = customPrice(0, 10, tredyshop_price)
                            pttavm_price = tredyshop_price + decimal.Decimal(20.00)
                            trendyol_price = tredyshop_price + decimal.Decimal(75) + decimal.Decimal(20)
                            trendyol_price = customPrice(0, 10, trendyol_price)
                        if float(price) >= 300.00 and float(price) < 400.00:
                            tredyshop_price = decimal.Decimal(price) + decimal.Decimal(145)
                            tredyshop_price = customPrice(0, 10, tredyshop_price)
                            pttavm_price = tredyshop_price + decimal.Decimal(20.00)
                            trendyol_price = tredyshop_price + decimal.Decimal(95) + + decimal.Decimal(20)
                            trendyol_price = customPrice(0, 10, trendyol_price)
                        if float(price) >= 400.00 and float(price) < 500.00:
                            tredyshop_price = decimal.Decimal(price) + decimal.Decimal(140)
                            tredyshop_price = customPrice(0, 10, tredyshop_price)
                            pttavm_price = tredyshop_price + decimal.Decimal(20.00)
                            trendyol_price = tredyshop_price + decimal.Decimal(130) + decimal.Decimal(20)
                            trendyol_price = customPrice(0, 10, trendyol_price)
                        if float(price) >= 500.00 and float(price) < 600.00:
                            tredyshop_price = decimal.Decimal(price) + decimal.Decimal(150)
                            tredyshop_price = customPrice(0, 10, tredyshop_price)
                            pttavm_price = tredyshop_price + decimal.Decimal(20.00)
                            trendyol_price = tredyshop_price + decimal.Decimal(175) + decimal.Decimal(20)
                            trendyol_price = customPrice(0, 10, trendyol_price)
                        if float(price) >= 600.00 and float(price) < 700.00:
                            tredyshop_price = decimal.Decimal(price) + decimal.Decimal(170)
                            tredyshop_price = customPrice(0, 10, tredyshop_price)
                            pttavm_price = tredyshop_price + decimal.Decimal(20.00)
                            trendyol_price = tredyshop_price + decimal.Decimal(195) + decimal.Decimal(20)
                            trendyol_price = customPrice(0, 10, trendyol_price)
                        if float(price) >= 700.00:
                            tredyshop_price = decimal.Decimal(price) + decimal.Decimal(190)
                            tredyshop_price = customPrice(0, 10, tredyshop_price)
                            pttavm_price = tredyshop_price + decimal.Decimal(20.00)
                            trendyol_price = tredyshop_price + decimal.Decimal(260) + decimal.Decimal(20)
                            trendyol_price = customPrice(0, 10, trendyol_price)

                        hepsiburada_price = tredyshop_price + decimal.Decimal(25.00)
                        hepsiburada_price = customPrice(0, 10, hepsiburada_price)

                        for a in c.iter("Attributes"):
                            for ac in a.iter("Attribute"):
                                combination_attribute_name = ac.get("Name")
                                combination_attribute_value = ac.get("Value")
                                if combination_attribute_name == 'Beden':
                                    beden = combination_attribute_value
                        beden_id = None
                        for s in Size.objects.all():
                            if beden is not None:
                                if beden.replace(" ", "").replace(",", ".") == s.name.replace(" ", "").replace(",",
                                                                                                               "."):
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

                        data = ApiProduct.objects.create(xml_id=id, category_id=1, dropshipping="Modaymış" ,subcategory_id=sub_category_id,
                                                         barcode=combination_gtin, model_code=sku,
                                                         stock_code=combination_sku,
                                                         brand_id=9, title=name, description=name,
                                                         price=tredyshop_price,
                                                         trendyol_price=trendyol_price,
                                                         hepsiburada_price=hepsiburada_price, pttavm_price=pttavm_price,
                                                         quantity=combination_stock, detail=description,
                                                         status=True, color_id=renk_id, size_id=beden_id, age_group="Yetişkin")
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

                        if len(image_list) > 6 and len(image_list) <=7:
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
                        pttavm_price = None
                        trendyol_price = None

                        renk = exist_product.color.name

                        if float(price) < 50.00:
                            tredyshop_price = decimal.Decimal(price) + decimal.Decimal(90)
                            tredyshop_price = customPrice(0, 10, tredyshop_price)
                            pttavm_price = tredyshop_price
                            trendyol_price = tredyshop_price + decimal.Decimal(20)
                        if float(price) >= 50.00 and float(price) < 100.00:
                            tredyshop_price = decimal.Decimal(price) + decimal.Decimal(115)
                            tredyshop_price = customPrice(0, 10, tredyshop_price)
                            pttavm_price = tredyshop_price
                            trendyol_price = tredyshop_price + decimal.Decimal(20)
                        if float(price) >= 100.00 and float(price) < 150.00:
                            tredyshop_price = decimal.Decimal(price) + decimal.Decimal(130)
                            tredyshop_price = customPrice(0, 10, tredyshop_price)
                            pttavm_price = tredyshop_price
                            trendyol_price = tredyshop_price + decimal.Decimal(20)
                        if float(price) >= 150.00 and float(price) < 200.00:
                            tredyshop_price = decimal.Decimal(price) + decimal.Decimal(120)
                            tredyshop_price = customPrice(0, 10, tredyshop_price)
                            pttavm_price = tredyshop_price
                            trendyol_price = tredyshop_price + decimal.Decimal(45) + decimal.Decimal(20)
                            trendyol_price = customPrice(0, 10, trendyol_price)
                        if float(price) >= 200.00 and float(price) < 300.00:
                            tredyshop_price = decimal.Decimal(price) + decimal.Decimal(140)
                            tredyshop_price = customPrice(0, 10, tredyshop_price)
                            pttavm_price = tredyshop_price + decimal.Decimal(20.00)
                            trendyol_price = tredyshop_price + decimal.Decimal(75) + decimal.Decimal(20)
                            trendyol_price = customPrice(0, 10, trendyol_price)
                        if float(price) >= 300.00 and float(price) < 400.00:
                            tredyshop_price = decimal.Decimal(price) + decimal.Decimal(145)
                            tredyshop_price = customPrice(0, 10, tredyshop_price)
                            pttavm_price = tredyshop_price + decimal.Decimal(20.00)
                            trendyol_price = tredyshop_price + decimal.Decimal(95) + decimal.Decimal(20)
                            trendyol_price = customPrice(0, 10, trendyol_price)
                        if float(price) >= 400.00 and float(price) < 500.00:
                            tredyshop_price = decimal.Decimal(price) + decimal.Decimal(140)
                            tredyshop_price = customPrice(0, 10, tredyshop_price)
                            pttavm_price = tredyshop_price + decimal.Decimal(20.00)
                            trendyol_price = tredyshop_price + decimal.Decimal(130) + decimal.Decimal(20)
                            trendyol_price = customPrice(0, 10, trendyol_price)
                        if float(price) >= 500.00 and float(price) < 600.00:
                            tredyshop_price = decimal.Decimal(price) + decimal.Decimal(150)
                            tredyshop_price = customPrice(0, 10, tredyshop_price)
                            pttavm_price = tredyshop_price + decimal.Decimal(20.00)
                            trendyol_price = tredyshop_price + decimal.Decimal(175) + decimal.Decimal(20)
                            trendyol_price = customPrice(0, 10, trendyol_price)
                        if float(price) >= 600.00 and float(price) < 700.00:
                            tredyshop_price = decimal.Decimal(price) + decimal.Decimal(170)
                            tredyshop_price = customPrice(0, 10, tredyshop_price)
                            pttavm_price = tredyshop_price + decimal.Decimal(20.00)
                            trendyol_price = tredyshop_price + decimal.Decimal(195) + decimal.Decimal(20)
                            trendyol_price = customPrice(0, 10, trendyol_price)
                        if float(price) >= 700.00:
                            tredyshop_price = decimal.Decimal(price) + decimal.Decimal(190)
                            tredyshop_price = customPrice(0, 10, tredyshop_price)
                            pttavm_price = tredyshop_price + decimal.Decimal(20.00)
                            trendyol_price = tredyshop_price + decimal.Decimal(260) + decimal.Decimal(20)
                            trendyol_price = customPrice(0, 10, trendyol_price)

                        hepsiburada_price = tredyshop_price + decimal.Decimal(35.00)
                        hepsiburada_price = customPrice(0, 10, hepsiburada_price)
                        exist_product.price = tredyshop_price
                        exist_product.trendyol_price = trendyol_price
                        exist_product.hepsiburada_price = hepsiburada_price
                        exist_product.pttavm_price = pttavm_price
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
                        exist_product.size_id = beden_id
                        exist_product.color_id = renk_id
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