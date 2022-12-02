import json
import requests


def get_free_games() -> dict:
    games = {'free_now': [], 'free_next': []}
    url = 'https://store-site-backend-static.ak.epicgames.com/freeGamesPromotions?country=CN'
    resp = requests.get(url)
    for element in resp.json()['data']['Catalog']['searchStore']['elements']:
        if promotions := element['promotions']:
            game = {}
            game['title'] = element['title']
            game['images'] = element['keyImages']
            game['origin_price'] = element['price']['totalPrice']['fmtPrice']['originalPrice']
            game['discount_price'] = element['price']['totalPrice']['fmtPrice']['discountPrice']
            if offers := promotions['promotionalOffers']:
                game['start_date'] = offers[0]['promotionalOffers'][0]['startDate']
                game['end_date'] = offers[0]['promotionalOffers'][0]['endDate']
                games['free_now'].append(game)
            if offers := promotions['upcomingPromotionalOffers']:
                game['start_date'] = offers[0]['promotionalOffers'][0]['startDate']
                game['end_date'] = offers[0]['promotionalOffers'][0]['endDate']
                games['free_next'].append(game)
    return games


def generate_json(games: dict, filename: str):
    with open(filename, 'w') as f:
        json.dump(games, f)
        # json.dump(obj=games, fp=f, ensure_ascii=False, indent=4)


def generate_markdown(games: dict, filename: str):
    images = {}
    for data in games.values():
        for game in data:
            for image in game['images']:
                if image['type'] == 'OfferImageWide':
                    images[game['title']] = image['url']

    content = '''# Epic 每周限免

- ## 本周限免

***

'''

    for game in games['free_now']:
        content += f'''
  - ### [{game['title']}][]

  原价: {game['origin_price']}

  [![{game['title']}]({images[game['title']]})]({images[game['title']]})

'''

    content += f'''
- ## 下周限免

***

'''

    for game in games['free_next']:
        content += f'''
  - ### [{game['title']}][]

  原价: {game['origin_price']}

  [![{game['title']}]({images[game['title']]})]({images[game['title']]})

'''

    with open(filename, 'w') as f:
        f.write(content)


if __name__ == '__main__':
    games = get_free_games()
    generate_json(games, './epic_free_games.json')
    generate_markdown(games, './README.md')
