#!/usr/bin/python
__author__ = 'Josh Hudson'

import argparse

def load_word_dict():
    """Load the word list files into a master word list for validation."""

    word_dict = {}
    
    # Load the word list from the word files. This word list is pretty verbose
    # and includes a lot of acronyms, so don't dock me when weird permutations
    # show up :)
    for file in ['english.%d' % number for number in range(4)]:
        with open('word_lists/'+file) as f:
            for line in f:
                # Strip carriage returns and newlines.
                line = line.lower().replace('\r\n', '')
                # Sort the word lists into a dictionary by letter, to make
                # filtering for valid words easier later.
                if word_dict.get(line[0],):
                    word_dict[line[0]].append(line)
                else:
                    word_dict[line[0]] = [line,]
                    
    return word_dict


def recursive_jumble(string):
    """Recursively go through your word and return permutations as a generator."""

    if len(string) == 1:
        yield string
    else:
        # I <3 enumerate
        for index, letter in enumerate(string):
            # Recursively find permutations of string minus current
            # letter. Yield
            for combo in recursive_jumble(string[:index] + string[index+1:]):
                yield letter + combo
                yield combo


def filter_words(potential_words, word_dict):
    """Validate potential words against our dictionary of words."""

    filtered_words = []
    
    for word in potential_words:
        # If the word is in our word list and not a duplicate, add it.
        if word in word_dict.get(word[0]) and word not in filtered_words:
            filtered_words.append(word)
            
    return filtered_words


def produce_word_jumbles(word):
    """Bringing it all together."""

    word_dict = load_word_dict()
    potential_words = recursive_jumble(word)
    filtered_words = filter_words(potential_words, word_dict)
    return filtered_words


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Sample script to list string/substring permutations for a given string')
    parser.add_argument('-w', '--word', help='A string used to genereate permutations', required=True)
    args = parser.parse_args()
    print produce_word_jumbles(args.word)
