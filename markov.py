import os
import sys
from random import choice
from sys import argv

class Markov(object):
    '''Markov chain story generation'''

    def __init__(self, ngram = 3, limit = 140, paths=['static/markov_text/green-eggs.txt']):

        self.n_gram = ngram
        self.character_limit = limit
        # Open the files and turn them into one long string
        self.input_text = self._open_and_read_files(paths)

        # Get a Markov chain
        self.chains = self._make_chains(self.input_text)

    def _open_and_read_files(self, paths):
        """Takes file path as string; returns text as string.

        Takes a string that is a file path, opens the file, and turns
        the file's contents as one string of text.
        """
        text = ''
        for path in paths:
            with open(path, 'r') as filey:
                text += filey.read()
        return text

    def _make_chains(self, text_string):
        """Takes input text as string; returns _dictionary_ of markov chains.

        A chain will be a key that consists of a tuple of (word1, word2)
        and the value would be a list of the word(s) that follow those two
        words in the input text.

        For example:

            >>> _make_chains("hi there mary hi there juanita")
            {('hi', 'there'): ['mary', 'juanita'], ('there', 'mary'): ['hi'], ('mary', 'hi': ['there']}
        """
        chains = {}
        # Split on white space to get words
        words = text_string.split()

        for i in range(len(words) - self.n_gram):
            # Create tuple to hold n words
            words_ngram = tuple(words[i : i + self.n_gram])
            # Get the last element
            element = words[i + self.n_gram]
            # If the tuple key exists, append the element to the value list
            if words_ngram in chains:
                chains[words_ngram].append(element)
            # The tuple key doesn't exist, so create it and add the element in the value list
            else:
                chains[words_ngram] = [element]

        return chains

    def tell_a_story(self):
        """Takes dictionary of markov chains; returns random text."""
        text = ''
        return_text = ''
        last_punctuation_index = 0
        sentence_enders = [".", "!", "?"]


        not_legit_caps = True

        while not_legit_caps:
            # Get the beginning tuple
            words_ngram = choice(list(self.chains.keys()))
            # Start with a capitalized word
            if words_ngram[0][0].isupper():
                not_legit_caps = False
                text = " ".join(words_ngram)


        # Tuple is a key in chains dict
        while len(text) < self.character_limit:
            # Get a random list from the given tuple
            word_list = self.chains.get(words_ngram)

            # Check for an empty list
            if word_list is None:
                break

            word_n = choice(word_list)

            # Add strings to text
            text = text + " " + word_n

            # Set the punctuation flag for slicing
            if word_n[-1] in sentence_enders:
                last_punctuation_index = len(text) - 1

            # Shift over the words to get the next key
            words_ngram = words_ngram[1:] + (word_n,)

        # Set and test our return text
        return_text = text[:last_punctuation_index + 1]

        if return_text is '':
            self.tell_a_story()
        else:
            return return_text

# TODO: Make this a unittest
if __name__ == '__main__':
    '''
    As a convenience, if we run this module interactively, it will leave
    you in a state of being able to work with the objects directly.
    '''

    marky = Markov(
        limit = 400,
        ngram = 5,
        paths = ['static/markov_text/alice_in_wonderland.txt',
                'static/markov_text/through_the_looking_glass.txt'])

    print(marky.tell_a_story())
    