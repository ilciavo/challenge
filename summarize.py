"""
Script to summary text from an url using NLTK
based on : https://stackabuse.com/text-summarization-with-nltk-in-python/
author: leonardo.echeverria@gmail.com
"""

import heapq
import bs4 as bs
import urllib.request
import re
import nltk

def retrieve_text():
    scraped_data = urllib.request.urlopen('https://en.wikipedia.org/wiki/Artificial_intelligence')
    article = scraped_data.read()
    parsed_article = bs.BeautifulSoup(article,'lxml')
    paragraphs = parsed_article.find_all('p')

    article_text = ""

    for p in paragraphs:
        article_text += p.text

    return article_text


def summarize_text(article_text):
    #Preprocessing
    # Removing Square Brackets and Extra Spaces
    article_text = re.sub(r'\[[0-9]*\]', ' ', article_text)
    article_text = re.sub(r'\s+', ' ', article_text)

    # Removing special characters and digits
    formatted_article_text = re.sub('[^a-zA-Z]', ' ', article_text)
    formatted_article_text = re.sub(r'\s+', ' ', formatted_article_text)


    #Converting text to sentences
    sentence_list = nltk.sent_tokenize(article_text)

    #Find weighted frequency
    stopwords = nltk.corpus.stopwords.words('english')

    word_frequencies = {}
    for word in nltk.word_tokenize(formatted_article_text):
        if word not in stopwords:
            if word not in word_frequencies.keys():
                word_frequencies[word] = 1
            else:
                word_frequencies[word] += 1

    maximum_frequncy = max(word_frequencies.values())

    for word in word_frequencies.keys():
        word_frequencies[word] = (word_frequencies[word] / maximum_frequncy)

    #Compute sentence scores
    sentence_scores = {}
    for sent in sentence_list:
        for word in nltk.word_tokenize(sent.lower()):
            if word in word_frequencies.keys():
                if len(sent.split(' ')) < 30:
                    if sent not in sentence_scores.keys():
                        sentence_scores[sent] = word_frequencies[word]
                    else:
                        sentence_scores[sent] += word_frequencies[word]

    #Get summary
    summary_sentences = heapq.nlargest(7, sentence_scores, key=sentence_scores.get)

    summary = ' '.join(summary_sentences)

    return summary

if __name__ == "__main__":
    article_text = retrieve_text()
    summary = summarize(article_text)
    #print("Article:", article_text)
    print("Summary:", summary)