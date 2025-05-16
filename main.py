import json
import requests
from datetime import datetime


def get_free_games() -> dict:
    timestamp = datetime.timestamp(datetime.now())
    games = {'timestamp': timestamp, 'free_now': [], 'free_next': []}
    base_store_url = 'https://store.epicgames.com'
    api_url = 'https://store-site-backend-static.ak.epicgames.com/freeGamesPromotions?country=CN'
    resp = requests.get(api_url)
    for element in resp.json()['data']['Catalog']['searchStore']['elements']:
        if promotions := element['promotions']:
            game = {}
            game['title'] = element['title']
            if ("Mystery Game") in game['title']:
                continue
            game['images'] = element['keyImages']
            game['origin_price'] = element['price']['totalPrice']['originalPrice']
            game['discount_price'] = element['price']['totalPrice']['discountPrice']
            if game['origin_price'] and game['discount_price'] != 0:
                continue
            slug = element.get('productSlug')
            game['store_url'] = f"{base_store_url}/p/{slug}" if slug else base_store_url
            if offers := promotions.get('promotionalOffers'):
                game['start_date'] = offers[0]['promotionalOffers'][0]['startDate']
                game['end_date'] = offers[0]['promotionalOffers'][0]['endDate']
                games['free_now'].append(game)
            if offers := promotions.get('upcomingPromotionalOffers'):
                game['start_date'] = offers[0]['promotionalOffers'][0]['startDate']
                game['end_date'] = offers[0]['promotionalOffers'][0]['endDate']
                games['free_next'].append(game)
    return games


def generate_json(games: dict, filename: str):
    with open(filename, 'w', encoding='utf-8') as f:
        json.dump(games, f, ensure_ascii=False, indent=2)


def generate_markdown(games: dict, filename: str):
    images = {}
    data = games['free_now'] + games['free_next']
    for game in data:
        for image in game['images']:
            if image['type'] in ['OfferImageWide', 'VaultClosed', 'DieselStoreFrontWide']:
                images[game['title']] = image['url']
                break

    content = '''# Epic 每周限免

- ## 本周限免
'''

    for game in games['free_now']:
        content += f'''
  - ### [{game['title']}]({game['store_url']} "{game['title']}")

    原价: {game['origin_price']}

    购买链接: [{game['store_url']}]({game['store_url']} "{game['title']}")

    ![{game['title']}]({images.get(game['title'], '')})
'''

    if games['free_next'] != []:
        content += '''
- ## 下周限免
'''

    for game in games['free_next']:
        content += f'''
  - ### [{game['title']}]({game['store_url']} "{game['title']}")

    原价: {game['origin_price']}

    购买链接: [{game['store_url']}]({game['store_url']} "{game['title']}")

    ![{game['title']}]({images.get(game['title'], '')})
'''

    with open(filename, 'w', encoding='utf-8') as f:
        f.write(content)


if __name__ == '__main__':
    games = get_free_games()
    generate_json(games, './epic_free_games.json')
    generate_markdown(games, './README.md')
