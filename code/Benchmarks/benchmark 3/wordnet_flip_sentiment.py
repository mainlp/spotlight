from nltk.corpus import wordnet as wn
from nltk.corpus import sentiwordnet as swn
import numpy as np
import nltk

def is_adjective(word):
    for synset in wn.synsets(word):
        if synset.pos() == 'a' or synset.pos() == 'r' or synset.pos() == 's':
            return True
    return False

def get_antonyms(word, pos_tag):
    antonyms = []
    for synset in wn.synsets(word):
        if synset.pos() == pos_tag:
            for lemma in synset.lemmas():
                for antonym in lemma.antonyms():
                    antonyms.append(antonym.name())
    return antonyms

def is_sentiment(word, pos_tag=None):
    for synset in swn.senti_synsets(word):
        if pos_tag is None or synset.pos() == pos_tag:
            if synset.pos_score() > 0 or synset.neg_score() > 0:
                return True
    return False

def sentiment_score(word, pos_tag=None):
    scores = []
    for synset in swn.senti_synsets(word):
        if pos_tag is None or synset.pos() == pos_tag:
            if np.abs(synset.pos_score() - synset.neg_score()) > 0:
                scores.append(synset.pos_score() - synset.neg_score())
    return np.mean(scores)

def sort_by_sentiment(words):
    scores = [sentiment_score(word) for word in words]
    print("words:", words)
    print("scores:", scores)
    ids = np.argsort(scores)
    words_sorted = [words[i] for i in ids]
    print("words_sorted:", words_sorted)
    return words_sorted

def flip_sentiment(sentence, tokenizer):
    tokens = tokenizer.tokenize(sentence)
    tokens_flipped = []
    for token in tokens:
        print(token, is_adjective(token), is_sentiment(token))
        if is_adjective(token) and is_sentiment(token):
            antonyms = get_antonyms(token)
            print(antonyms)
            if antonyms:
                # add maximising opposite sentiment
                antonyms_sorted = sort_by_sentiment(antonyms)
                if sentiment_score(token) > 0:
                    token = antonyms_sorted[-1]
                else:
                    token = antonyms_sorted[0]
        tokens_flipped.append(token)
    return tokenizer.convert_tokens_to_string(tokens_flipped)

class WhitespaceTokenizer:
    
    def tokenize(self, text):
        # split at whitespace and punctuation (keeping punctuation as a token)
        tokens = nltk.word_tokenize(text)
        return tokens

    def convert_tokens_to_string(self, tokens):
        # avoid prepending whitespace to punctuation
        sentence = ""
        for token in tokens:
            if nltk.tokenize.punkt.PunktToken(token).is_non_punct:
                sentence += " " + token
            else:
                sentence += token
        return sentence


sentence = "I did not like this movie."
tokenizer = WhitespaceTokenizer()
print(flip_sentiment(sentence, tokenizer))