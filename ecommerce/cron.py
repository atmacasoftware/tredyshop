from trendyol.helpers import *
from trendyol.trendyol_cron import get_trendyol_orders
from product.read_xml import updateModaymisSaveXML2db, notActiveModaymisProduct, modaymissaveXML2db, \
    xml_dunyasi_gsm_update, xml_dunyasi_gsm_not_active, xml_dunyasi_diger_update
from adminpage.cron import task


def create_modaymis():
    modaymissaveXML2db()

def update_modaymis():
    updateModaymisSaveXML2db()


def find_not_active_modaymis():
    notActiveModaymisProduct()

def updatexmldunyasi():
    xml_dunyasi_gsm_update()

def updatexmldunyasi_diger():
    xml_dunyasi_diger_update()

def find_not_active_xmldunyasi():
    xml_dunyasi_gsm_not_active()

def trendyol_update_stok_fiyat():
    trendyol_schedule_update_price_stok()

def trendyol_orders():
    get_trendyol_orders()

def task_cron():
    task()