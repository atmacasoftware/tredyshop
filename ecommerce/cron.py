from trendyol.helpers import *
from trendyol.trendyol_cron import get_trendyol_orders
from product.read_xml import updateModaymisSaveXML2db, notActiveModaymisProduct, modaymissaveXML2db, \
    addGecelikDolabi, updateGecelikDolabi, notActiveGecelikDolabi, addLeyna, updateLeyna, notActiveLeyna
from adminpage.cron import task


def create_modaymis():
    modaymissaveXML2db()

def update_modaymis():
    updateModaymisSaveXML2db()

def find_not_active_modaymis():
    notActiveModaymisProduct()

def create_gecelikdolabi():
    addGecelikDolabi()

def update_gecelikdolabi():
    updateGecelikDolabi()

def find_not_active_gecelikdolabi():
    notActiveGecelikDolabi()

def create_leyna():
    addLeyna()

def update_leyna():
    updateLeyna()

def find_not_active_leyna():
    notActiveLeyna()

def trendyol_update_stok_fiyat():
    trendyol_schedule_update_price_stok()

def trendyol_send_product():
    trendyol_schedule_send_product()

def trendyol_orders():
    get_trendyol_orders()

def task_cron():
    task()