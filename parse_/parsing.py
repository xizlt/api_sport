import json
import os
import django
import requests
from bs4 import BeautifulSoup as bs
from django.conf.global_settings import MEDIA_ROOT

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "apiSport.settings")
django.setup()
# from apiSport.settings import MEDIA_ROOT
from shop.models import Description, Product, Specification, Category, Brand

HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/81.0.4044.138 Safari/537.36 OPR/68.0.3618.125',
    'accept': '*/*',
}
HOST = 'https://www.sportmaster.ru'


def get_html(url, params=None):
    return requests.get(url, headers=HEADERS, params=params)


def get_content(html):
    soup = bs(html, 'html.parser')
    items = soup.find_all('div', class_='sm-category__item')
    products = []

    for item in items:
        specification = {
            'general': {},
            'feature': {},
            'composition': {},
            'addition': {}
        }
        description = {}

        link = HOST + item.find('a').get('href').strip()
        single = bs(get_html(link).text, 'html.parser')

        desc = single.find('div', class_='sm-goods__description-text', attrs={'itemprop': 'description'})
        if desc:
            texts = desc.find_all('li')
            for n in range(0, len(texts)):
                benefits = texts[n].find_all('b')
                for benefit in benefits:
                    k = benefit.get_text().capitalize()
                    description.update({k: texts[n].get_text()[len(k):].strip()})

        spes = single.find('table', class_='sm-goods_tabs_characteristix')
        if spes:
            specification_html = spes.find_all('tbody', class_='sm-characteristics_block')
            for j in range(0, len(specification_html)):
                tr = specification_html[j].find_all('tr', class_='characteristics_values')
                for i in range(0, len(tr)):
                    td = tr[i].find_all('td')
                    if j == 0:
                        upd = 'general'
                    elif j == 1:
                        upd = 'feature'
                    elif j == 2:
                        upd = 'composition'
                    else:
                        upd = 'addition'
                    specification[upd].update({td[0].get_text().lower(): td[1].get_text()})

        price_old = item.find('div', class_='smTileOldpriceBlock')
        if price_old:
            price_old = int(price_old.findNext('sm-amount').get_text(strip=True).replace(',', ''))
        else:
            price_old = 0

        rating = item.find('span', class_='sm-category__item-rating-stars')
        if rating:
            rating = float(rating.get('title'))
        else:
            rating = None

        products.append({
            'title': item.find('h2').get_text(strip=True),
            'brand': single.find('div', class_='sm-goods_main_logo-holder').findNext('img').get('alt'),
            'price': int(item.find('div', class_='sm-category__item-actual-price tr').
                         findNext('span').
                         get_text(strip=True).
                         replace(',', '')),
            'price_old': price_old,
            'img': item.find('img').get('src'),
            'rating': rating,
            'link': link,
            'description': description,
            'specification': specification
        })
    return products


def get_pages_count(html):
    soup = bs(html, 'html.parser')
    pages = soup.find_all('a', class_='ajax-facet-value')
    if pages:
        pages = int(pages[-2].get_text())
    else:
        pages = 1
    return pages


def save_file(items, name):
    from django.conf.global_settings import MEDIA_ROOT
    with open(MEDIA_ROOT + f'/data/{name}.json', 'w', encoding='utf-8') as f:
        for item in items:
            json.dump(item, f, ensure_ascii=False)


# def get_description(product):
#     description = set()
#     pr = product['description'].keys()
#     for i in pr:
#         description.add(i.capitalize())
#     return description
#
#
# def get_specification(product):
#     specification = set()
#     pr = product['specification']
#     for k, v in pr.items():
#         for d in pr[k].keys():
#             specification.add(d.capitalize())
#     return specification


# def write_description(products):
#     descriptions = list(get_description(products))
#     db_descriptions = Description.objects.values_list('name', flat=True)
#     for description in descriptions:
#         if description not in db_descriptions:
#             Description.objects.create(name=description)
#
#
# def write_specification(products):
#     specifications = get_specification(products)
#     db_specifications = Specification.objects.values_list('name', flat=True)
#     for specification in specifications:
#         if specification not in db_specifications:
#             Specification.objects.create(name=specification)


def get_file(url):
    r = requests.get(url, stream=True)
    return r


def get_name_file(url, category):
    name = url.split('/')[-1]
    # folder = f'products/{date.today().year}/{date.today().month}/{date.today().day}'
    folder = f'products/{category["slug"]}'
    if not os.path.exists(MEDIA_ROOT + folder):
        os.makedirs(MEDIA_ROOT + folder)
    return folder + '/' + name


def save_image(name, src):
    with open(MEDIA_ROOT + name, 'wb') as f:
        for chunk in src.iter_content(8192):
            f.write(chunk)


def write_product(products, category):
    cat, st = Category.objects.get_or_create(name=category.capitalize())
    for product in products:
        brn, st = Brand.objects.get_or_create(name=product['brand'])

        pr = product['description']
        sp = product['specification']
        # name_img = get_name_file(product['img'], category)
        # file_img = get_file(product['img'])
        # save_image(name_img, file_img)
        t = Product.objects.update_or_create(
            name=product['title'],
            brand=brn,
            price=product['price'],
            old_price=product['price_old'],
            # image=name_img,
            image=product['img'],
            rating=product['rating'],
            category_id=cat.id,
            link=product['link'],
        )
        for k, v in pr.items():
            description = Description.objects.get_or_create(name=k, benefit=v)
            t[0].description.add(description[0].id)
            t[0].save()

        for item in sp.values():
            for k, v in item.items():
                specification = Specification.objects.get_or_create(name=k.strip(), benefit=v.strip())
                t[0].specification.add(specification[0].id)
                t[0].save()


def parse(url, category):
    html = get_html(url)
    if html.status_code == 200:
        products = []
        pages = get_pages_count(html.text)
        for page in range(1, pages):
            print(f'Обработано {page} из {pages}')
            html = get_html(url, params={'page': page})
            products.extend(get_content(html.text))
            print(f'Принято {len(products)}')
        write_product(products, category)
        # save_file(products, name=category['slug'])
    else:
        print('Error')

