from categorymodel.models import SubCategory
from product.models import Pattern, Product, FabricType, EnvironmentType, CollerType, Waist, Height, LegType, Sex, \
    Product, ProductVariant, Size


def beden():
    ic_giyim_products = ProductVariant.objects.filter(product__subcategory_id=7)
    for product in ic_giyim_products:
        if product.size is not None:
            if product.size.name == "S-M":
                product.size = Size.objects.get(id=442)
                product.save()

            if product.size.name == "L-XL":
                product.size = Size.objects.get(id=443)
                product.save()
    sweat_products = ProductVariant.objects.filter(product__subbottomcategory_id=65)
    for product in sweat_products:
        if product.size is not None:
            if product.size.name == "STD":
                product.size = Size.objects.get(id=210)
                product.save()
            if product.size.name == "Standart":
                product.size = Size.objects.get(id=210)
                product.save()
            if product.size.name == "S-M":
                product.size = Size.objects.get(id=442)
                product.save()
            if product.size.name == "L-XL":
                product.size = Size.objects.get(id=443)
                product.save()
            if product.size.name == "XXL":
                product.size = Size.objects.get(id=13)
                product.save()
    bluz_products = ProductVariant.objects.filter(product__subbottomcategory_id=2)
    for product in bluz_products:
        if product.size is not None:
            if product.size.name == "S-M":
                product.size = Size.objects.get(id=442)
                product.save()
            if product.size.name == "L-XL":
                product.size = Size.objects.get(id=443)
                product.save()
    atlet_products = ProductVariant.objects.filter(product__subbottomcategory_id=1)
    for product in atlet_products:
        if product.size is not None:
            if product.size.name == "S-M":
                product.size = Size.objects.get(id=442)
                product.save()
            if product.size.name == "L-XL":
                product.size = Size.objects.get(id=443)
                product.save()
    tshirt_products = ProductVariant.objects.filter(product__subbottomcategory_id=5)
    for product in tshirt_products:
        if product.size is not None:
            if product.size.name == "S-M":
                product.size = Size.objects.get(id=442)
                product.save()
            if product.size.name == "L-XL":
                product.size = Size.objects.get(id=443)
                product.save()
    pijama_products = ProductVariant.objects.filter(product__subbottomcategory_id=94)
    for product in pijama_products:
        if product.size is not None:
            if product.size.name == "XXL":
                product.size = Size.objects.get(id=13)
                product.save()
    esofman_products = ProductVariant.objects.filter(product__subbottomcategory_id=12)
    for product in esofman_products:
        if product.size is not None:
            if product.size.name == "XXL":
                product.size = Size.objects.get(id=13)
                product.save()
    esofman_alti = ProductVariant.objects.filter(product__subbottomcategory_id=13)
    for product in esofman_alti:
        if product.size is not None:
            if product.size.name == "XXL":
                product.size = Size.objects.get(id=13)
                product.save()
def kalip():
    kalip_liste = ['Normal', 'Rahat', 'Dar']

    regular_pattern = Pattern.objects.get(name='Regular')
    comfort_pattern = Pattern.objects.get(name='Comfort')
    dar_pattern = Pattern.objects.get(name='Dar')
    slim_pattern = Pattern.objects.get(name='Slim')

    product = Product.objects.all().exclude(subcategory__category_no=5 or 6)

    data = 'failed'

    for p in product:
        if p.pattern == '' or p.pattern == None or p.pattern == 'None':
            p.pattern = regular_pattern
            p.save()
            for d in p.detail.split():
                for liste in kalip_liste:
                    if liste.lower() in d.lower():
                        if liste == 'Normal':
                            p.pattern = regular_pattern
                        elif liste == 'Rahat':
                            p.pattern = comfort_pattern
                        elif liste == 'Dar':
                            p.pattern = slim_pattern
                        else:
                            p.pattern = regular_pattern
                        p.save()
                        data = 'success'
    return data


