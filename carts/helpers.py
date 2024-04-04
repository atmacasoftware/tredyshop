import base64
import hashlib
import hmac
import html
import json
import random
import requests
import time
from django.shortcuts import render, HttpResponse
from django.views.decorators.csrf import csrf_exempt

from ecommerce import settings

def paytr_api(email, payment_amount, merchant_oid, full_name, address, mobile, item, ip, installment_count):
    merchant_id = '379607'
    merchant_key = b'xXWCLan3y1m97K4u'
    merchant_salt = b'3yfMDbiraNXoG311'

    if settings.DEBUG == True:
        merchant_ok_url = f'http://127.0.0.1:8000/odeme-tamamlandi/siparis_no={str(merchant_oid)}'
    else:
        merchant_ok_url = f'https://www.tredyshop.com/odeme-tamamlandi/siparis_no={str(merchant_oid)}'

    merchant_fail_url = 'https://www.tredyshop.com/odeme_basarisiz'

    user_basket = html.unescape(json.dumps([item]))

    merchant_oid = str(merchant_oid)
    debug_on = '1'

    # 3d'siz işlem
    non_3d = '0'

    client_lang = 'tr'

    non3d_test_failed = '0'

    if settings.DEBUG == True:
        user_ip = '213.238.183.81'
    else:
        user_ip = ip

    email = email

    str_payment = str(payment_amount)

    payment_amount = int(payment_amount * 100)
    currency = 'TL'
    payment_type = 'card'

    user_name = full_name
    user_address = address
    user_phone = mobile

    timeout_limit = 30

    debug_on = 1

    test_mode = "1"

    no_installment = 0

    max_installment = 0

    # Alabileceği değerler; advantage, axess, combo, bonus, cardfinans, maximum, paraf, world, saglamkart

    installment_count = "0"

    hash_str = merchant_id + user_ip + merchant_oid + email + str_payment + payment_type + installment_count + currency + test_mode + non_3d
    paytr_token = base64.b64encode(hmac.new(merchant_key, hash_str.encode() + merchant_salt, hashlib.sha256).digest())

    data = {
        'merchant_id': merchant_id,
        'user_ip': user_ip,
        'merchant_oid': merchant_oid,
        'email': email,
        'payment_type': payment_type,
        'payment_amount': payment_amount,
        'currency': currency,
        'non_3d': non_3d,
        'merchant_ok_url': merchant_ok_url,
        'merchant_fail_url': merchant_fail_url,
        'user_name': user_name,
        'user_address': user_address,
        'user_phone': user_phone,
        'user_basket': user_basket,
        'debug_on': debug_on,
        'no_installment': no_installment,
        'max_installment':max_installment,
        'client_lang': client_lang,
        'paytr_token': paytr_token.decode(),
        'non3d_test_failed': non3d_test_failed,
        'installment_count': installment_count,
        'test_mode':test_mode,
    }

    return data


def paytr_post(email, payment_amount, merchant_oid, full_name, address, mobile, item, ip, installment_count, card_holder, card_number, cvv, expiry_month, expiry_year, kart_tipi):
    merchant_id = '379607'
    merchant_key = b'xXWCLan3y1m97K4u'
    merchant_salt = b'3yfMDbiraNXoG311'

    if settings.DEBUG == True:
        merchant_ok_url = f'http://127.0.0.1:8000/odeme-tamamlandi/siparis_no={str(merchant_oid)}'
    else:
        merchant_ok_url = f'https://www.tredyshop.com/odeme-tamamlandi/siparis_no={str(merchant_oid)}'

    merchant_fail_url = 'https://www.tredyshop.com/odeme_basarisiz'

    user_basket = html.unescape(json.dumps([item]))

    merchant_oid = str(merchant_oid)
    debug_on = '1'

    # 3d'siz işlem
    non_3d = "0"

    client_lang = "tr"

    non3d_test_failed = '0'

    if settings.DEBUG == True:
        user_ip = '213.238.183.81'
    else:
        user_ip = ip

    email = email

    payment_amount = int(float(payment_amount)*100)
    currency = 'TL'
    payment_type = 'card'

    user_name = full_name
    user_address = address
    user_phone = mobile

    timeout_limit = 30

    debug_on = 1

    test_mode = "1"

    no_installment = 0

    max_installment = 0

    installment_count = "0"

    hash_str = merchant_id + user_ip + merchant_oid + email + str(
        payment_amount) + payment_type + installment_count + currency + test_mode + non_3d
    paytr_token = base64.b64encode(hmac.new(merchant_key, hash_str.encode() + merchant_salt, hashlib.sha256).digest())

    params = {
        'merchant_id': merchant_id,
        'paytr_token': paytr_token.decode(),
        'user_ip': user_ip,
        'merchant_oid': merchant_oid,
        'email': email,
        'payment_type': payment_type,
        'payment_amount': payment_amount,
        'installment_count': installment_count,
        'card_type': kart_tipi,
        'currency': currency,
        'client_lang': client_lang,
        'test_mode': test_mode,
        'non_3d': non_3d,
        'non3d_test_failed': non3d_test_failed,
        'cc_owner': card_holder,
        'card_number': card_number,
        'expiry_month': expiry_month,
        'expiry_year':expiry_year,
        'cvv':cvv,
        'merchant_ok_url': merchant_ok_url,
        'merchant_fail_url': merchant_fail_url,
        'user_name': user_name,
        'user_address': user_address,
        'user_phone': user_phone,
        'user_basket': user_basket,
        'debug_on': debug_on,
        'no_installment': no_installment,
        'max_installment':max_installment,
    }

    result = requests.post('https://www.paytr.com/odeme', params)
    return result

