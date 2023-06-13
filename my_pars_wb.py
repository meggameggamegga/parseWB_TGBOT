import csv
import json
import time

import requests
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By

path = r'C:\Users\роман\PycharmProjects\scrapping_prac\chromedriver\chromedriver.exe'
services = Service(executable_path=path)


class ParseWb:
    def __init__(self, label: str = None, pages: int = 1, article: int = None):
        self.label = label
        self.pages = pages
        self.data_save = []
        self.article = article

    def __get_url(self):
        for page in range(1, self.pages+1):
            responce = requests.get(
                url=f'https://search.wb.ru/exactmatch/ru/common/v4/search?TestGroup=no_test&TestID=no_test&appType=1&curr=rub&dest=-1257786&page={page}&query={self.label}&regions=80,38,4,64,83,33,68,70,69,30,86,75,40,1,66,110,22,31,48,71,114&resultset=catalog&sort=popular&spp=0&suppressSpellcheck=false')
            if not responce.json()['data']['products']:
                print('Кол-во страниц указано больше, чем есть')
                return False
            self.data_save.append(responce.json()['data'])
        self.__save_data()
        return True

    def __save_data(self):
        with open('wb_result.json', 'w', encoding='UTF-8') as file:
            json.dump(self.data_save, file, indent=4, ensure_ascii=False)

    def get_all_info(self):
        self.__get_url()
        items = self.open_data()
        for page in range(self.pages):
            for item in items[page]['products']:
                result = {
                    'id': item.get('id'),
                    'Название': item.get('name').replace('/', ''),
                    'Цена': item.get('salePriceU') / 100,
                    'Наличие': item.get('volume'),
                    'Бренд': item.get('brand'),
                    'Рейтинг': item.get('rating'),
                    'Отзывы': item.get('feedbacks')
                }
                print(result)
                self.data_save.append(result)
        return self.data_save

    def open_data(self):
        with open('wb_result.json', 'r', encoding='UTF-8') as file:
            items = json.load(file)
        return items



    def parse(self):
        self.__get_url()
        self.get_all_info()


if __name__ == '__main__':
    ParseWb(label='apple').parse()
