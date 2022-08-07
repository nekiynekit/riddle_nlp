import requests as rq
import bs4
import pandas as pd

def loot_berry_riddle(url):
    response = rq.get(url)
    soup = bs4.BeautifulSoup(response.text, 'html.parser')
    trash = soup.find_all('li', class_='item')
    qa_dataset = []
    for piece in trash:
        try:
            dirty_riddle = piece.find('p')
            answer = piece.find('button')['data-a']
            riddle = str(dirty_riddle).replace('<br/>', '\n').replace('<p>', '').replace('</p>', '')
            qa_dataset.append((answer, riddle))
        except Exception as E:
            print(f"Can't parse tag because of {E}")
    return qa_dataset

if __name__ == '__main__':
    urls = [
        'https://deti-online.com/zagadki/zagadki-pro-yagody/',
        'https://deti-online.com/zagadki/zagadki-pro-griby/',
        'https://deti-online.com/zagadki/zagadki-ovoschi-frukty/',
        'https://deti-online.com/zagadki/zagadki-pro-edu/',
        'https://deti-online.com/zagadki/zagadki-pro-zhivotnyh/',
        'https://deti-online.com/zagadki/zagadki-pro-ptic/',
        'https://deti-online.com/zagadki/zagadki-pro-ryb/',
        'https://deti-online.com/zagadki/zagadki-pro-nasekomyh/zagadki-pro-svetljachka/',
        'https://deti-online.com/zagadki/zagadki-pro-nasekomyh/zagadki-pro-osu/',
        'https://deti-online.com/zagadki/zagadki-pro-nasekomyh/zagadki-pro-bloh/',
        'https://deti-online.com/zagadki/zagadki-pro-nasekomyh/zagadki-pro-gusenicu/',
        'https://deti-online.com/zagadki/zagadki-pro-nasekomyh/zagadki-pro-zhuka/',
        'https://deti-online.com/zagadki/zagadki-pro-ryb/zagadki-pro-akul/',
        'https://deti-online.com/zagadki/zagadki-pro-ryb/zagadki-pro-kita/',
        'https://deti-online.com/zagadki/zagadki-pro-ryb/zagadki-pro-delfinov/',
        'https://deti-online.com/zagadki/zagadki-semya-druzya/',
        'https://deti-online.com/zagadki/zagadki-pro-skazochnyh-geroev/',
        'https://deti-online.com/zagadki/zagadki-pro-cvety/',
        'https://deti-online.com/zagadki/zagadki-pro-kosmos/',
        'https://deti-online.com/zagadki/zagadki-pro-prirodnye-yavleniya/',
        'https://deti-online.com/zagadki/zagadki-pro-solnce/',
        'https://deti-online.com/zagadki/zagadki-pro-derevya/',
        'https://deti-online.com/zagadki/zagadki-pro-sport/',
        'https://deti-online.com/zagadki/zagadki-pro-transport/',
        'https://deti-online.com/zagadki/dlya-shkolnikov/populyarnye/',
    ]
    dataset = []
    for url in urls:
        dataset.extend(loot_berry_riddle(url))
    