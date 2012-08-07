'''
Created on Nov 28, 2011

@author: Tony
'''
import re
import enchant
from nltk.metrics import edit_distance

replacement_patterns = [(r'ly$', '')]

class RegexpReplacer(object):
    def __init__(self, patterns = replacement_patterns):
        self.patterns = [(re.compile(regex), repl) for (regex, repl) in patterns]
    def replace(self, text):
        s = text
        for (pattern, repl) in self.patterns:
            (s, count) = re.subn(pattern, repl, s)
        return s

class SpellingReplacer(object):

    def __init__(self, dict_name = 'en', max_dist = 2):

        self.spell_dict = enchant.Dict(dict_name)
        self.max_dist = 2
        
    def replace(self, word):
        if self.spell_dict.check(word):
            return word
        suggestions = self.spell_dict.suggest(word)
        
        if suggestions and edit_distance(word, suggestions[0]) <= self.max_dist:
            return suggestions[0]
        else:
            return word