def kumas():
    kumas_list = ['deri','triko', 'dokuma', 'dantel', 'denim', 'kot denim', 'kaşkorse', 'poplin', 'örme', 'flamlı']
    product = Product.objects.all().exclude(subcategory__category_no=5 or 6)
    suni_deri = FabricType.objects.get(id=6)
    dokuma = FabricType.objects.get(id=3)
    dantel = FabricType.objects.get(id=1)
    orme = FabricType.objects.get(id=4)
    denim = FabricType.objects.get(id=2)
    triko = FabricType.objects.get(id=5)
    poplin = FabricType.objects.get(id=10)
    kaskorse = FabricType.objects.get(id=8)
    flamli = FabricType.objects.get(id=7)

    for p in product:

        if p.fabrictype == '' or p.fabrictype == None or p.fabrictype == 'None':
            p.fabrictype = dokuma
            p.save()
            for liste in kumas_list:
                if liste.lower() in p.title.lower().split():
                    if liste == 'deri':
                        p.fabrictype = suni_deri
                    if liste == 'triko':
                        p.fabrictype = triko
                    if liste == 'dokuma':
                        p.fabrictype = dokuma
                    if liste == 'dantel':
                        p.fabrictype = dantel
                    if liste == 'örme':
                        p.fabrictype = orme
                    if liste == 'denim':
                        p.fabrictype = denim
                    if liste == 'poplin':
                        p.fabrictype = poplin
                    if liste == 'kaşkorse':
                        p.fabrictype = dokuma
                    if liste == 'flamlı':
                        p.fabrictype = dokuma
                    p.save()
        try:
            if p.subbottomcategory.category_no == "1015":
                p.fabrictype = denim
                p.save()
        except:
            pass
    return 'success'


def ortam():
    product = Product.objects.all().exclude(subcategory__category_no=5 or 6)
    casual = EnvironmentType.objects.get(id=4)

    for p in product:
        if p.environment == '' or p.environment == None or p.environment == 'None':
            p.environment = casual
            p.save()

def yaka():
    product = Product.objects.filter(subcategory__category_no=1)

    yaka_list = ['hakim', 'kare', 'balıkçı', 'bisiklet', 'u', 'v', 'dik', 'polo', 'dantel', 'fermuarlı', 'düğmeli', 'madonna']

    hakim = CollerType.objects.get(id=18)
    kare = CollerType.objects.get(id=23)
    balikci = CollerType.objects.get(id=3)
    bisiklet = CollerType.objects.get(id=5)
    u_yaka = CollerType.objects.get(id=38)
    v_yaka = CollerType.objects.get(id=30)
    dik = CollerType.objects.get(id=13)
    polo = CollerType.objects.get(id=27)
    dantel = CollerType.objects.get(id=47)
    fermuarli = CollerType.objects.get(id=37)
    dugmeli = CollerType.objects.get(id=35)
    madonna = CollerType.objects.get(id=58)

    for p in product:
        if p.collartype == '' or p.collartype == None or p.collartype == 'None':
            for liste in yaka_list:
                if liste.lower() in p.title.lower().split():
                    if liste == 'hakim':
                        p.collartype = hakim
                    if liste == 'kare':
                        p.collartype = kare
                    if liste == 'balıkçı':
                        p.collartype = balikci
                    if liste == 'bisiklet':
                        p.collartype = bisiklet
                    if liste == 'u':
                        p.collartype = u_yaka
                    if liste == 'v':
                        p.collartype = v_yaka
                    if liste == 'dik':
                        p.collartype = dik
                    if liste == 'polo':
                        p.collartype = polo
                    if liste == 'dantel':
                        p.collartype = dantel
                    if liste == 'fermuarlı':
                        p.collartype = fermuarli
                    if liste == 'düğmeli':
                        p.collartype = dugmeli
                    if liste == 'madonna':
                        p.collartype = madonna
                    p.save()

