from trendyol.helpers import *
from product.read_xml import updateModaymisSaveXML2db,notActiveModaymisProduct

def update_modaymis():
    updateModaymisSaveXML2db()


def find_not_active_modaymis():
    notActiveModaymisProduct()


def trendyol_update_stok_fiyat():
    trendyol_schedule_update_price_stok()

def trendyol_orders():
    get_cron_trendyol_orders()