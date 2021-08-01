from datetime import datetime
from bs4 import BeautifulSoup
from bs4.element import Tag
import os
import shutil
from get import GetList
import requests
from threading import Thread, Lock

requests.packages.urllib3.disable_warnings()

url = 'https://lolchess.gg/statistics/meta'
headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/77.0.3865.90 Safari/537.36'}


i = 1
path = ''
a = 0
step=0

def work(tag,lock):
    global i
    global path
    global a
    global step
    if isinstance(tag, Tag):
        if tag['class'] == ['deck-name']:
            lock.acquire()
            a = 0
            lock.release()
            if 'class' in tag.attrs:
                name = tag.find(name='td', attrs={'class': "header-name"}).string.replace('\n', '').replace(' ', '')
                lock.acquire()
                path = os.path.join(os.path.abspath("."), "res", "top{:02d}_{}".format(i, name))
                i += 1
                lock.release()
                if not os.path.exists(path):
                    os.makedirs(path)
            step += 1

        else:
            lock.acquire()
            a += 1

            lock.release()
            traits_path = os.path.join(path, "{}".format(a), 'traits_list')
            units_path = os.path.join(path, "{}".format(a), 'units_list')
            rates_path = os.path.join(path, "{}".format(a), 'rates')

            getlist = GetList(traits_path, units_path, rates_path, tag)
            getlist.get_traits_list()
            getlist.get_rate()
            getlist.get_units_list()

            step += 1

def set_pbar(bar,max_num):
    while step<max_num:
        bar.setValue(step)

def main_spider(bar):
    if not os.path.exists('res'):
        os.makedirs('res')
    elif not os.listdir('res'):
        os.rmdir('res')
        os.makedirs('res')
    else:
        shutil.rmtree('res')
        os.makedirs('res')
    print('start read html at:', datetime.now())
    res = requests.get(url=url, stream=True, headers=headers)
    res.encoding = res.apparent_encoding
    soup = BeautifulSoup(res.text, 'html.parser')
    print('read html ok')
    tags = soup.find('tbody')

    MAX_TAG = 0
    for t in tags:
        if isinstance(t, Tag):
            MAX_TAG+=1
    bar.setMaximum(MAX_TAG)
    threads = []
    lock = Lock()
    for tag in tags:
        threads.append(Thread(target=work, args=(tag, lock)))
    threads.append(Thread(target=set_pbar, args=(bar, MAX_TAG)))
    # for thread in threads:
    #     thread.start()
    # for thread in threads:
    #     thread.join()
    return threads

if __name__ == '__main__':
    main_spider()

