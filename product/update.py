from product.models import Pattern, ApiProduct, FabricType, EnvironmentType, CollerType, Waist, Height


def kalip():
    kalip_liste = ['Normal', 'Rahat', 'Dar']

    regular_pattern = Pattern.objects.get(name='Regular')
    comfort_pattern = Pattern.objects.get(name='Comfort')
    dar_pattern = Pattern.objects.get(name='Dar')

    product = ApiProduct.objects.all().exclude(subcategory__category_no=5 or 6)

    data = 'failed'

    for p in product:
        if p.pattern == '' or p.pattern == None:
            for d in p.detail.split():
                for liste in kalip_liste:
                    if liste.lower() in d.lower():
                        if liste == 'Normal':
                            p.pattern = regular_pattern
                        elif liste == 'Rahat':
                            p.pattern = comfort_pattern
                        elif liste == 'Dar':
                            p.pattern = dar_pattern
                        else:
                            p.pattern = regular_pattern
                        p.save()
                        data = 'success'
    return data


def kumas():
    kumas_list = ['deri','triko', 'dokuma', 'dantel', 'denim', 'kot denim', 'kaşkorse', 'poplin', 'örme', 'flamlı']
    product = ApiProduct.objects.all().exclude(subcategory__category_no=5 or 6)
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
        if p.fabrictype == '' or p.fabrictype == None:
            p.fabrictype = dokuma
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
                        p.fabrictype = kaskorse
                    if liste == 'flamlı':
                        p.fabrictype = flamli
                    p.save()

    return 'success'


def ortam():
    product = ApiProduct.objects.all().exclude(subcategory__category_no=5 or 6)
    casual = EnvironmentType.objects.get(id=4)

    for p in product:
        if p.environment == '' or p.environment == None:
            p.environment = casual
            p.save()

def yaka():
    product = ApiProduct.objects.filter(subcategory__category_no=1)

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
        if p.collartype == '' or p.collartype == None:
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
    product = ApiProduct.objects.filter(dropshipping="Modaymış")

    for p in product:
        p.sex = 'Kadın/Kız'
        p.save()

def bel():
    product = ApiProduct.objects.filter(subbottomcategory_id=8 or 7 or 9 or 10 or 11 or 13 or 14)

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

    for p in product:
        if p.waist == '' or p.waist == None:
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
    product = ApiProduct.objects.all().exclude(subcategory_id=7 or 6 or 5)

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
        if p.height == '' or p.height == None:
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