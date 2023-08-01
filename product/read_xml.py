import decimal
import html.parser
import os
import xml.etree.ElementTree as ET
from urllib.request import urlopen
from unidecode import unidecode
from categorymodel.models import SubCategory, SubBottomCategory
from ecommerce.settings import BASE_DIR
from product.models import Product, ProductKeywords, Images, Color, Size, Variants
from decimal import Decimal


def modaymissaveXML2db():
    with urlopen('https://www.modaymis.com/1.xml') as f:
        file_path = os.path.join(BASE_DIR, 'modaymis.xml')
        modaymis = ET.parse(f)
        modaymis_products = modaymis.findall("Product")
        for product in modaymis_products:
            id = product.get("Id")
            modelcode = product.get("ModelCode")
            sku = product.get("Sku")
            name = product.get("Name").split("-")[0]
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

            if Product.objects.filter(stock_code=sku).count() < 1:
                if float(price) < 50.00:
                    tredyshop_price = decimal.Decimal(price) * decimal.Decimal(1.60)
                    pttavm_price = tredyshop_price
                if float(price) >= 50.00 and float(price) < 100.00:
                    tredyshop_price = decimal.Decimal(price) * decimal.Decimal(1.40)
                    pttavm_price = tredyshop_price
                if float(price) >= 100.00 and float(price) < 150.00:
                    tredyshop_price = decimal.Decimal(price) * decimal.Decimal(1.30)
                    pttavm_price = tredyshop_price + decimal.Decimal(20.00)
                if float(price) >= 150.00 and float(price) < 200.00:
                    tredyshop_price = decimal.Decimal(price) * decimal.Decimal(1.25)
                    pttavm_price = tredyshop_price + decimal.Decimal(20.00)
                if float(price) >= 200.00:
                    tredyshop_price = decimal.Decimal(price) * decimal.Decimal(1.15)
                    pttavm_price = tredyshop_price + decimal.Decimal(20.00)

                trendyol_price = tredyshop_price + decimal.Decimal(25.00)
                hepsiburada_price = tredyshop_price + decimal.Decimal(25.00)

                if manufacturer == 'Diğer':
                    manufacturer = 8

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
                        " ", "").replace("ı", "i").replace("ö", "o").replace("ü", "u").replace("İ", "I").replace("ş",
                                                                                                                 "s"):
                        sub_category_id = sc.id
                data = Product.objects.create(xml_id=id, category_id=1, subcategory_id=sub_category_id, stock_code=sku,
                                              barcode=modelcode, title=name,
                                              description=name,
                                              brand_id=manufacturer, price=tredyshop_price,
                                              trendyol_price=tredyshop_price,
                                              hepsiburada_price=hepsiburada_price, pttavm_price=pttavm_price,
                                              amount=stok,
                                              dropshipping="Modaymış",
                                              detail=description,
                                              status=True)
                data.save()
                if Product.objects.filter(stock_code=sku).count() > 1:
                    Product.objects.all().filter(stock_code=sku).delete()
                    data = Product.objects.create(xml_id=id, category_id=1, subcategory_id=sub_category_id,
                                                  stock_code=sku,
                                                  description=name,
                                                  barcode=modelcode, title=name,
                                                  brand_id=manufacturer, price=tredyshop_price, amount=stok,
                                                  detail=description,
                                                  dropshipping="Modaymış",
                                                  status=True)
                    data.save()
                for k in keywords:
                    product_keyword = ProductKeywords.objects.create(product=data, keyword=k)
                    product_keyword.save()
                for p in product.iter('Pictures'):
                    for i in p.iter("Picture"):
                        image = i.get("Path")
                        kapak = image
                        break;
                    for i in p.iter("Picture"):
                        images = i.get("Path")
                        image_data = Images.objects.create(product=data, image_url=images, title=name)
                        image_data.save()
                data.image_url = kapak
                data.save()
                size = None
                size_array = []
                beden_id = None
                renk_id = None
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
                            size_array.append(size)
                for c in Color.objects.all():
                    if renk is not None:
                        if renk.replace(" ", "").replace("İ", "I").replace("ı", "i").replace("ö", "o").replace("ü",
                                                                                                               "u") == c.name.replace(
                            " ", "").replace("İ", "I").replace("ı", "i").replace("ö", "o").replace("ü", "u"):
                            renk_id = c.id
                for p in product.iter("Combinations"):
                    for c in p.iter("Combination"):
                        combination_stock = c.get("StockQuantity")
                        combination_sku = c.get("Sku")
                        combination_gtin = c.get("Gtin")
                        combination_stock_array.append(combination_stock)
                        for a in c.iter("Attributes"):
                            for ac in a.iter("Attribute"):
                                combination_attribute_name = ac.get("Name")
                                combination_attribute_value = ac.get("Value")
                                if combination_attribute_name == 'Beden':
                                    beden = combination_attribute_value
                        for s in Size.objects.all():
                            if beden is not None:
                                if beden.replace(" ", "").replace(",", ".") == s.name.replace(" ", "").replace(",",
                                                                                                               "."):
                                    beden_id = s.id
                                    variants = Variants.objects.create(product=data, title=name, size_id=beden_id,
                                                                       color_id=renk_id,
                                                                       sku=combination_sku,
                                                                       gtin=combination_gtin,
                                                                       quantity=combination_stock, price=price,
                                                                       trendyol_price=trendyol_price,
                                                                       hepsiburada_price=hepsiburada_price,
                                                                       pttavm_price=pttavm_price,
                                                                       is_publish=True)
                                    variants.save()
                for sb in SubBottomCategory.objects.all():
                    if bottom_category.lower().replace(" ", "").replace("ı", "i").replace("ö", "o").replace("ü",
                                                                                                            "u").replace(
                        "ş", "s").replace("İ", "I") == sb.title.lower().replace(" ", "").replace("ı", "i").replace("ö",
                                                                                                                   "o").replace(
                        "ü", "u").replace("ş", "s").replace("İ", "I"):
                        bottom_category_id = sb.id

                if beden is not None and renk is None:
                    data.variant = 'Boyut'
                elif beden is None and renk is not None:
                    data.variant = 'Renk'
                elif beden is not None and renk is not None:
                    data.variant = 'Renk-Boyut'
                else:
                    data.variant = 'Yok'
                data.subbottomcategory_id = bottom_category_id
                data.save()


