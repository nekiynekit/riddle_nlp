from cmath import nan
import re
from xml.dom.minidom import Attr
import pandas as pd


junk_symbs = r'[\?\.,:;!\-…–—"()]'
dictionary = set()

def clean_str(s: str) -> str:
    s = s.lower()
    s = re.sub(junk_symbs, r'', s)
    s = s.replace('ё', 'е')
    s = s.replace('ó', 'о')
    s = s.replace('ó', 'о')
    for symb in ['a', 'c', 'e', 'l', 'p']:
        s = s.replace(symb, '')

    global dictionary
    dictionary = dictionary.union(set(s))
    return s

def clean_df(dataframe: pd.DataFrame) -> pd.DataFrame:
    dataframe['answer'] = list(map(clean_str, dataframe['answer']))
    dataframe['riddle'] = list(map(clean_str, dataframe['riddle']))
    print(sorted(dictionary))
    return dataframe

if __name__ == '__main__':
    data = pd.read_csv('puzzles_dataset.csv')
    data = data.drop('Unnamed: 0', axis=1)
    data = clean_df(data)
    nones = []
    for idx, riddle, answer in zip(range(len(data)), data['riddle'], data['answer']):
        if not isinstance(answer, str) or not isinstance(riddle, str):
            data = data.drop(idx, axis=0)
            print(idx, riddle, answer)
            
    data.to_csv('puzzles_dataset.csv')