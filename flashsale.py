from selenium.webdriver import Chrome
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import requests,json
from requests import Session
from bs4 import BeautifulSoup as bs
import calendar, time
from datetime import datetime
import datetime as dt
# import csv,pypyodbc
import time,pickle
from time import strftime
from time import gmtime
from selenium.webdriver.chrome.options import Options  
import pyautogui  

driver = Chrome()
headers = {
    'accept': 'application/json',
    'accept-encoding': 'gzip, deflate, br',
    'accept-language': 'en-US,en;q=0.9',
    'content-length': '196',
    'content-type': 'application/json',
    'cookie': 'csrftoken=VYDwnRuEuxVtHJ5JfVHVJmT6szkurtjl; welcomePkgShown=true; AMP_TOKEN=%24NOT_FOUND; SPC_T_ID="0+imP8SdM05h0SrImE01UZT2XeIuGJvNUI0Zj+MvFtrsafXD+bXyg7hzfsUalwFmAEN5KwF/PqAJ8pGjxzI0S6Qgxsso8vKRIbI2NvPR/Sc="; SPC_T_IV="t3ZZtZB6Ua51YnzjjjNdIw=="; welcomePkgShown=true; SPC_IA=1; SPC_EC=RDeftO8r+hk97QrKe/ptk/1DKGjUnnVsc1umuS9BixcTPkkV86KhrmdI52dIghkyQJ+z6rAFeKcycNB34m2P8SJLX6ufTtILn6WLBInZ3vvKed6x6O1WMD5XLZQ/swci; SPC_U=32718758; SPC_CLIENTID=Q0xqMEFJYWg3VjZYjlyygjrxmkgwznpe; G_ENABLED_IDPS=google; _gcl_au=1.1.1273437804.1609401967; csrftoken=pcVLPYsOxQyU6HzwTpO6LzagTi9GBR7D; _gid=GA1.3.1317725863.1609401969; SPC_SI=mall.1RCe3uoYDem9vzP4GYYlbNR6vJiYbtAD; REC_T_ID=133f7a74-4b3f-11eb-bbbb-ccbbfe1557c2; SPC_F=CLj0AIah7V6XwEhw9pBoksnXlwNcqcwp; _fbp=fb.2.1609401967196.1521933535; _ga=GA1.1.1390037977.1609401969; _dc_gtm_UA-61904553-8=1; _ga_SW6D8G0HXK=GS1.1.1609401968.1.1.1609402807.0; SPC_R_T_ID="WDx1XhbR9ZRKJlb6mM6oUoHrHXjLXX7ysfn5paY/pQBiCGyWXhpKXg7n9eV6gwT7hWKxy47YfuDDvEwxi46qkMv+cuEExtF7NfZ6ReNPV7w="; SPC_T_IV="VE9HsFpbYKzBosuaKAqqDw=="; SPC_R_T_IV="VE9HsFpbYKzBosuaKAqqDw=="; SPC_T_ID="WDx1XhbR9ZRKJlb6mM6oUoHrHXjLXX7ysfn5paY/pQBiCGyWXhpKXg7n9eV6gwT7hWKxy47YfuDDvEwxi46qkMv+cuEExtF7NfZ6ReNPV7w="',
    'if-none-match-': '55b03-15b2442c994f97258346e997f8d1ba08',
    'origin': 'https://shopee.co.id',
    'referer': 'https://shopee.co.id/HEADSET-HANDSFREE-U19-MACARON-MATE-COLOR-HIFI-EXTRA-BASS-i.125865704.5438746840',
    'sec-fetch-dest': 'empty',
    'sec-fetch-mode': 'cors',
    'sec-fetch-site': 'same-origin',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.88 Safari/537.36',
    'x-api-source': 'pc',
    'x-csrftoken': 'VYDwnRuEuxVtHJ5JfVHVJmT6szkurtjl',
    'x-requested-with': 'XMLHttpRequest',
    'x-shopee-language': 'id'
}


def login():
    url = "https://shopee.co.id/buyer/login?next=https%3A%2F%2Fshopee.co.id%2F"
    driver.get(url)
    time.sleep(40)
    pickle.dump(driver.get_cookies() , open("shopee_cookies.pkl","wb"))
    print("save cookies success")
    
def load():
    url = "https://shopee.co.id/"
    driver.get(url)
    cookies = pickle.load(open("shopee_cookies.pkl", "rb"))
    for cookie in cookies:
        driver.add_cookie(cookie)
    print("load success")
    driver.get(url)

def payment(data,now):
    del data['shipping_orders'][0]['logistics']
    del data['payment_channel_info']
    del data['shoporders'][0]['logistics']
    with Session() as s:
        url = "https://shopee.co.id/api/v2/checkout/place_order"
        payload = {"status":200,"headers":{}} 
        payload = payload | data
        try:
            payload['timestamp'] = 1609347601
        except:
            pass

        print("before Payment ",datetime.now().strftime("%H:%M:%S.%f"))
        r = s.post(url,json=payload, headers=headers)
        try:
            now = r.json()['timestamp']
            print("Time after Paymet ",datetime.now().strftime("%H:%M:%S.%f"))
            print("Payment Succes at", datetime.fromtimestamp(now).strftime("%H:%M:%S"))
            driver.get(r.json()['redirect_url'])
            WebDriverWait(driver, 5).until(EC.presence_of_element_located((By.XPATH,'//*[@id="pay-button"]'))).click()
            driver.find_element_by_xpath('//*[@id="pin-popup"]/div[1]/div[4]/div[2]').click()
            time.sleep(3)
            driver.find_element_by_xpath('//*[@id="pin-popup"]/div[1]/div[3]/div[1]').click()
            pyautogui.write('250417', interval=0.5)
            time.sleep(0.7)
            driver.find_element_by_xpath('//*[@id="pin-popup"]/div[1]/div[4]/div[2]').click()
        except:
            print("pembayaran gagal")


