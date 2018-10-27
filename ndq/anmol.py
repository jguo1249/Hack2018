from sumy.parsers.html import HtmlParser
from sumy.parsers.plaintext import PlaintextParser
from sumy.nlp.tokenizers import Tokenizer
from sumy.summarizers.lsa import LsaSummarizer as Summarizer
from sumy.nlp.stemmers import Stemmer
from sumy.utils import get_stop_words
import nltk
import requests
from bs4 import BeautifulSoup
from newspaper import Article
import time

SENTENCE_COUNT = 8
SOURCES = dict()
SOURCES['Entertainment'] = [
    'https://www.cnn.com/entertainment',
    'https://www.nytimes.com/section/t-magazine/entertainment',
    'https://www.foxnews.com/entertainment',
]
SOURCES['Food'] = [
    'https://www.cnn.com/travel/food-and-drink',
    'https://www.nytimes.com/section/food',
    'https://www.wsj.com/news/life-arts/food-cooking-drink',
    'https://www.foxnews.com/food-drink'
]
SOURCES['Local'] = ['https://www.foxnews.com/search-results/search?q=columbus']
SOURCES['Politics'] = [
    'https://www.cnn.com/politics', 'https://www.nytimes.com/section/politics',
    'https://www.wsj.com/news/politics', 'https://www.foxnews.com/politics'
]
SOURCES['Science'] = [
    'https://www.cnn.com/specials/space-science',
    'https://www.nytimes.com/section/science',
    'https://www.wsj.com/news/science', 'https://www.foxnews.com/science'
]
SOURCES['Sports'] = [
    'https://edition.cnn.com/sport', 'https://www.nytimes.com/section/sports',
    'https://www.wsj.com/news/life-arts/sports',
    'https://www.foxnews.com/search-results/search?q=sports'
]
SOURCES['Technology'] = [
    'https://www.cnn.com/business/tech',
    'https://www.nytimes.com/section/technology',
    'https://www.wsj.com/news/technology',
    'https://www.foxbusiness.com/category/technology',
    'https://www.foxnews.com/tech'
]
SOURCES['World'] = [
    'https://www.cnn.com/world', 'https://www.nytimes.com/section/world',
    'https://www.wsj.com/news/world', 'https://www.foxnews.com/world'
]


# Headline
def format_headline(headline):
    return headline.title()


# Summary
def clean_sentence(sentence):
    clean_sentence = sentence
    removal_list = ['•', '\n', '\t', '(CNN)']
    for item in removal_list:
        clean_sentence = clean_sentence.replace(item, '')
    clean_sentence = clean_sentence.strip()
    return clean_sentence


def summarize(text):
    parser = PlaintextParser.from_string(text, Tokenizer('english'))
    summarizer = Summarizer(Stemmer('english'))
    summarizer.stop_words = get_stop_words('english')

    result = ''
    for sentence in summarizer(parser.document, SENTENCE_COUNT):
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


# Parse
def parse_article(url, topic):
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

# Get URLs
def obtain_news_sources(topic):

    for source in SOURCES[topic]:

    soup = BeautifulSoup()

    return sources


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


def main():
    sources = obtain_news_sources('')
    return


parse_article(
    'https://www.cnn.com/2018/10/27/us/pittsburgh-synagogue-active-shooter/index.html',
    '')
