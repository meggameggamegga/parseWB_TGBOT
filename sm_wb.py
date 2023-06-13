import time
from selenium import webdriver
from selenium.common import NoSuchElementException
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By


class ParseSelWB:
    def __init__(self, label: str, article: int):
        self.label = label
        self.article = article
        self.page = 1

    def __set_up(self):
        path = r'C:\Users\роман\PycharmProjects\scrapping_prac\chromedriver\chromedriver.exe'
        options = Options()
        #options.add_argument('--headless')
        services = Service(executable_path=path)
        self.driver = webdriver.Chrome(service=services, options=options)

    def __get_url(self):
        self.driver.get(f'https://www.wildberries.ru/catalog/0/search.aspx?page=1&sort=popular&search={self.label}')
        self.driver.refresh()
        time.sleep(5)

    def __scroll_to_bottom(self):
        while True:
            self.driver.execute_script('window.scrollTo(0, document.body.scrollHeight);')
            if self.__get_place():
                self.__turn_off()
                break
            time.sleep(0.3)
            try:
                button = self.driver.find_element(By.CLASS_NAME, 'pagination-next.pagination__next.j-next-page')
                self.driver.execute_script("arguments[0].click();", button)
                self.page+=1
            except NoSuchElementException:
                break


    def __get_place(self):
        place = 0
        block_elements = self.driver.find_elements(By.CLASS_NAME, 'product-card.product-card--hoverable.j-card-item')
        for element in block_elements:
            place += 1
            article = element.get_attribute('data-nm-id')
            if str(self.article) == article:
                print(f"Местоположение: {place},Страница {self.page}")
                return place
        return None

    def __get_other_info(self):
        self.__set_up()
        self.driver.get(f'https://www.wildberries.ru/catalog/{self.article}/detail.aspx')
        time.sleep(2)
        price = self.driver.find_element(By.CLASS_NAME,'price-block__final-price').text
        reviews = self.driver.find_element(By.CLASS_NAME,'product-review__count-review').text
        element = self.driver.find_element(By.CSS_SELECTOR, '[data-link*="productCardOrderCount"]')
        return price,reviews,element

    def __turn_off(self):
        self.driver.close()
        self.driver.quit()

    def parse(self):
        #self.__set_up()
        #self.__get_url()
        #self.__scroll_to_bottom()
        self.__get_other_info()


if __name__ == '__main__':
    ParseSelWB(label='Лейка садовая', article=152348929).parse()
