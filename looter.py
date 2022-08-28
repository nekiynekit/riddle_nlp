from collections import defaultdict
from distutils.command.clean import clean

import requests as rq
import bs4
import pandas as pd
import re


def loot_berry_riddles(url, dataset):
    response = rq.get(url)
    soup = bs4.BeautifulSoup(response.text, 'html.parser')
    trash = soup.find_all('li', class_='item')
    for piece in trash:
        try:
            dirty_riddle = piece.find('p')
            answer = piece.find('button')['data-a']
            riddle = str(dirty_riddle).replace('<br/>', ' ').replace('<p>', '').replace('</p>', '')
            dataset['riddle'].append(riddle)
            dataset['answer'].append(answer)
        except Exception as E:
            print(f"Can't parse tag because of {E}")

def loot_kartashov_riddles(url, dataset):
    response = rq.get(url)
    soup = bs4.BeautifulSoup(response.text, 'html.parser')
    current_layer = soup.find_all('div', class_='book-section')[1]

    dataset['riddle'].append('')
    for tag in current_layer:
        if tag.name == 'p':
            text = tag.string
            if not text:
                continue

            is_number = re.match(r'\d+\.', text)
            if not is_number:
                dataset['riddle'][-1] += f'{text} '

        elif tag.name == 'blockquote':
            text = tag.find('span').string
            text = re.match(r'\((.*)\)', text)

            if dataset['riddle'][-1]:
                dataset['riddle'].append('')

            if text:
                text = text.groups()[0]
                dataset['answer'].append(text)
            else:
                dataset['riddle'].pop()

            assert len(dataset['riddle']) - 1 == len(dataset['answer'])
            
    dataset['riddle'].pop()

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
    dataset = defaultdict(list)
    
    loot_kartashov_riddles('https://kartaslov.ru/книги/Юрий_Парфёнов_3333_Самая_толстая_книга_загадок_Загадки_для_ума_заплатки/2', dataset)
    for url in urls:
        loot_berry_riddles(url, dataset)
    puzzles = pd.DataFrame(data=dataset)
    print(len(puzzles))
    puzzles.to_csv('puzzles_dataset.csv')
    