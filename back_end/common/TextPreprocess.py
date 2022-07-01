from nltk.stem import PorterStemmer
import re
from nltk.corpus import stopwords
import spacy
import html.parser as htmlparser
from .Post_loader import *
from sklearn.feature_extraction.text import TfidfVectorizer

class TextPreprocess():

    def __init__(self):
        """Text preprocessing module
        Args:
            strlist (list): list of target strings. If unspecified, it uses
            a default list of vulnerability-related target phrases

        Use strmatch() to obtain all strings that were matched by the
        aho-corasick algorithm
        """
        self.ps = PorterStemmer()

        # Read UK/US spelling dictionary
        uk_us_csv = PostLoader().load_csv('/output/data/uk_us.csv')[1:]
        self.ukus = {one_ele[0]:one_ele[1] for one_ele in uk_us_csv}

        try:
            self.nlp = spacy.load("en_core_web_sm")
        except:
            from spacy.cli import download
            download("en_core_web_sm")
            self.nlp = spacy.load("en_core_web_sm")
        self.keep_tags = {'PUNCT', 'VERB', 'NOUN', 'PROPN', 'ADJ', 'SYM', 'NUM', 'ADP'}

        self.en_stop = set(stopwords.words('english'))
        self.en_stop.update(['use', 'like', 'tri', 'get', 'set', 'way', 'may', 'would', 'could', 'might', 'also'])

        self.parser = htmlparser.HTMLParser()

    def parse_html(self, s):
        return self.parser.unescape(s)

    def preprocess(self, s, remove_last=True, remove_marks=True):
        """Preprocess text - Removes code blocks and special char
        Args:
            s (str): string to be preprocessed
        Returns:
            str: preprocessed text joined by ' ' delimiter
        """

        # Remove code blocks
        s = re.sub('<pre>|<\/pre>|\n', ' ', s)
        s = re.sub('<code>|<\/code>|\n', ' ', s)
        s = re.sub('<samp>|<\/samp>|\n', ' ', s)
        s = re.sub('<.*?>|\'', ' ', s)

        # Remove certain special characters
        s = s.replace('\"', "''").replace('\"', "''").replace('\'', '').replace(': ', ' ').\
            replace('(', '').replace(')', '').replace('\n', '').strip().lower()

        if remove_marks:
            s = s.replace(', ', ' ').replace('; ', ' ').replace('. ', ' ')

        # Check empty string
        if s == "": return ""

        # Remove last char if letter or number
        if remove_last:
            if not s[-1].isalnum(): s = s[:-1]
        return s

    def stem(self, t):
        """Convenience function for stemming multiple words delimited by ' '.
           Only stems words that are length > 3
        Args:
            t (str): string of words (tokens defined with delimiter ' ')
        Returns:
            str: string of stemmed words
        """
        return ' '.join([self.ps.stem(i) if len(i) > 3 else i for i in t.split()])

    def reverse_ukus(self, phrase, delim=' '):
        """Reverse UK US spelling of a phrase
        Args:
            phrase (str): string of words where spelling is to be reversed
            delim (str): phrase delimiter. Could be ' ', '_', etc.
        Returns:
            str: string of words joined by given delimiter with the spelling
            reversed from UK to US or US to UK
        """

        ret = []
        for i in phrase.split():
            if i in self.ukus: ret.append(self.ukus[i])
            else: ret.append(i)
        return delim.join(ret)

    def select_by_pos(self, s):
        doc = self.nlp(s)
        ret = []
        for one_token in doc:
            if one_token.pos_ in self.keep_tags:
                ret.append(str(one_token.lemma_))

        return ' '.join(ret)


    def remove_stopwords(self, s):
        return ' '.join([i for i in s.split() if not i in self.en_stop])

    def clean_so_data(self, text):
        text = self.parse_html(text)
        text = self.preprocess(text).lower()
        text = self.reverse_ukus(text)
        text = self.select_by_pos(text)
        text = self.stem(text)
        return self.remove_stopwords(text)

    def clean_so_data_nopos(self, text, remove_last=True, remove_marks=True, remove_stop=True):
        # text = self.parse_html(text)
        text = self.preprocess(text, remove_last, remove_marks).lower()
        text = self.reverse_ukus(text)
        text = self.stem(text)
        if remove_stop:
            return self.remove_stopwords(text)
        else:
            return text

    def clean_data_simple(self,text):
        text = self.parse_html(text)
        text = self.preprocess(text).lower()
        return text

    def cal_idf(self, text_set):
        text_set.remove('')
        text_set = list(text_set)
        vectorizer = TfidfVectorizer()
        X = vectorizer.fit_transform(text_set)
        word = vectorizer.get_feature_names()
        idf = vectorizer.idf_
        return dict(zip(word, idf))

    def cal_tf(self, word_list):
        word_set = set(word_list)
        tf = [(one_word, word_list.count(one_word)/len(word_list)) for one_word in word_set]
        return tf