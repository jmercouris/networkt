"""
Utility to strip tweets of arbitrary characters

"""
import re

from nltk.corpus import stopwords
from nltk.tokenize import TweetTokenizer


def process(text):
    # remove urls
    text = re.sub(r"http\S+", "", text)
    
    # attempt to remove twitter artifacts
    text = ' '.join(re.sub("(@[A-Za-z0-9]+)|([^0-9A-Za-z \t])|(\w+:\/\/\S+)", " ", text).split())
    
    # Strip RT
    text = text.replace('RT', '')
    
    tknzr = TweetTokenizer(strip_handles=True, reduce_len=True)
    words = tknzr.tokenize(text)
    
    # remove stopwords
    filtered_words = [word for word in words
                      if word not in stopwords.words('english')]
    filtered_words = [word for word in filtered_words
                      if word not in stopwords.words('german')]
    
    return filtered_words
