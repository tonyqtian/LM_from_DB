# Natural Language Toolkit: Language Models
#
# Copyright (C) 2001-2010 NLTK Project
# Author: Steven Bird <sb@csse.unimelb.edu.au>
# URL: <http://www.nltk.org/>
# For license information, see LICENSE.TXT

#import random
#from itertools import chain

from __future__ import division
from math import log

#from nltk.probability import (ConditionalProbDist, ConditionalFreqDist, MLEProbDist)
#from nltk.util import ingrams

#from api import *

import MySQLdb

from replacer import RegexpReplacer
from nltk.tokenize import RegexpTokenizer

#def _estimator(fdist, bins):
#    """
#    Default estimator function using an MLEProbDist.
#    """
#    # can't be an instance method of NgramModel as they 
#    # can't be pickled either.
#    return MLEProbDist(fdist)

class NgramcModel(object):
    """
    A processing interface for assigning a probability to the next word.
    """

    # add cutoff
    def __init__(self, n, train="host = localhost, port = 3306, \
                 user = root, passwd = cikuutest! ", \
                 estimator="web1t"):
        """
        Creates an ngram language model to capture patterns in n consecutive
        words of training text.  An estimator smooths the probabilities derived
        from the text and may allow generation of ngrams not seen during
        training.

        @param n: the order of the language model (ngram size)
        @type n: C{int}
        @param train: the training text
        @type train: C{list} of C{string}
        @param estimator: a function for generating a probability distribution
        @type estimator: a function that takes a C{ConditionalFreqDist} and
              returns a C{ConditionalProbDist}
        """

        connection = MySQLdb.connect(host = "localhost", port = 3306,\
                                      user = "root", passwd = "cikuutest!")
        connection.select_db(estimator)
        self.cursor = connection.cursor()
        
        self.cnt_sum = (1, 1024908267229, 889143670228, 733110350273, \
                        503325708296, 349051688901)
        #sum[0] = 1
        #sum[1] = 1024908267229
        #sum[2] = 889143670228
        #sum[3] = 733110350273
        #sum[4] = 503325708296
        #sum[5] = 349051688901

        self._n = n
        self.slct = "select cnt from gramc where gram like '%s' "
        
        self.myReplacer = RegexpReplacer()
        self.tokenizer = RegexpTokenizer("[\w]+")

#        if estimator is None:
#            estimator = _estimator
#        
#        cfd = ConditionalFreqDist()
#        self._ngrams = set()
#        self._prefix = ('',) * (n - 1)
#
#        for ngram in ingrams(chain(self._prefix, train), n):
#            self._ngrams.add(ngram)
#            context = tuple(ngram[:-1])
#            token = ngram[-1]
#            cfd[context].inc(token)
#
#        self._model = ConditionalProbDist(cfd, estimator, len(cfd))

#        # recursively construct the lower-order models
#        if n > 1:
#            self._backoff = NgramcModel(n-1, train, estimator)

    # Katz Backoff probability
    def prob(self, word, context):
        """
        Evaluate the probability of this word in this context.
        """

        context = tuple(context)
        
        context_lenth = len(context) 
        if context_lenth == 0:
            line = ''
        elif context_lenth == 1:
            line = context[0]
        elif context_lenth >= 2:
            line = context[0]
            for each_word in context[1:]:
                line = line + ' ' + each_word
        line = line + ' ' + word
        
        try:
            #print self.slct % (line)
            self.cursor.execute(self.slct % (line))
            data = self.cursor.fetchall()
        except Exception, e:
            print "Error happened when access gramc DB: ", e
            return 1
        
        if len(data):
            cnt = data[0][0]
            #result = 0.0
            result = cnt / self.cnt_sum[context_lenth]
            #print result
            if result == 0:
                result = 1
            return result
        elif context_lenth == 0:
            return 1
        else:
            return self.prob(word, context[1:])
        