def cekout(shopid,itemid,modelid,groupid,now):
    headers["referer"] = "https://shopee.co.id/checkout"
    bca = {"channel_id": 8005200,"channel_item_option_info": {"option_info": "89052001"},"version": 2}
    shopeepay = {"channel_id": 8001400,"channel_item_option_info": {},"version": 2}
    with Session() as s:
        url = "https://shopee.co.id/api/v2/checkout/get"
        payload = '{"timestamp":1609347600,"shoporders":[{"shop":{"shopid":222593200},"items":[{"itemid":5338734798,"modelid":50036979633,"add_on_deal_id":0,"is_add_on_sub_item":false,"item_group_id":0,"quantity":1}],"logistics":{"recommended_channelids":null},"buyer_address_data":{"tax_address":"","error_status":"","address_type":0,"addressid":3752005},"selected_logistic_channelid":80015,"shipping_id":1,"selected_preferred_delivery_time_option_id":0,"selected_preferred_delivery_time_slot_id":null}],"selected_payment_channel_data":{"channel_id":8001400,"channel_item_option_info":{},"version":2},"promotion_data":{"use_coins":false,"free_shipping_voucher_info":{"free_shipping_voucher_id":0,"disabled_reason":null,"free_shipping_voucher_code":""},"platform_vouchers":[],"shop_vouchers":[],"check_shop_voucher_entrances":true,"auto_apply_shop_voucher":false},"device_info":{"device_id":"","device_fingerprint":"","tongdun_blackbox":"","buyer_payment_info":{}},"cart_type":0,"client_id":0,"tax_info":{"tax_id":""},"dropshipping_info":{"phone_number":"","enabled":false,"name":""},"shipping_orders":[{"sync":true,"logistics":{"recommended_channelids":null},"buyer_address_data":{"tax_address":"","error_status":"","address_type":0,"addressid":3752005},"selected_logistic_channelid":80015,"shipping_id":1,"shoporder_indexes":[0],"buyer_ic_number":"","selected_preferred_delivery_time_option_id":0,"selected_preferred_delivery_time_slot_id":null}],"order_update_info":{}}'
        payload = json.loads(payload)
        payload['shoporders'][0]['shop']['shopid'] = shopid
        payload['shoporders'][0]['items'][0]['itemid'] = itemid
        payload['shoporders'][0]['items'][0]['modelid'] = modelid
        # payload['shoporders'][0]['items'][0]['add_on_deal_id'] = 632227
        payload['shoporders'][0]['items'][0]['item_group_id'] = groupid
        payload['timestamp'] = now
        payload['shoporders'][0]['selected_logistic_channelid'] = 80088 # 80015 #80005 #
        payload['shipping_orders'][0]['selected_logistic_channelid'] = 80088 # 80005 #80015
        print("before cekout ",datetime.now().strftime("%H:%M:%S.%f"))
        r = s.post(url,json=payload, headers=headers)
        try:
            if r.json()['can_checkout'] == True:
                print("Payment with shopeepay")
                print("after cekout ",datetime.now().strftime("%H:%M:%S.%f"))
                payment(r.json(),now)
            
            elif r.json()['can_checkout'] == False:
                print("Shopeepay Failed Change payment method to BCA")
                payload['selected_payment_channel_data'] = bca
                r = s.post(url,json=payload, headers=headers)
                payment(r.json(),now)
        except:
            print("cekout gagal")

def add_to_chart(shopid,itemid,modelid,product_url,now):
    headers["referer"] = product_url
    with Session() as s:
        url = "https://shopee.co.id/api/v2/cart/add_to_cart"
        payload = {"quantity":1,"checkout":True,"update_checkout_only":False,"donot_add_quantity":False,"source":"{\"refer_urls\":[]}","client_source":1,"shopid":shopid,"itemid":itemid,"modelid":modelid}
        print("before add cart ",datetime.now().strftime("%H:%M:%S.%f"))
        r = s.post(url,json=payload, headers=headers)
        try:
            groupid = r.json()['data']['cart_item']['item_group_id']
        except:
            groupid = ""
        print("after add cart ",datetime.now().strftime("%H:%M:%S.%f"))
        cekout(shopid,itemid,modelid,groupid,now)

def get_data(now):
    product_url = "https://shopee.co.id/product/12802752/4457933273"
    newurl = product_url.split("/")
    shopid = int(newurl[-2])
    itemid = int(newurl[-1])
    url=(f"https://shopee.co.id/api/v4/item/get?itemid={itemid}&shopid={shopid}")
    with Session() as s:
        r = s.get(url)
        data = r.json()
        modelid = data["data"]["models"][0]["modelid"]
        a = True
        # print(data)
        while a:
            gmt = now-int(datetime.now())
            print(gmt)
            # timeleft = "time left: {}".format(strftime("%H:%M:%S.%f", gmt))
            print(datetime.now().strftime("%H:%M:%S.%f"), gmt)
            if int(time.time()*1000) >= (now*1000):
                start = int(time.time())
                print("start",start)
                add_to_chart(shopid,itemid,modelid,product_url,now)
                a = False


# login()
load()
now = 1609347600 #local 00.00
now = 1809434000 #GMT 00.00
get_data(now)


