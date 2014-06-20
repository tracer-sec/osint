import sys
import os
import json
import pprint
import re
import operator
import textblob

def process_text(text):
    # pre-process text (remove usernames, hashtags and urls)
    text = re.sub('#[a-zA-Z]+\s*', '', text)
    text = re.sub('@[a-zA-Z0-9]+', '', text)
    text = re.sub('https?\://[a-zA-Z0-9/?=:&#._-]+', '', text)
    return textblob.TextBlob(text)
    
def get_tags(blob):
    return blob.tags
    
def get_nouns(blob):
    return [x[0] for x in blob.tags if x[1].startswith('N')]
    
def get_noun_phrases(blob):
    return blob.noun_phrases
    
def get_sentiments(blob):
    return [x.sentiment for x in blob.sentences]
    
def get_wordcounts(blob):
    # only interested in nouns, verbs and adjectives
    interesting_words = [x[0].lower() for x in blob.tags if x[1].startswith('N') or x[1].startswith('V') or x[1].startswith('J')]
    filtered_list = [x for x in blob.word_counts.items() if x[0].lower() in interesting_words]
    return sorted(filtered_list, key=operator.itemgetter(1), reverse=True)
    
def parse_tweet(t):
    blob = process_text(t)
    result = { 
        'text': t, 
        'nouns': get_nouns(blob), 
        'noun_phrases': get_noun_phrases(blob), 
        'word_counts': get_wordcounts(blob), 
        'sentiments': get_sentiments(blob) 
    }
    return result
    
if __name__ == '__main__':
    '''
    t = process_text('This cat is crap. I love that dog, though.')
    print(get_tags(t))
    print(get_nouns(t))
    print(get_sentiments(t))
    '''
    output = open('result.txt', 'a')
    path = sys.argv[1]
    for file in os.listdir(path):
        if file.endswith('.json') and os.path.isfile(os.path.join(path, file)):
            f = open(os.path.join(path, file), 'r')
            j = json.load(f)
            f.close()
            # filter out hashtags? users?
            result = parse_tweet(j['text'])
            pprint.pprint(result, output, 4)
            output.write('----------------------------\n')
    output.close()
    
'''
CC    Coordinating conjunction
CD    Cardinal number
DT    Determiner
EX    Existential there
FW    Foreign word
IN    Preposition or subordinating conjunction
JJ    Adjective
JJR   Adjective, comparative
JJS   Adjective, superlative
LS    List item marker
MD    Modal
NN    Noun, singular or mass
NNS   Noun, plural
NNP   Proper noun, singular
NNPS  Proper noun, plural
PDT   Predeterminer
POS   Possessive ending
PRP   Personal pronoun
PRP$  Possessive pronoun
RB    Adverb
RBR   Adverb, comparative
RBS   Adverb, superlative
RP    Particle
SYM   Symbol
TO    to
UH    Interjection
VB    Verb, base form
VBD   Verb, past tense
VBG   Verb, gerund or present participle
VBN   Verb, past participle
VBP   Verb, non-3rd person singular present
VBZ   Verb, 3rd person singular present
WDT   Wh-determiner
WP    Wh-pronoun
WP$   Possessive wh-pronoun
WRB   Wh-adverb 
'''
