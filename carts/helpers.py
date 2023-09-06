import base64
import hashlib
import hmac
import html
import json
import random
import requests

from django.shortcuts import render, HttpResponse
from django.views.decorators.csrf import csrf_exempt

from ecommerce import settings


def paytr_api(email, payment_amount, full_name, address, mobile, item, ip):
    # API Entegrasyon Bilgileri - Mağaza paneline giriş yaparak BİLGİ sayfasından alabilirsiniz.
    merchant_id = '379607'
    merchant_key = b'xXWCLan3y1m97K4u'
    merchant_salt = b'3yfMDbiraNXoG311'

    merchant_ok_url = 'http://site-ismi/basarili'
    merchant_fail_url = 'http://site-ismi/basarisiz'

    user_basket = html.unescape(json.dumps([item]))

    merchant_oid = 'OS' + random.randint(1, 9999999).__str__()
    test_mode = '0'
    debug_on = '1'

    # 3d'siz işlem
    non_3d = '0'

    # Ödeme süreci dil seçeneği tr veya en
    client_lang = 'tr'

    # non3d işlemde, başarısız işlemi test etmek için 1 gönderilir (test_mode ve non_3d değerleri 1 ise dikkate alınır!)
    non3d_test_failed = '0'
    user_ip = ''
    email = 'testnon3d@paytr.com'

    # 100.99 TL ödeme
    payment_amount = "100.99"
    currency = 'TL'
    payment_type = 'card'

    user_name = 'Paytr Test'
    user_address = 'test test test'
    user_phone = '05555555555'

    # Alabileceği değerler; advantage, axess, combo, bonus, cardfinans, maximum, paraf, world, saglamkart
    card_type = 'bonus'
    installment_count = '5'

    hash_str = merchant_id + user_ip + merchant_oid + email + payment_amount + payment_type + installment_count + currency + test_mode + non_3d
    paytr_token = base64.b64encode(hmac.new(merchant_key, hash_str.encode() + merchant_salt, hashlib.sha256).digest())

    context = {
        'merchant_id': merchant_id,
        'user_ip': user_ip,
        'merchant_oid': merchant_oid,
        'email': email,
        'payment_type': payment_type,
        'payment_amount': payment_amount,
        'currency': currency,
        'test_mode': test_mode,
        'non_3d': non_3d,
        'merchant_ok_url': merchant_ok_url,
        'merchant_fail_url': merchant_fail_url,
        'user_name': user_name,
        'user_address': user_address,
        'user_phone': user_phone,
        'user_basket': user_basket,
        'debug_on': debug_on,
        'client_lang': client_lang,
        'paytr_token': paytr_token.decode(),
        'non3d_test_failed': non3d_test_failed,
        'installment_count': installment_count,
        'card_type': card_type
    }


def paytr_iframe(email, payment_amount, merchant_oid, fullname, address, mobile, item, ip, installment_option):
    # API Entegrasyon Bilgileri - Mağaza paneline giriş yaparak BİLGİ sayfasından alabilirsiniz.
    merchant_id = '379607'
    merchant_key = b'xXWCLan3y1m97K4u'
    merchant_salt = b'3yfMDbiraNXoG311'

    email = email

    payment_amount = int(payment_amount * 100)

    merchant_oid = merchant_oid

    user_name = fullname

    user_address = address

    user_phone = mobile

    if settings.DEBUG == True:
        merchant_ok_url = f'http://127.0.0.1:8000/odeme-tamamlandi/siparis_no={str(merchant_oid)}'
    else:
        merchant_ok_url = f'https://www.tredyshop.com/odeme-tamamlandi/siparis_no={str(merchant_oid)}'

    merchant_fail_url = 'https://www.tredyshop.com/odeme_basarisiz'

    user_basket = base64.b64encode(json.dumps(item).encode())

    if settings.DEBUG == True:
        user_ip = '213.238.183.81'
    else:
        user_ip = ip

    timeout_limit = 30

    debug_on = 1

    test_mode = 1

    if installment_option == True:
        no_installment = 0
    else:
        no_installment = 1

    max_installment = 0

    currency = 'TL'

    # Bu kısımda herhangi bir değişiklik yapmanıza gerek yoktur.
    hash_str = merchant_id + user_ip + merchant_oid + email + str(payment_amount) + user_basket.decode() + str(no_installment) + str(max_installment) + currency + str(test_mode)
    paytr_token = base64.b64encode(hmac.new(merchant_key, hash_str.encode() + merchant_salt, hashlib.sha256).digest())

    params = {
        'merchant_id': merchant_id,
        'user_ip': user_ip,
        'merchant_oid': merchant_oid,
        'email': email,
        'payment_amount': payment_amount,
        'paytr_token': paytr_token,
        'user_basket': user_basket,
        'debug_on': debug_on,
        'no_installment': no_installment,
        'max_installment': max_installment,
        'user_name': user_name,
        'user_address': user_address,
        'user_phone': user_phone,
        'merchant_ok_url': merchant_ok_url,
        'merchant_fail_url': merchant_fail_url,
        'timeout_limit': timeout_limit,
        'currency': currency,
        'test_mode': test_mode
    }

    result = requests.post('https://www.paytr.com/odeme/api/get-token', params)
    res = json.loads(result.text)

    if res['status'] == 'success':
        return res['token']

    else:
        return result.text


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