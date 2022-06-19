# Web parser
import requests
from bs4 import BeautifulSoup
from fake_useragent import UserAgent
import pandas as pd
import traceback

page_link = 'https://news.ycombinator.com/news'

def ftitle(soup, stats):
    find_title = soup.findAll(lambda tag: tag.name == 'a' and tag.get('class') == ['titlelink'])
    title = [title.text for title in find_title]
    return title

def ftitlelink(soup, stats):
    find_titlelink = soup.findAll(lambda tag: tag.name == 'a' and tag.get('class') == ['titlelink'])
    link = [link.attrs['href'] for link ain find_titlelink]
    return link

def fage(soup, stats):
    find_age = soup.findAll(lambda tag: tag.name == 'span' and tag.get('class') == ['age'])
    age = [age.attrs['title'] for age in find_age]
    return age

def fhnusers(soup, stats):
    find_hnusers = soup.findAll(lambda tag: tag.name == 'a' and tag.get('class') == ['hnuser'])
    hnusers = [hnusers.text for hnusers in find_hnusers]
    return hnusers

def getData(page_link):

    responce = requests.get(page_link, headers={'User-Agent': UserAgent().safari})
    if not responce.ok:
        return responce.status_code

    content = responce.content
    soup = BeautifulSoup(content, 'html.parser')

    find_title = ftitle(soup=soup, stats='title')
    find_titlelink = ftitlelink(soup=soup, stats='titlelink')
    find_age = fage(soup=soup, stats='age')
    find_hnusers = fhnusers(soup=soup, stats='hnusers')

    raw_data = {
        "title":find_title, "titlelink":find_titlelink,
        "age":find_age, "hnusers":find_hnusers
    }

    return raw_data

raw_data = getData(page_link)
df = pd.DataFrame(columns=['title', 'titlelink', 'age', 'hnusers'])
df = df.append(raw_data, ignore_index=True)

if __name__ == "__main__":
    print(df)
    # print(getData(page_link))
