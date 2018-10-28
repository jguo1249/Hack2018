import re
import time

import nltk
import requests
from bs4 import BeautifulSoup
from newspaper import Article
from sumy.nlp.stemmers import Stemmer
from sumy.nlp.tokenizers import Tokenizer
from sumy.parsers.html import HtmlParser
from sumy.parsers.plaintext import PlaintextParser
from sumy.summarizers.lsa import LsaSummarizer as Summarizer
from sumy.utils import get_stop_words

SUMMARIZER = Summarizer(Stemmer('english'))
SUMMARIZER.stop_words = get_stop_words('english')

SENTENCE_COUNT = 8
SOURCES = dict()
SOURCES['entertainment'] = [
    'https://www.cnn.com/entertainment',
    'https://www.nytimes.com/section/t-magazine/entertainment',
    'https://www.foxnews.com/entertainment',
]
SOURCES['food'] = [
    'https://www.cnn.com/travel/food-and-drink',
    'https://www.nytimes.com/section/food',
    'https://www.wsj.com/news/life-arts/food-cooking-drink',
    'https://www.foxnews.com/food-drink'
]
SOURCES['local'] = ['https://www.foxnews.com/search-results/search?q=columbus']
SOURCES['politics'] = [
    'https://www.cnn.com/politics', 'https://www.nytimes.com/section/politics',
    'https://www.wsj.com/news/politics', 'https://www.foxnews.com/politics'
]
SOURCES['science'] = [
    'https://www.cnn.com/specials/space-science',
    'https://www.nytimes.com/section/science',
    'https://www.wsj.com/news/science', 'https://www.foxnews.com/science'
]
SOURCES['sports'] = [
    'https://edition.cnn.com/sport', 'https://www.nytimes.com/section/sports',
    'https://www.wsj.com/news/life-arts/sports',
    'https://www.foxnews.com/search-results/search?q=sports'
]
SOURCES['technology'] = [
    'https://www.cnn.com/business/tech',
    'https://www.nytimes.com/section/technology',
    'https://www.wsj.com/news/technology',
    'https://www.foxbusiness.com/category/technology',
    'https://www.foxnews.com/tech'
]
SOURCES['world'] = [
    'https://www.cnn.com/world', 'https://www.nytimes.com/section/world',
    'https://www.wsj.com/news/world', 'https://www.foxnews.com/world'
]

TAGS = ['headline', 'article']
BAD_TAGS = ['video', 'fool', 'comparecards', 'bleacherreport', 'lendingtree']


## Parse Article - Helpers
# Headline
def format_headline(headline):
    return headline.title()


# Summary - Helper
def clean_sentence(sentence):
    clean_sentence = sentence
    removal_list = ['•', '\n', '\t', '(CNN)']
    for item in removal_list:
        clean_sentence = clean_sentence.replace(item, '')
    clean_sentence = clean_sentence.strip()
    return clean_sentence


# Summary
def summarize(text):
    parser = PlaintextParser.from_string(text, Tokenizer('english'))

    result = ''
    for sentence in SUMMARIZER(parser.document, SENTENCE_COUNT):
        result += clean_sentence(str(sentence)) + " "
    return result.strip()


# Published
def format_published(date_time):
    temp = str(date_time)
    pattern = '%Y-%m-%d %H:%M:%S'
    epoch = int(time.mktime(time.strptime(temp, pattern)))
    return epoch


# Authors
def format_authors(authors):
    result = ''
    for author in authors:
        result += author + ','
    return result[:-1]


## Parse Article
def parse_article(url, topic):
    try:
        article = Article(url)
        article.download()
        article.parse()

        result = dict()
        result['headline'] = format_headline(article.title)
        result['body'] = summarize(article.text)
        result['link'] = url
        result['topic'] = topic
        result['published'] = format_published(article.publish_date)
        result['author'] = format_authors(article.authors)
        result['image'] = article.top_image

        return result

    except Exception as e:
        print(url + ' failed:')
        print(e)
        return None


## Parse News Sources - Helpers
# Get HTML
def get_html(url):
    response = requests.get(url)

    if response.encoding != 'ISO-8859-1':
        html = response.text
    else:
        html = response.content
        if 'charset' not in response.headers.get('content-type'):
            encodings = requests.utils.get_encodings_from_content(
                response.text)
            if len(encodings) > 0:
                response.encoding = encodings[0]
                html = response.text

    return html or ''


## Parse News Sources
def parse_news_sources(topic):
    urls = []

    for source in SOURCES[topic]:
        html = get_html(source)
        soup = BeautifulSoup(html, 'html.parser')

        for tag in TAGS:
            regex = re.compile('.*' + tag + '.*', re.IGNORECASE)

            for block in soup.find_all(attrs={'class': regex}):
                for sub_block in block.find_all('a', href=True):
                    url = sub_block['href']
                    if url != None:
                        if 'http' not in url:
                            url = source[0:source.index('.com') + 4] + url
                        urls.append(url)

    def is_valid(url):
        for tag in BAD_TAGS:
            if tag in url:
                return False
        return True

    urls[:] = [url for url in urls if is_valid(url)]

    #temp to speed things up
    urls = urls[0:10]

    result = []
    for url in urls:
        article = parse_article(url, topic)
        if article is not None:
            result.append(article)
    return result