def cinsiyet():
    products = Product.objects.filter(category_id=1, is_publish=True)
    men = Sex.objects.get(id=1)
    women = Sex.objects.get(id=2)

    for product in products:
        if "Erkek" in product.title:
            product.sextype = men
            product.save()

        else:
            product.sextype = women
            product.save()

    return 'success'

def bel():

    bel_list = ['yüksek bel', 'süper yüksek bel', 'regular', 'paperbag', 'normal bel', 'lastikli', 'kuşaklı', 'kemerli', 'jogger lastik bel', 'extra yüksek bel', 'düşük bel']

    yuksek_bel = Waist.objects.get(id=132)
    super_yuksek_bel = Waist.objects.get(id=131)
    regular = Waist.objects.get(id=130)
    paperbag = Waist.objects.get(id=129)
    normal = Waist.objects.get(id=128)
    lastikli = Waist.objects.get(id=127)
    kusakli = Waist.objects.get(id=126)
    kemerli = Waist.objects.get(id=125)
    jogger_lastik = Waist.objects.get(id=124)
    extra_yuksek = Waist.objects.get(id=123)
    dusuk_bel = Waist.objects.get(id=122)

    for p in Product.objects.filter(subbottomcategory_id=8):
        if p.waist == '' or p.waist == None or p.waist == 'None':
            if p.subbottomcategory.category_no == "1015":
                p.waist = yuksek_bel
                p.save()
            else:
                for liste in bel_list:
                    if liste.lower() in p.title.lower():
                        if liste == 'yüksek bel':
                            p.waist = yuksek_bel
                        if liste == 'süper yüksek bel':
                            p.waist = super_yuksek_bel
                        if liste == 'regular':
                            p.waist = regular
                        if liste == 'paperbag':
                            p.waist = paperbag
                        if liste == 'normal bel':
                            p.waist = normal
                        if liste == 'lastikli':
                            p.waist = lastikli
                        if liste == 'kuşaklı':
                            p.waist = kusakli
                        if liste == 'kemerli':
                            p.waist = kemerli
                        if liste == 'jogger lastik bel':
                            p.waist = jogger_lastik
                        if liste == 'extra yüksek bel':
                            p.waist = extra_yuksek
                        if liste == 'düşük bel':
                            p.waist = dusuk_bel
                        p.save()
                    else:
                        p.waist = normal
                        p.save()

    for p in Product.objects.filter(subbottomcategory_id=7):
        if p.waist == '' or p.waist == None or p.waist == 'None':
            for liste in bel_list:
                if liste.lower() in p.title.lower():
                    if liste == 'yüksek bel':
                        p.waist = yuksek_bel
                    if liste == 'süper yüksek bel':
                        p.waist = super_yuksek_bel
                    if liste == 'regular':
                        p.waist = regular
                    if liste == 'paperbag':
                        p.waist = paperbag
                    if liste == 'normal bel':
                        p.waist = normal
                    if liste == 'lastikli':
                        p.waist = lastikli
                    if liste == 'kuşaklı':
                        p.waist = kusakli
                    if liste == 'kemerli':
                        p.waist = kemerli
                    if liste == 'jogger lastik bel':
                        p.waist = jogger_lastik
                    if liste == 'extra yüksek bel':
                        p.waist = extra_yuksek
                    if liste == 'düşük bel':
                        p.waist = dusuk_bel
                    p.save()
                else:
                    p.waist = normal
                    p.save()

    for p in Product.objects.filter(subbottomcategory_id=9):
        if p.waist == '' or p.waist == None or p.waist == 'None':
            for liste in bel_list:
                if liste.lower() in p.title.lower():
                    if liste == 'yüksek bel':
                        p.waist = yuksek_bel
                    if liste == 'süper yüksek bel':
                        p.waist = super_yuksek_bel
                    if liste == 'regular':
                        p.waist = regular
                    if liste == 'paperbag':
                        p.waist = paperbag
                    if liste == 'normal bel':
                        p.waist = normal
                    if liste == 'lastikli':
                        p.waist = lastikli
                    if liste == 'kuşaklı':
                        p.waist = kusakli
                    if liste == 'kemerli':
                        p.waist = kemerli
                    if liste == 'jogger lastik bel':
                        p.waist = jogger_lastik
                    if liste == 'extra yüksek bel':
                        p.waist = extra_yuksek
                    if liste == 'düşük bel':
                        p.waist = dusuk_bel
                    p.save()
                else:
                    p.waist = normal
                    p.save()

    for p in Product.objects.filter(subbottomcategory_id=10):
        if p.waist == '' or p.waist == None or p.waist == 'None':
            for liste in bel_list:
                if liste.lower() in p.title.lower():
                    if liste == 'yüksek bel':
                        p.waist = yuksek_bel
                    if liste == 'süper yüksek bel':
                        p.waist = super_yuksek_bel
                    if liste == 'regular':
                        p.waist = regular
                    if liste == 'paperbag':
                        p.waist = paperbag
                    if liste == 'normal bel':
                        p.waist = normal
                    if liste == 'lastikli':
                        p.waist = lastikli
                    if liste == 'kuşaklı':
                        p.waist = kusakli
                    if liste == 'kemerli':
                        p.waist = kemerli
                    if liste == 'jogger lastik bel':
                        p.waist = jogger_lastik
                    if liste == 'extra yüksek bel':
                        p.waist = extra_yuksek
                    if liste == 'düşük bel':
                        p.waist = dusuk_bel
                    p.save()
                else:
                    p.waist = normal
                    p.save()
        for p in Product.objects.filter(subbottomcategory_id=11):
            if p.waist == '' or p.waist == None or p.waist == 'None':
                for liste in bel_list:
                    if liste.lower() in p.title.lower():
                        if liste == 'yüksek bel':
                            p.waist = yuksek_bel
                        if liste == 'süper yüksek bel':
                            p.waist = super_yuksek_bel
                        if liste == 'regular':
                            p.waist = regular
                        if liste == 'paperbag':
                            p.waist = paperbag
                        if liste == 'normal bel':
                            p.waist = normal
                        if liste == 'lastikli':
                            p.waist = lastikli
                        if liste == 'kuşaklı':
                            p.waist = kusakli
                        if liste == 'kemerli':
                            p.waist = kemerli
                        if liste == 'jogger lastik bel':
                            p.waist = jogger_lastik
                        if liste == 'extra yüksek bel':
                            p.waist = extra_yuksek
                        if liste == 'düşük bel':
                            p.waist = dusuk_bel
                        p.save()
                    else:
                        p.waist = normal
                        p.save()

        for p in Product.objects.filter(subbottomcategory_id=12):
            if p.waist == '' or p.waist == None or p.waist == 'None':
                for liste in bel_list:
                    if liste.lower() in p.title.lower():
                        if liste == 'yüksek bel':
                            p.waist = yuksek_bel
                        if liste == 'süper yüksek bel':
                            p.productwaist = super_yuksek_bel
                        if liste == 'regular':
                            p.waist = regular
                        if liste == 'paperbag':
                            p.waist = paperbag
                        if liste == 'normal bel':
                            p.waist = normal
                        if liste == 'lastikli':
                            p.waist = lastikli
                        if liste == 'kuşaklı':
                            p.waist = kusakli
                        if liste == 'kemerli':
                            p.waist = kemerli
                        if liste == 'jogger lastik bel':
                            p.waist = jogger_lastik
                        if liste == 'extra yüksek bel':
                            p.waist = extra_yuksek
                        if liste == 'düşük bel':
                            p.waist = dusuk_bel
                        p.save()
                    else:
                        p.waist = normal
                        p.save()

        for p in Product.objects.filter(subbottomcategory_id=13):
            if p.waist == '' or p.waist == None or p.waist == 'None':
                for liste in bel_list:
                    if liste.lower() in p.title.lower():
                        if liste == 'yüksek bel':
                            p.waist = yuksek_bel
                        if liste == 'süper yüksek bel':
                            p.waist = super_yuksek_bel
                        if liste == 'regular':
                            p.waist = regular
                        if liste == 'paperbag':
                            p.waist = paperbag
                        if liste == 'normal bel':
                            p.waist = normal
                        if liste == 'lastikli':
                            p.waist = lastikli
                        if liste == 'kuşaklı':
                            p.waist = kusakli
                        if liste == 'kemerli':
                            p.waist = kemerli
                        if liste == 'jogger lastik bel':
                            p.waist = jogger_lastik
                        if liste == 'extra yüksek bel':
                            p.waist = extra_yuksek
                        if liste == 'düşük bel':
                            p.waist = dusuk_bel
                        p.save()
                    else:
                        p.waist = normal
                        p.save()

        for p in Product.objects.filter(subbottomcategory_id=14):
            if p.waist == '' or p.waist == None or p.waist == 'None':
                for liste in bel_list:
                    if liste.lower() in p.title.lower():
                        if liste == 'yüksek bel':
                            p.waist = yuksek_bel
                        if liste == 'süper yüksek bel':
                            p.waist = super_yuksek_bel
                        if liste == 'regular':
                            p.waist = regular
                        if liste == 'paperbag':
                            p.waist = paperbag
                        if liste == 'normal bel':
                            p.waist = normal
                        if liste == 'lastikli':
                            p.waist = lastikli
                        if liste == 'kuşaklı':
                            p.waist = kusakli
                        if liste == 'kemerli':
                            p.waist = kemerli
                        if liste == 'jogger lastik bel':
                            p.waist = jogger_lastik
                        if liste == 'extra yüksek bel':
                            p.waist = extra_yuksek
                        if liste == 'düşük bel':
                            p.waist = dusuk_bel
                        p.save()
                    else:
                        p.waist = normal
                        p.save()
    return 'success'


