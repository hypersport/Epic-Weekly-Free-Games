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


def generate_json(data: dict, filename: str):
    with open(filename, 'w') as f:
        json.dump(data, f)
        # json.dump(obj=data, fp=f, ensure_ascii=False, indent=4)


def generate_markdown(data: dict, filename: str):
    pass


if __name__ == '__main__':
    games = get_free_games()
    generate_json(games, './epic_free_games.json')
