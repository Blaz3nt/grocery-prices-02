import json, requests, time, random
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException

browser = webdriver.Chrome()
base_url = 'https://www.woolworths.com.au/shop/search/products?searchTerm='

def execute_script(filename):
    f = open(filename, 'r')
    json_string = browser.execute_script(f.read())
    f.close()
    json_data = json.loads(json_string)
    return json_data

def save_json(filename, data):
    f = open(filename, 'w+')
    json_string = json.dumps(data, indent=4, sort_keys=True)
    f.write(json_string)
    f.close()

def scrape_products(search_terms, get_nutrition_info = False, save_images = False, max_num_pages = float('inf')):
    data = {}
    items = set()

    for term in search_terms:
        page_number = 1
        url = base_url + term + '&pageNumber=' + str(page_number)

        data[term] = []

        while url != 'NONE':
            if page_number > max_num_pages:
                break

            browser.get(url)

            try:
                timeout = 10
                WebDriverWait(browser, timeout).until(EC.presence_of_element_located((By.CLASS_NAME, 'shelfProductTile-descriptionLink')))
            except TimeoutException:
                pass

            page_data = execute_script('../Coles/scrape_products.js')

            if save_images or get_nutrition_info:
                for product in page_data['products']:
                    if save_images:
                        # image saving logic here
                        pass
                    if get_nutrition_info:
                        # nutrition info scraping logic here
                        pass

            for product in page_data['products']:
                if product['name'] not in items:
                    items.add(product['name'])
                    product['searchTerm'] = term
                    data[term].append(product)

            url = page_data['nextPage']
            page_number += 1
            time.sleep(random.randint(1,5))

        filename = '../Datasets/Woolworths/' + term.replace('/', '-') + '.json'
        save_json(filename, data[term])

if __name__ == '__main__':
    search_terms = ['milk']  # Example search terms
    scrape_products(search_terms)