def boy():
    product = Product.objects.all().exclude(subcategory_id=7 or 6 or 5)

    boy_list = ['bilek boy', 'crop', 'kısa', 'maxi','midi', 'mini', 'regular', 'standart', 'uzun', 'kapri']

    bilek = Height.objects.get(id=52)
    crop = Height.objects.get(id=53)
    kisa = Height.objects.get(id=54)
    maxi = Height.objects.get(id=55)
    midi = Height.objects.get(id=56)
    mini = Height.objects.get(id=57)
    regular = Height.objects.get(id=58)
    standart = Height.objects.get(id=59)
    uzun = Height.objects.get(id=60)
    kapri = Height.objects.get(id=61)

    for p in product:
        if p.height == '' or p.height == None or p.height == 'None':
            for liste in boy_list:
                if liste.lower() in p.title.lower():
                    if liste == 'bilek boy':
                        p.height = bilek
                    if liste == 'crop':
                        p.height = crop
                    if liste == 'kısa':
                        p.height = kisa
                    if liste == 'maxi':
                        p.height = maxi
                    if liste == 'midi':
                        p.height = midi
                    if liste == 'mini':
                        p.height = mini
                    if liste == 'regular':
                        p.height = regular
                    if liste == 'standart':
                        p.height = standart
                    if liste == 'uzun':
                        p.height = uzun
                    if liste == 'kapri':
                        p.height = kapri
                    p.save()
                else:
                    p.height = regular
                    p.save()
    return 'success'