def updateModaymisSaveXML2db():
    with urlopen('https://www.modaymis.com/1.xml') as f:
        file_path = os.path.join(BASE_DIR, 'modaymis.xml')
        modaymis = ET.parse(f)
        modaymis_products = modaymis.findall("Product")

        for product in modaymis_products:
            sku = product.get("Sku")
            name = product.get("Name").split("-")[0]
            description = product.get("FullDescription")
            stok = product.get("StockQuantity")
            beden = None
            beden_array = []
            combination_stock = None
            combination_stock_array = []
            beden_quantity = {}

            if Product.objects.filter(stock_code=sku).exists():
                exist_product = Product.objects.filter(stock_code=sku).last()
                price = exist_product.price
                pttavm_price = None
                if float(price) < 50.00:
                    pttavm_price = price
                if float(price) >= 50.00 and float(price) < 100.00:
                    pttavm_price = price
                if float(price) >= 100.00 and float(price) < 150.00:
                    pttavm_price = price + decimal.Decimal(20.00)
                if float(price) >= 150.00 and float(price) < 200.00:
                    pttavm_price = price + decimal.Decimal(20.00)
                if float(price) >= 200.00:
                    pttavm_price = price + decimal.Decimal(20.00)

                trendyol_price = price + decimal.Decimal(25.00)
                hepsiburada_price = price + decimal.Decimal(25.00)

                exist_product.trendyol_price = trendyol_price
                exist_product.hepsiburada_price = hepsiburada_price
                exist_product.pttavm_price = pttavm_price
                exist_product.amount = stok
                exist_product.detail = description
                exist_product.save()

                size = None
                size_array = []
                beden_id = None
                beden_id_array = []
                renk_id = None
                for p in product.iter("Specifications"):
                    for s in p.iter("Specification"):
                        if s.get("Name") == 'Renk':
                            renk = s.get("Value")
                        if s.get("Name") == 'Beden Seçiniz':
                            size = s.get("Value")
                            size_array.append(size)
                for c in Color.objects.all():
                    if renk is not None:
                        if renk.lower().replace(" ", "").replace("İ", "I").replace("ı", "i").replace("ö", "o").replace(
                                "ü",
                                "u") == c.name.lower().replace(
                            " ", "").replace("İ", "I").replace("ı", "i").replace("ö", "o").replace("ü", "u"):
                            renk_id = c.id
                for p in product.iter("Combinations"):
                    for c in p.iter("Combination"):
                        combination_stock = c.get("StockQuantity")
                        combination_sku = c.get("Sku")
                        combination_gtin = c.get("Gtin")
                        combination_stock_array.append(combination_stock)
                        for a in c.iter("Attributes"):
                            for ac in a.iter("Attribute"):
                                combination_attribute_name = ac.get("Name")
                                combination_attribute_value = ac.get("Value")
                                if combination_attribute_name == 'Beden':
                                    beden = combination_attribute_value
                        for s in Size.objects.all():
                            if beden is not None:
                                if beden.lower().replace(" ", "").replace(",", ".") == s.name.lower().replace(" ",
                                                                                                              "").replace(
                                    ",", "."):
                                    beden_id_array.append(s.id)
                                    beden_id = s.id
                                    try:
                                        variations = Variants.objects.get(sku=combination_sku)
                                        variations.pttavm_price = pttavm_price
                                        variations.trendyol_price = trendyol_price
                                        variations.hepsiburada_price = hepsiburada_price
                                        variations.size_id = beden_id
                                        variations.color_id = renk_id
                                        variations.gtin = combination_gtin
                                        variations.quantity = combination_stock
                                        variations.save()
                                    except variations.DoesNotExist:
                                        variations = Variants.objects.create(sku=combination_sku, product=exist_product,
                                                                             pttavm_price=pttavm_price,
                                                                             trendyol_price=trendyol_price,
                                                                             hepsiburada_price=hepsiburada_price,
                                                                             size_id=beden_id, color_id=renk_id,
                                                                             gtin=combination_gtin,
                                                                             quantity=combination_stock, title=name, is_publish=True, price=price)
                                    except:
                                        pass