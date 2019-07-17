from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
from cacheout import Cache

cache = Cache()

@cache.memoize(ttl=300)
def get_currency_price():
    result = {}
    options = webdriver.ChromeOptions()
    options.add_argument('--headless')
    browser = webdriver.Chrome(options=options)
    browser.get("https://www.feixiaohao.com/")
    tr_list = browser.find_elements_by_css_selector("table tr")[1:]
    for tr in tr_list:
        try:
            name = tr.find_element_by_css_selector(".name").text
            price = tr.find_element_by_css_selector("td:nth-child(4)").text
            result[name] = price
        except NoSuchElementException as e:
            print(e, tr)
    return result

if __name__ == "__main__":
    r = get_currency_price()
