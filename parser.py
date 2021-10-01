import requests
import json
import datetime

URL = 'https://roscarservis.ru/catalog/legkovye/?form_id=catalog_filter_form&filter_mode=params&sort=asc&filter_type=tires&arCatalogFilter_458_1500340406=Y&set_filter=Y&PAGEN_1=1'

HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.159 YaBrowser/21.8.3.614 Yowser/2.5 Safari/537.36',
    'Accept': 'application/json, text/javascript, */*; q=0.01',
    'X-Is-Ajax-Request': 'X-Is-Ajax-Request',
    'X-Requested-With': 'XMLHttpRequest'
}

def get_data():
    start_time = datetime.datetime.now()
    r = requests.get(url = URL, headers = HEADERS)

    with open('index.html', 'w', encoding = 'utf-8') as file:
        file.write(r.text)

    with open ('r.json', 'w', encoding = 'utf-8') as file:
        json.dump(r.json(), file, indent = 4, ensure_ascii = False)

    page_count = r.json()['pageCount']
    
    data_list = []

    for page in range(1, page_count + 1):
        url = f'https://roscarservis.ru/catalog/legkovye/?form_id=catalog_filter_form&filter_mode=params&sort=asc&filter_type=tires&arCatalogFilter_458_1500340406=Y&set_filter=Y&PAGEN_1={page}'

        r = requests.get(url = url, headers = HEADERS)
        data = r.json()
        items = data['items']

        possible_stores = ['discountStores', 'fortochkiStores', 'commonStores']

        for item in items:
            total_amount = 0

            item_name = item['name']
            item_price = item['price']
            item_img = f'https://roscarservis.ru{item["imgSrc"]}'
            item_url = f'https://roscarservis.ru{item["url"]}'

            stores = []
            for i in possible_stores:
                if i in item:
                    if item[i] is None or len(item[i]) < 1:
                        continue
                    else:
                        for store in item[i]:
                            store_name = store['STORE_NAME']
                            store_price = store['PRICE']
                            store_amount = store['AMOUNT']
                            total_amount += int(store['AMOUNT'])

                            stores.append(
                                {
                                    'store_name': store_name,
                                    'store_price': store_price,
                                    'store_amount': store_amount
                                }
                            )

            data_list.append(
                {
                    'name': item_name,
                    'price': item_price,
                    'url': item_url,
                    'img_link': item_img,
                    'stores': stores,
                    'total_amount': total_amount,

                }
            )

        print(f'The page_{page}/{page_count} has been processed')

    cur_time = datetime.datetime.now().strftime('%d_%m_%Y_%H_%M')

    with open(f'data_{cur_time}.json', 'a', encoding = 'utf-8') as file:
        json.dump(data_list, file, indent = 4, ensure_ascii = False)

    #Time spent on the program
    different_time = datetime.datetime.now() - start_time
    print(different_time)

def main():
    get_data()

if __name__ == '__main__':
     main()