#        if context + (word,) in self._ngrams:
#            return self[context].prob(word)
#        elif self._n > 1:
#            return self._alpha(context) * self._backoff.prob(word, context[1:])
#        else:
#            return self[context].prob(word)

#    def _alpha(self, tokens):
#        return self._beta(tokens) / self._backoff._beta(tokens[1:])
#
#    def _beta(self, tokens):
#        token_lenth = len(tokens) 
#        if token_lenth == 0:
#            line = ''
#        elif token_lenth == 1:
#            line = tokens[0]
#        elif token_lenth >= 2:
#            line = tokens[0]
#            for word in tokens[1:]:
#                line = line + ' ' + word
#                
#        try:
#            self.cursor.execute(self.slct, (line,))
#            data = self.cursor.fetchall()
#        except Exception, e:
#            print "Error happened when access gramc DB: ", e
#            return 1
#        
#        if len(data):
#            cnt = data[0]
#            return cnt / self.cnt_sum[token_lenth]
#        else:
#            return 1

    def logprob(self, word, context):
        """
        Evaluate the (negative) log probability of this word in this context.
        """

        return -log(self.prob(word, context), 2)

#    def choose_random_word(self, context):
#        '''Randomly select a word that is likely to appear in this context.'''
#        return self.generate(1, context)[-1]
#
#    # NB, this will always start with same word since model
#    # is trained on a single text
#    def generate(self, num_words, context=()):
#        '''Generate random text based on the language model.'''
#        text = list(context)
#        for i in range(num_words):
#            text.append(self._generate_one(text))
#        return text
#
#    def _generate_one(self, context):
#        context = (self._prefix + tuple(context))[-self._n+1:]
#        # print "Context (%d): <%s>" % (self._n, ','.join(context))
#        if context in self:
#            return self[context].generate()
#        elif self._n > 1:
#            return self._backoff._generate_one(context[1:])
#        else:
#            return '.'

    def entropy(self, text):
        """
        Evaluate the total entropy of a text with respect to the model.
        This is the sum of the log probability of each word in the message.
        """

        text = self.myReplacer.replace(text)
        text = self.tokenizer.tokenize(text)
        e = 0.0
        lenth = len(text)
        if lenth == 0:
            return 0
        elif lenth < self._n:
            current_n = lenth
        else:
            current_n = self._n
            
        for i in range(current_n - 1, len(text)):
            context = tuple(text[(i - current_n + 1) : i])
            token = text[i]
            e += self.logprob(token, context)
        return e

    def __contains__(self, item):
        return tuple(item) in self._model

    def __getitem__(self, item):
        return self._model[tuple(item)]

    def __repr__(self):
        return '<NgramcModel with %d-grams> connected to %s' % (self._n, self.cursor)

def demo():
#    from nltk.corpus import brown
#    from nltk.probability import LidstoneProbDist, WittenBellProbDist
#    estimator = lambda fdist, bins: LidstoneProbDist(fdist, 0.2)
#    estimator = lambda fdist, bins: WittenBellProbDist(fdist, 0.2)
    lm = NgramcModel(5)
    print lm
    sent = "Like a bridge over troubled water, I will lay it down."
    print sent
    print "Entropy: ", lm.entropy(sent)
    
    sent = "it looked quiet lovely. "
    print sent
    print "Entropy: ", lm.entropy(sent)
    
    sent = "it looks quiet lovely. "
    print sent
    print "Entropy: ", lm.entropy(sent)
    
    sent = "he speak German. "
    print sent
    print "Entropy: ", lm.entropy(sent)
    
    sent = "he speaks German. "
    print sent
    print "Entropy: ", lm.entropy(sent)    

    sent = "in the shop all seller are very friendly they always smile. "
    print sent
    print "Entropy: ", lm.entropy(sent)    

    sent = "in the shop all sellers are very friendly they always smile. "
    print sent
    print "Entropy: ", lm.entropy(sent)    

#    text = lm.generate(100)
#    import textwrap
#    print '\n'.join(textwrap.wrap(' '.join(text)))

if __name__ == '__main__':
    demo()
