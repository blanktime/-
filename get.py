from bs4.element import Tag
import requests
import os
import re
import random
import time
from threading import Thread
import urllib3
from retrying import retry

requests.packages.urllib3.disable_warnings()

headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.97 Safari/537.36', 'Connection': 'close'}
requests.adapters.DEFAULT_RETRIES = 5


class GetList(object):
    def __init__(self, traits_path, units_path, rates_path, tag, processes=4):
        self.traits_path = traits_path
        self.units_path = units_path
        self.rates_path = rates_path
        self.unit_index = 0
        self.tag = tag
        self.processes = processes

    def get_traits_list(self):
        if not os.path.exists(self.traits_path):
            os.makedirs(self.traits_path)
        traits_list = self.tag.find(name='td', attrs={'class': 'traits-list'})
        trait_imgs = traits_list.find_all('img')
        self.save_imgs(trait_imgs, self.traits_path, 'trait_')
        print("save traits to %s successfully" % self.traits_path)
        print("------------------------------------------------")

    def get_units_list(self):
        self.unit_index = 0
        if not os.path.exists(self.units_path):
            os.makedirs(self.units_path)
        units_list = self.tag.find(name='div', attrs={'class': 'units'})
        for unit in units_list:
            if isinstance(unit, Tag):
                self.unit_index += 1
                unit_path = os.path.join(self.units_path, "unit_{}".format(self.unit_index))
                if not os.path.exists(unit_path):
                    os.makedirs(unit_path)
                star_imgs = unit.find('img')
                unit_div = unit.find(name='div')
                unit_imgs = unit_div.find('img')
                items = unit.find(name='ul', attrs={'class': 'items'})
                item_imgs = items.find_all('img')

                self.save_imgs(star_imgs, unit_path, 'star_')
                self.save_imgs(unit_imgs, unit_path, 'unit_')
                self.save_imgs(item_imgs, unit_path, 'item_')
        print("save units to %s successfully" % self.units_path)
        print("------------------------------------------------")

    def save_imgs(self, imgs, save_path, pre_name):
        if isinstance(imgs, Tag):
            self.download_imgs(imgs, save_path, pre_name)
        else:
            threads = []
            for img in imgs:
                threads.append(Thread(target=self.download_imgs, args=(img, save_path, pre_name,)))
            for thread in threads:
                thread.start()
            for thread in threads:
                thread.join()

    @retry(stop_max_attempt_number=10, wait_fixed=5000)
    def download_imgs(self, img, save_path, pre_name):
        t = random.uniform(1, 3)
        time.sleep(t)
        url = "https:" + img['src']
        image_name = url.split('/')[-1]
        print("downloading %s%s" % (pre_name, image_name))
        try:
            r = requests.get(url, stream=True, headers=headers, verify=False, timeout=(5, 5))

        except urllib3.exceptions.MaxRetryError:
            t = random.uniform(5, 10)
            s = requests.session()
            s.keep_alive = False
            time.sleep(t)
            r = requests.get(url, stream=True, headers=headers, verify=False, timeout=(5, 5))

        except requests.exceptions.Timeout:
            global NETWORK_STATUS
            NETWORK_STATUS = False  # 请求超时改变状态
            if NETWORK_STATUS == False:
                for i in range(1, 10):
                    try:
                        print("请求下载%s%s超时，正在进行第%s次重试" % (pre_name, image_name, i))
                        r = requests.get(url, stream=True, headers=headers, verify=False, timeout=(5, 5))
                        if r.status_code == 200:
                            print("重新下载%s%s成功" % (pre_name, image_name,))
                            NETWORK_STATUS = True
                            break
                    except:
                        pass

        path = os.path.join(save_path, pre_name+image_name)
        with open(path, 'wb') as f:
            for chunk in r.iter_content(chunk_size=128):
                f.write(chunk)

    def get_rate(self):
        if not os.path.exists(self.rates_path):
            os.makedirs(self.rates_path)

        win_rate = self.tag.find(name='td', attrs={'class': 'winrate'})
        win_rate = win_rate.contents[0].string.replace('\n', '').replace(' ', '')
        win_rate_path = os.path.join(self.rates_path, 'win_rate.txt')
        with open(win_rate_path, 'w') as t1:
            t1.write(win_rate)

        top_rate = self.tag.find(name='td', attrs={'class': 'toprate'})
        top_rate = str(top_rate.contents[0].string.replace('\n', '').replace(' ', ''))
        top_rate_path = os.path.join(self.rates_path, 'top4_rate.txt')
        with open(top_rate_path, 'w') as t2:
            t2.write(top_rate)

        avg_rates = self.tag.find(name='td', attrs={'class': 'avgrate'})
        avg_rate = str(avg_rates.find(name='span'))
        avg_rate = re.search('(?<=<span>#).*?(?=</span>)', avg_rate)
        avg_rate = avg_rate.group(0)
        avg_rate_path = os.path.join(self.rates_path, 'avg_rate.txt')
        with open(avg_rate_path, 'w') as t3:
            t3.write(avg_rate)

        print("save rate to %s successfully" % self.rates_path)
        print("------------------------------------------------")



