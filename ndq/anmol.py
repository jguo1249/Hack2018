import re
import time
import string
from dateutil import parser
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
SOURCES['local'] = [
    'https://abc6onyourside.com/news/local', 'https://www.10tv.com/local-news',
    'https://www.10tv.com/categories/ohio-news'
]
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

TAGS = set()
TAGS.add('headline')
TAGS.add('article')

BAD_TAGS = set()
BAD_TAGS.add('video.foxnews')
BAD_TAGS.add('fool')
BAD_TAGS.add('comparecards')
BAD_TAGS.add('bleacherreport')
BAD_TAGS.add('lendingtree')
BAD_TAGS.add('tmz')
BAD_TAGS.add('foxnews.com/category')

TRANSLATION_TABLE = str.maketrans(
    string.punctuation + string.ascii_uppercase,
    " " * len(string.punctuation) + string.ascii_lowercase)


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


# Date
def format_date(date_time):
    if date_time is not None:
        result = str(parser.parse(str(date_time)))
        return result[0:-6]
    else:
        return None


# Authors
def format_authors(authors):
    result = ''

    for author in authors:
        result += author + ','

    if result == '':
        return None
    else:
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
        result['published'] = format_date(article.publish_date)
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


# Cluster - Helper
def document_distance(a, b):
    def get_words(text):
        text = text.translate(TRANSLATION_TABLE)
        word_list = text.split()
        return word_list

    def count_frequency(word_list):
        freq_mapping = {}
        for new_word in word_list:
            if new_word in freq_mapping:
                freq_mapping[new_word] = freq_mapping[new_word] + 1
            else:
                freq_mapping[new_word] = 1
        return freq_mapping

    def dot_product(a, b):
        sum = 0.0
        for key in a:
            if key in b:
                sum += a[key] * b[key]
        return sum

    a_word_list = get_words(a)
    a_freq_mapping = count_frequency(a_word_list)
    b_word_list = get_words(b)
    b_freq_mapping = count_frequency(b_word_list)

    numerator = inner_product(a_freq_mapping, b_freq_mapping)
    denominator = math.sqrt(
        inner_product(a_freq_mapping, b_freq_mapping) * inner_product(
            a_freq_mapping, b_freq_mapping))
    distance = math.acos(numerator / denominator)
    return distance


# Cluster
def cluster(articles, num_articles_wanted):
    return articles[0:num_articles_wanted]


## Parse News Sources
def parse_news_sources(topic, num_articles_wanted, total_articles_to_consider):
    urls = set()
    articles_to_consider = total_articles_to_consider / len(SOURCES[topic])

    for source in SOURCES[topic]:
        html = get_html(source)
        soup = BeautifulSoup(html, 'lxml')
        source_urls = set()

        for tag in TAGS:
            regex = re.compile('.*' + tag + '.*', re.IGNORECASE)

            for block in soup.find_all(attrs={'class': regex}):
                for sub_block in block.find_all('a', href=True):
                    if len(source_urls) < articles_to_consider:
                        url = sub_block['href']

                        if url is not None:
                            if 'http' not in url:
                                url = source[0:source.index('.com') + 4] + url

                            if url != source and not any(
                                    substring in url
                                    for substring in BAD_TAGS):
                                source_urls.add(url)

        urls.update(source_urls)

    articles = []
    for url in urls:
        article = parse_article(url, topic)
        if article is not None:
            articles.append(article)

    result = cluster(articles, num_articles_wanted)
    return result


def main():
    start = time.time()
    sources = parse_news_sources('world', 5, 50)
    end = time.time()
    print(str(end - start) + ' elapsed')

    for source in sources:
        for key in source:
            print(source[key])

    return


main()
