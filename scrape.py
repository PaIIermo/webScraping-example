import requests
from bs4 import BeautifulSoup
import pprint

with open('keywords.txt', 'r') as file:
    keywords = [line.strip().lower() for line in file]

links = []
subtext = []

for x in range(2):
    res = requests.get(f'https://news.ycombinator.com/?p={x + 1}')
    soup = BeautifulSoup(res.text, 'html.parser')
    links.extend(soup.select('.titleline > a'))
    subtext.extend(soup.select('.subtext'))


def create_custom_hn(links, subtext, keywords):
    hn = []
    for index, item in enumerate(links):
        title = links[index].getText()
        href = links[index].get('href', None)
        vote = subtext[index].select('.score')
        if len(vote):
            points = int(vote[0].getText().replace(' points', ''))
            if points > 99 or any(keyword in title.lower() for keyword in keywords):
                hn.append({'title': title, 'link': href, 'votes': points})
    return sort_stories(hn)


def sort_stories(news):
    return sorted(news, key=lambda k: k['votes'], reverse=True)


pprint.pprint(create_custom_hn(links, subtext, keywords))