def paca():
    product = Product.objects.filter(subbottomcategory_id=7 or 8 or 9 or 11 or 13 or 14)
    paca_list = LegType.objects.all()

    for p in product:
        if p.legtype == '' or p.legtype == None or p.legtype == 'None':
            for liste in paca_list:
                if liste.name.lower() in p.title.lower():
                    p.legtype = liste
                    p.save()

    return 'success'

def kategori():
    product = Product.objects.all()

    for p in product:
        if p.is_completed_category == False:
            if p.subbottomcategory:
                if p.subbottomcategory.category_no == "1010" and p.subcategory == None:
                    p.subcategory = SubCategory.objects.get(category_no="1")
                    p.save()

                if p.subbottomcategory.category_no == "1038" and p.subcategory == None:
                    p.subcategory = SubCategory.objects.get(category_no="7")
                    p.save()

            if 'çorap' in p.title.lower() or 'çorabı' in p.title.lower():
                p.subcategory_id = 7
                p.subbottomcategory_id = 105
                p.save()

            if 'havlu' in p.title.lower():
                p.subcategory_id = 86
                p.subbottomcategory_id = 106
                p.save()

            if 'eşofman altı' in p.title.lower():
                p.subcategory_id = 3
                p.subbottomcategory_id = 13
                p.save()

            if 'bebek zıbın' in p.title.lower() or 'çocuk zıbın' in p.title.lower():
                p.subcategory_id = 86
                p.subbottomcategory_id = 102
                p.save()

            if 'bebek tulum' in p.title.lower():
                p.subcategory_id = 86
                p.subbottomcategory_id = 103
                p.save()

            if 'bebek takım' in p.title.lower():
                p.subcategory_id = 86
                p.subbottomcategory_id = 104
                p.save()

            if 'tişört' in p.title.lower():
                p.subcategory_id = 1
                p.subbottomcategory_id = 5
                p.save()

            if 'poliviskon takım' in p.title.lower() or 'poliviskon önü düğmeli takım' in p.title.lower() or 'poliviskon düğmeli takım' in p.title.lower():
                p.subcategory_id = 3
                p.subbottomcategory_id = 94
                p.save()

            if 'süet takım' in p.title.lower():
                p.subcategory_id = 3
                p.subbottomcategory_id = 94
                p.save()

            if 'peluş takım' in p.title.lower():
                p.subcategory_id = 3
                p.subbottomcategory_id = 94
                p.save()

            if 'fitilli takım' in p.title.lower():
                p.subcategory_id = 3
                p.subbottomcategory_id = 94
                p.save()

            if 'panço' in p.title.lower():
                p.subcategory_id = 1
                p.subbottomcategory_id = 77
                p.save()

            if 'kostüm' in p.title.lower():
                p.subcategory_id = 7
                p.subbottomcategory_id = 87
                p.save()

            if 'babydoll' in p.title.lower():
                p.subcategory_id = 7
                p.subbottomcategory_id = 85
                p.save()

            if 'crop triko' in p.title.lower():
                p.subcategory_id = 1
                p.subbottomcategory_id = 100
                p.save()

            if 'bluz' in p.title.lower():
                p.subcategory_id = 1
                p.subbottomcategory_id = 2
                p.save()

            if 'body' in p.title.lower():
                p.subcategory_id = 1
                p.subbottomcategory_id = 100
                p.save()

            if 'hırka' in p.title.lower():
                p.subcategory_id = 1
                p.subbottomcategory_id = 66
                p.save()

            if 'terlik' in p.title.lower() or 'ev terliği' in p.title.lower():
                p.subcategory_id = 5
                p.subbottomcategory_id = 80
                p.save()

            if 'bot' in p.title.lower():
                p.subcategory_id = 5
                p.subbottomcategory_id = 73
                p.save()

            if 'sandalet' in p.title.lower():
                p.subcategory_id = 5
                p.subbottomcategory_id = 90
                p.save()

            if 'ev botu' in p.title.lower():
                p.subcategory_id = 5
                p.subbottomcategory_id = 81
                p.save()

            if 'çizme' in p.title.lower():
                p.subcategory_id = 5
                p.subbottomcategory_id = 78
                p.save()

            if 'panduf' in p.title.lower():
                p.subcategory_id = 5
                p.subbottomcategory_id = 76
                p.save()

            if 'pijama takımı' in p.title.lower():
                p.subcategory_id = 3
                p.subbottomcategory_id = 94
                p.save()

            if 'sabahlık' in p.title.lower():
                p.subcategory_id = 3
                p.subbottomcategory_id = 94
                p.save()

            if 'peluş takımı' in p.title.lower():
                p.subcategory_id = 3
                p.subbottomcategory_id = 94
                p.save()

            if 'şortlu takım' in p.title.lower():
                p.subcategory_id = 3
                p.subbottomcategory_id = 94
                p.save()

            if 'çocuk takım' in p.title.lower():
                p.subcategory_id = 3
                p.subbottomcategory_id = 94
                p.save()

            if 'bileklik' in p.title.lower():
                p.subcategory_id = 6
                p.subbottomcategory_id = 98
                p.save()

            if 'kolye' in p.title.lower():
                p.subcategory_id = 6
                p.subbottomcategory_id = 97
                p.save()

            if 'küpe' in p.title.lower():
                p.subcategory_id = 6
                p.subbottomcategory_id = 99
                p.save()

            if 'atlet' in p.title.lower():
                p.subcategory_id = 1
                p.subbottomcategory_id = 1
                p.save()

            if 'ceket' in p.title.lower():
                p.subcategory_id = 1
                p.subbottomcategory_id = 3
                p.save()

            if 'yağmurluk' in p.title.lower():
                p.subcategory_id = 1
                p.subbottomcategory_id = 68
                p.save()

            if 'babet' in p.title.lower():
                p.subcategory_id = 5
                p.subbottomcategory_id = 89
                p.save()

            if 'günlük ayakkabı' in p.title.lower():
                p.subcategory_id = 5
                p.subbottomcategory_id = 21
                p.save()

            if 'çanta' in p.title.lower():
                p.subcategory_id = 6
                p.subbottomcategory_id = 24
                p.save()

            if 'şal' in p.title.lower():
                p.subcategory_id = 6
                p.subbottomcategory_id = 62
                p.save()

            if 'kaza' in p.title.lower():
                p.subcategory_id = 1
                p.subbottomcategory_id = 74
                p.save()

            if 'kaban' in p.title.lower():
                p.subcategory_id = 1
                p.subbottomcategory_id = 74
                p.save()

            if 'sweat' in p.title.lower():
                p.subcategory_id = 1
                p.subbottomcategory_id = 65
                p.save()

            if 'çocuk bornoz' in p.title.lower() or 'bebek bornoz' in p.title.lower():
                p.subcategory_id = 86
                p.subbottomcategory_id = 106
                p.save()

            if 'sütyen tek damla desen' in p.title.lower() or 'sütyen tek damla desenli' in p.title.lower():
                p.subcategory_id = 7
                p.subbottomcategory_id = 27
                p.save()

            if 'tayt' in p.title.lower():
                p.subcategory_id = 2
                p.subbottomcategory_id = 11
                p.save()

            if 'salopet' in p.title.lower():
                p.subcategory_id = 4
                p.subbottomcategory_id = 86
                p.save()

            if 'fantezi sütyen takım' in p.title.lower() or 'jartiyer sütyen takım' in p.title.lower():
                p.subcategory_id = 7
                p.subbottomcategory_id = 88
                p.save()

    return 'success'


def yas_grubu():
    products = Product.objects.filter(is_publish=True)
    for product in products:
        for t in product.title.split(' '):
            if t == "Çocuk":
                product.age_group = "Çocuk"
                product.save()

            if t == "Bebek":
                product.age_group = "Bebek"
                product.save()

    return "success"

def topukTipi():
    product = Product.objects.filter(subcategory_id=5)
