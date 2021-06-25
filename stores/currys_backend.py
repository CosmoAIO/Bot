import os
import time
import json
import random
import requests
import csv

from os import sys, path
from requests.models import Response
from tasks import TaskManager
from termcolor import colored
from datetime import datetime
from datetime import timedelta

# OOS: 10216240
# INSTOCK:10141295


class Currys():
    def __init__(self, task, proxies, i):
        self.task = task
        self.proxies = proxies

        self.task_id = f"Currys Task - {i}"
        self.pid = '10141295'
        self.delay = 0
        self.pay_method = task['method']
        self.account_email = task['account_email']
        self.account_password = task['account_password']

        # self.address_headers = {
        #     'Connection': 'keep-alive',
        #     'sec-ch-ua': '" Not A;Brand";v="99", "Chromium";v="90", "Google Chrome";v="90"',
        #     'sec-ch-ua-mobile': '?0',
        #     'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.212 Safari/537.36',
        #     'Content-Type': 'text/plain;charset=UTF-8',
        #     'Accept': '*/*',
        #     'Origin': 'https://www.currys.co.uk',
        #     'Sec-Fetch-Site': 'same-origin',
        #     'Sec-Fetch-Mode': 'cors',
        #     'Sec-Fetch-Dest': 'empty',
        #     'Referer': 'https://www.currys.co.uk/gbuk/cameras-and-camcorders/digital-cameras/compact-and-bridge-cameras/fujifilm-finepix-finepix-xp140-tough-compact-camera-graphite-10192499-pdt.html',
        #     'Accept-Language': 'en-US,en;q=0.9',
        # }
        self.address_headers = {
            'Connection': 'keep-alive',
            'sec-ch-ua': '" Not A;Brand";v="99", "Chromium";v="90", "Google Chrome";v="90"',
            'X-Requested-With': 'XMLHttpRequest',
            'sec-ch-ua-mobile': '?0',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.212 Safari/537.36',
            'Accept': '*/*',
            'Origin': 'https://www.currys.co.uk',
            'Sec-Fetch-Site': 'same-origin',
            'Sec-Fetch-Mode': 'cors',
            'Sec-Fetch-Dest': 'empty',
            'Referer': 'https://www.currys.co.uk/',
            'Accept-Language': 'en-US,en;q=0.9',
        }

    def tasks(self):
        self.build_proxy()
        with requests.Session() as self.session:
            self.monitor()
            self.login()
            self.atc()
            self.cart_checker()
            # self.location()
            self.slot()
            self.order()
            self.submit_payment()

    def error(self, text):
        print(text)
        return

    def build_proxy(self):
        self.proxy = None
        if self.proxies == [] or not self.proxies:
            return None
        self.px = random.choice(self.proxies)
        self.splitted = self.px.split(':')
        if len(self.splitted) == 2:
            self.proxy = 'http://{}'.format(self.px)
            return None

        elif len(self.splitted) == 4:
            self.proxy = 'http://{}:{}@{}:{}'.format(self.splitted[2], self.splitted[3], self.splitted[0], self.splitted[1])
            return None
        else:
            self.error('Invalid proxy: "{}", rotating'.format(self.px))
            return None

    def login(self):
        print("Logging in...")
        while True:
            url = "https://api.currys.co.uk/store/api/token"
            payload = {
                "customerEmail": self.account_email,
                "customerPassword": self.account_password
            }

            try:
                token = self.session.post(url, headers=self.address_headers, data=payload)
            except Exception as e:
                self.error(f"Exception adding token - {e}")
                continue

            if token.status_code == 401:
                self.error("Incorrect login details")
                time.sleep(self.delay)
                continue
            elif token.status_code == 500:
                self.error("Incorrect email")
                time.sleep(self.delay)
                continue
            elif token.status_code != 200:
                self.error(f"Error logging in - {token.status_code}")
                time.sleep(self.delay)
                continue
            else:
                print("Logged in")
                try:
                    self.bid = json.loads(token.text)['bid']
                    print(f"Receieved BID: {self.bid}")
                    return
                except Exception as e:
                    self.error(f"Error getting token - {e}")
                    continue

    def monitor(self):
        print("Fetching stock levels...")
        while True:
            # scrape/ monitor website for when item comes into stock
            # https://www.currys.co.uk/gbuk/product-{self.pid}-pdt.html
            instock = [0]
            url = f"https://api.currys.co.uk/smartphone/api/productsStock/{self.pid}"

            self.headers = {
                'sec-ch-ua': '" Not A;Brand";v="99", "Chromium";v="90", "Google Chrome";v="90"',
                'Referer': 'https://www.currys.co.uk/',
                'sec-ch-ua-mobile': '?0',
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.212 Safari/537.36',
            }

            try:
                response = self.session.get(url, headers=self.headers)
            except Exception as e:
                self.error(f"Error getting product - {e}")
                time.sleep(self.delay)
                continue

            if response.status_code == 404:
                self.error(f"Incorrect PID")
                time.sleep(self.delay)
                continue
            else:
                try:
                    stock = json.loads(response.text)['payload'][0]['quantityAvailable']
                except Exception as e:
                    self.error(f"Error loading stock levels - {e}")
                    time.sleep(self.delay)
                    continue

                if stock == 0:
                    self.error(f"Product OOS")
                    time.sleep(self.delay)
                    continue
                else:
                    return

    def atc(self):
        while True:

            url = "https://www.currys.co.uk/api/cart/addProduct"
            payload = "{\"fupid\":\""+f"{self.pid}"+"\",\"quantity\":1}"

            try:
                atc = self.session.post(url, headers=self.address_headers, data=payload)
            except Exception as e:
                self.error(f"Exception adding to cart - {e}")
                time.sleep(self.delay)
                continue

            if atc.status_code != 200:
                self.error("Error adding to cart")
                time.sleep(self.delay)
                continue
            else:
                print("Added to cart")
                return

    def cart_checker(self):
        while True:
            url = f"https://api.currys.co.uk/store/api/baskets/{self.bid}"
            headers = {
                'Connection': 'keep-alive',
                'sec-ch-ua': '" Not A;Brand";v="99", "Chromium";v="90", "Google Chrome";v="90"',
                'X-Requested-With': 'XMLHttpRequest',
                'sec-ch-ua-mobile': '?0',
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.212 Safari/537.36',
                'Accept': '*/*',
                'Origin': 'https://www.currys.co.uk',
                'Sec-Fetch-Site': 'same-site',
                'Sec-Fetch-Mode': 'cors',
                'Sec-Fetch-Dest': 'empty',
                'Referer': 'https://www.currys.co.uk/',
                'Accept-Language': 'en-US,en;q=0.9',
            }

            try:
                response = self.session.get(url, headers=self.headers)
            except Exception as e:
                self.error(f"Exception checking cart - {e}")
                continue

            try:
                item = json.loads(response.text)['payload']['products'][0]['title']
                print("Carted Items:")
                print(item)
            except Exception as e:
                error_code = json.loads(response.text)['error']['code']
                error_message = json.loads(response.text)['error']['message']
                print(f"Error code: {error_code}, Message: {error_message}")
                self.error(f"Error get carted item - {e}")
                continue

            try:
                self.type = json.loads(response.text)['payload']['consignments'][0]['id']['type']
                self.provider = self.type.replace('-', '_')+("_standard_delivery")
                print("Fetching provider...")
                return
            except Exception as e:
                print(f"Error fetching provider - {e}")
                continue

    def location(self):
        while True:
            url = f"https://api.currys.co.uk/store/api/baskets/{self.pid}/deliveryLocation"
            # payload = {
            #     "location": "E1 6AN",
            #     "latitude": 51.51885,
            #     "longitude": -0.07840
            # }
            payload = {
                "location": "E1 6AN"
            }
            try:
                location = self.session.put(url, headers=self.address_headers, data=payload)
                gg = json.loads(location.text)
                print("Entering location...")
                print(gg)
                return
            except Exception as e:
                self.error(f"Error entering location - {e}")
                time.sleep(self.delay)
                continue

    def slot(self):
        while True:
            date = str(datetime.now() + timedelta(days=2))[0:10]
            url = f"https://api.currys.co.uk/store/api/baskets/{self.pid}/consignments/small-box-home-delivery/deliverySlot"
            payload = {
                "provider": f"{self.provider}",
                "priceAmountWithVat": 0,
                "priceVatRate": 20,
                "priceCurrency": "GBP",
                "date": f"{date}",
                "timeSlot": "2DST"
            }
            headers = {
                'Connection': 'keep-alive',
                'sec-ch-ua': '" Not A;Brand";v="99", "Chromium";v="90", "Google Chrome";v="90"',
                'Accept': 'application/json',
                'X-Requested-With': 'XMLHttpRequest',
                'sec-ch-ua-mobile': '?0',
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.212 Safari/537.36',
                'Content-Type': 'application/json',
                'Origin': 'https://www.currys.co.uk',
                'Sec-Fetch-Site': 'same-site',
                'Sec-Fetch-Mode': 'cors',
                'Sec-Fetch-Dest': 'empty',
                'Referer': 'https://www.currys.co.uk/',
                'Accept-Language': 'en-US,en;q=0.9',
            }
            try:
                slot = self.session.put(url, headers=headers, data=payload)
                print("picking delivery slot...")
            except Exception as e:
                self.error(f"Exception picking delivery slot - {e}")
                time.sleep(self.delay)
                continue

            if slot.status_code != 200:
                self.error("Error picking delivery slot")
                time.sleep(self.delay)
                print(slot)
                continue
            else:
                return

    def order(self):
        while True:
            url = f"https://api.currys.co.uk/store/api/baskets/{self.pid}/orders"
            payload = {}
            headers = {
                'Connection': 'keep-alive',
                'sec-ch-ua': '" Not A;Brand";v="99", "Chromium";v="90", "Google Chrome";v="90"',
                'Accept': 'application/json',
                'X-Requested-With': 'XMLHttpRequest',
                'sec-ch-ua-mobile': '?0',
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.212 Safari/537.36',
                'Content-Type': 'application/json',
                'Origin': 'https://www.currys.co.uk',
                'Sec-Fetch-Site': 'same-site',
                'Sec-Fetch-Mode': 'cors',
                'Sec-Fetch-Dest': 'empty',
                'Referer': 'https://www.currys.co.uk/',
                'Accept-Language': 'en-US,en;q=0.9',
            }
            try:
                order = self.session.post(url, headers=headers, data=payload)
                print("Sending order")
                return
            except Exception as e:
                self.error(f"Exception sending order - {e}")
                time.sleep(self.delay)
                continue

            if order.status_code != 200:
                self.error("Error sending order")
                time.sleep(self.delay)
                print(order)
                return
            else:
                return

    def submit_payment(self):
        while True:
            url = f"https://api.currys.co.uk/store/api/baskets/{self.pid}/payments"
            payload = {
                "paymentMethodType": "paypal"
            }
            headers = {
                'Connection': 'keep-alive',
                'sec-ch-ua': '" Not A;Brand";v="99", "Chromium";v="90", "Google Chrome";v="90"',
                'Accept': 'application/json',
                'X-Requested-With': 'XMLHttpRequest',
                'sec-ch-ua-mobile': '?0',
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.212 Safari/537.36',
                'Content-Type': 'application/json',
                'Origin': 'https://www.currys.co.uk',
                'Sec-Fetch-Site': 'same-site',
                'Sec-Fetch-Mode': 'cors',
                'Sec-Fetch-Dest': 'empty',
                'Referer': 'https://www.currys.co.uk/',
                'Accept-Language': 'en-US,en;q=0.9',
            }
            try:
                payment = self.session.post(url, headers=headers, data=payload)
                print("Sending payment")
            except Exception as e:
                self.error(f"Exception sending payment - {e}")
                time.sleep(self.delay)
                continue

            if payment.status_code != 200:
                self.error("Error sending order")
                time.sleep(self.delay)
                print(payment)
                return
            else:
                jPayment = json.loads(payment.text)
                print(jPayment)
                return


def main():
    os.system("title CosmoAIO - Currys")

    # Load tasks
    taskManager = TaskManager("Footlocker/tasks.csv")
    taskManager.loadTasks()
    allTasks = taskManager.returnTasks()

    if len(allTasks) == 0:
        print(colored("No task loaded. Closing...", "red"))
        time.sleep(10)
        return "noTasks"
    else:
        # Load Proxies
        try:
            PROXIES = open('proxies.txt', 'r').read().splitlines()
            print(colored(f"Loaded {len(PROXIES)} proxies.", "green"))
        except:
            print(colored("Could not load proxies.", "red"))
            time.sleep(10)
            sys.exit()

    tasks = []
    i = 0

    # Gathers & starts tasks
    for userTask in allTasks:
        newTask = Currys(userTask, PROXIES, i).tasks()
        tasks.append(newTask)
        i += 1


if __name__ == "__main__":
    main()
