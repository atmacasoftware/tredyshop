from urllib.request import urlopen, Request
import decimal
import xml.etree.ElementTree as ET
from categorymodel.models import *
from product.models import *
from adminpage.models import *

class ReadXml():
    def customPrice(self, starter, finish, price):
        while finish < 15000:
            if float(price) >= starter and float(price) < finish:
                price = finish - 0.10
                return decimal.Decimal(price)

            starter += 10
            finish += 10

    def getUrl(self,url):
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

    def tredyshopPrice(self,urun_maliyeti, kdv):
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
                duzeltilmis_satis_fiyati = self.customPrice(0, 10, satis_fiyati)
        return duzeltilmis_satis_fiyati

    def trendyolPrice(self, urun_maliyeti, kdv, indirim=False):
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
                duzeltilmis_satis_fiyati = self.customPrice(0, 10, satis_fiyati)
        return duzeltilmis_satis_fiyati

    def ciceksepetiPrice(self, urun_maliyeti, kdv, indirim=False):
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
                duzeltilmis_satis_fiyati = self.customPrice(0, 10, satis_fiyati)
        return duzeltilmis_satis_fiyati