def create_order_token(user_ip, merchant_oid, email, payment_amount, installment_count):
    merchant_id = '379607'
    merchant_key = b'xXWCLan3y1m97K4u'
    merchant_salt = b'3yfMDbiraNXoG311'

    payment_amount = payment_amount
    currency = 'TL'
    payment_type = 'card'
    test_mode = "0"
    non_3d = '0'

    hash_str = merchant_id + user_ip + merchant_oid + email + str(
        payment_amount) + payment_type + installment_count + currency + test_mode + non_3d
    paytr_token = base64.b64encode(hmac.new(merchant_key, hash_str.encode() + merchant_salt, hashlib.sha256).digest())

    return paytr_token.decode()

def card_type(bin_code):

    url = f"https://api.apilayer.com/bincheck/{bin_code}"

    payload = {}
    headers = {
        "apikey": "aMXFVtUWkAMrgWacOiecjEEax60OhnvB"
    }

    response = requests.request("GET", url, headers=headers, data=payload)

    status_code = response.status_code
    result = response.text

    return result


def paytr_sorgu(order_number):
    merchant_id = '379607'
    merchant_key = b'xXWCLan3y1m97K4u'
    merchant_salt = '3yfMDbiraNXoG311'
    merchant_oid = str(order_number)

    # Bu kısımda herhangi bir değişiklik yapmanıza gerek yoktur.
    hash_str = merchant_id + merchant_oid + merchant_salt
    paytr_token = base64.b64encode(hmac.new(merchant_key, hash_str.encode(), hashlib.sha256).digest())

    params = {
        'merchant_id': merchant_id,
        'merchant_oid': merchant_oid,
        'paytr_token': paytr_token
    }

    result = requests.post('https://www.paytr.com/odeme/durum-sorgu', params)
    res = json.loads(result.text)

    if res['status'] == 'success':
        order_status = {
            'payment_amount': res['payment_amount'],
            'payment_total': res['payment_total'],
            'payment_date': res['payment_date'],
            'odeme_tipi': res['odeme_tipi'],
            'taksit': res['taksit'],
            'kart_marka': res['kart_marka'],
            'kesinti_tutari': res['kesinti_tutari'],
            'net_tutar': res['net_tutar'],
        }

        for return_success in res['returns']:
            print(return_success)
        return order_status
    else:
        error = (res['err_no'] + ' ' + res['err_msg'])
        return error


def paytr_taksit_sorgu():
    merchant_id = '379607'
    merchant_key = b'xXWCLan3y1m97K4u'
    merchant_salt = '3yfMDbiraNXoG311'

    request_id = str(time.time())

    hash_str = merchant_id + request_id + merchant_salt
    paytr_token = base64.b64encode(hmac.new(merchant_key, hash_str.encode(), hashlib.sha256).digest())

    params = {
        'merchant_id': merchant_id,
        'request_id': request_id,
        'paytr_token': paytr_token,
    }

    result = requests.post('https://www.paytr.com/odeme/taksit-oranlari', params)
    res = json.loads(result.text)
    taksit_data = {
        'world': res['oranlar']['world'],
        'axess': res['oranlar']['axess'],
        'maximum': res['oranlar']['maximum'],
        'cardfinans': res['oranlar']['cardfinans'],
        'paraf': res['oranlar']['paraf'],
        'advantage': res['oranlar']['advantage'],
        'combo': res['oranlar']['combo'],
        'bonus': res['oranlar']['bonus'],
        'saglamkart': res['oranlar']['saglamkart'],
    }

    if res['status'] == 'success':
        return taksit_data
    else:
        print(res)

def bin_sorgu(bin_code):
    merchant_id = '379607'
    merchant_key = b'xXWCLan3y1m97K4u'
    merchant_salt = '3yfMDbiraNXoG311'

    # Sorgulama yapılmak istenen karta ait kart numarasının ilk 6 veya 8 hanesi. Maksimum doğrulama için 8 hane kullanın.
    bin_number = bin_code

    # Bu kısımda herhangi bir değişiklik yapmanıza gerek yoktur.
    hash_str = bin_number + merchant_id + merchant_salt
    paytr_token = base64.b64encode(hmac.new(merchant_key, hash_str.encode(), hashlib.sha256).digest())

    params = {
        'merchant_id': merchant_id,
        'bin_number': bin_number,
        'paytr_token': paytr_token
    }

    result = requests.post('https://www.paytr.com/odeme/api/bin-detail', params)
    res = json.loads(result.text)

    if res['status'] == 'error':
        print('PAYTR BIN detail request error. Error: ' + res['err_msg'])
    elif res['status'] == 'failed':
        print('BIN tanımlı değil. (Örneğin bir yurtdışı kartı)')
    else:
        return res

def taksit_hesaplama(paymant_amount, vade, faiz):
    P = float(paymant_amount)
    R = float(faiz) / 100
    N = int(vade)
    T = N/12

    M = (P*(1+R*T)) / N
    toplam_odeme = M * N
    return toplam_odeme







