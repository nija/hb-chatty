import os
import sys
from random import choice
import twitter


from random import choice
from sys import argv

N_GRAM = int(argv[1])


def open_and_read_files(*paths):
    """Takes file path as string; returns text as string.

    Takes a string that is a file path, opens the file, and turns
    the file's contents as one string of text.
    """
    text = ''
    temp = ''
    for path_list in paths:
        for path in path_list:
            temp = open(str(path), 'r')
            text += temp.read()
    return text
    # with open(file_path, 'r') as f:
    #     return f.read()


def make_chains(text_string):
    """Takes input text as string; returns _dictionary_ of markov chains.

    A chain will be a key that consists of a tuple of (word1, word2)
    and the value would be a list of the word(s) that follow those two
    words in the input text.

    For example:

        >>> make_chains("hi there mary hi there juanita")
        {('hi', 'there'): ['mary', 'juanita'], ('there', 'mary'): ['hi'], ('mary', 'hi': ['there']}
    """
    chains = { }
    # Split on white space to get words
    words = text_string.split()

    for i in range(len(words) - N_GRAM):
        # Create tuple to hold n words
        words_ngram = tuple(words[i : i + N_GRAM ])
        # Get the last element
        element = words[i + N_GRAM]
        # If the tuple key exists, append the element to the value list 
        if words_ngram in chains:
            chains[words_ngram].append(element)
        # The tuple key doesn't exist, so create it and add the element in the value list
        else:
            chains[words_ngram] = [element]

    return chains


def make_text(chains):
    """Takes dictionary of markov chains; returns random text."""
    text = ''
    return_text = ''
    last_punctuation_index = 0
    sentence_enders = [".","!","?"]


    not_legit_caps = True

    while not_legit_caps:
        # Get the beginning tuple
        words_ngram = choice(chains.keys())
        # Start with a capitalized word
        if words_ngram[0][0].isupper():
            not_legit_caps = False
            text = " ".join(words_ngram)


    # Tuple is a key in chains dict
    while len(text) < 140:
        # Get a random list from the given tuple
        word_list = chains.get(words_ngram)

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
        make_text(chains)
    else:
        return return_text



def tweet(chains):
    # Use Python os.environ to get at environmental variables
    # Note: you must run `source secrets.sh` before running this file
    # to make sure these environmental variables are set.
    api = twitter.Api(
        consumer_key = os.environ['TWITTER_CONSUMER_KEY'],
        consumer_secret = os.environ['TWITTER_CONSUMER_SECRET'],
        access_token_key = os.environ['TWITTER_ACCESS_TOKEN_KEY'],
        access_token_secret = os.environ['TWITTER_ACCESS_TOKEN_SECRET']
        )
    print api.VerifyCredentials()

    status = api.PostUpdate(make_text(chains))

# Open the files and turn them into one long string
input_text = open_and_read_files(argv[2:])

# Get a Markov chain
chains = make_chains(input_text)


# # Produce random text
# random_text = make_text(chains)

# Tweet that business!
tweet(chains)