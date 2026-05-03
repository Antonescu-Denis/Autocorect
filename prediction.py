import wordfreq, Levenshtein
import funcvar as fv


fv.get_word_list()

# don't make suggestions until len(fv.word) == min_length
# suggestions should have same/greater length than fv.word
# make trie for words, each node has:
#     - end of word flag
#     - dict of chars and their nodes
# maybe stop when you have enough suggestions, or adjust at runtime
#     - optional but ideal, pre-sort words by frequency 
# store trie somehow for performance
# word ranking:
#     - frequency, more frequent = better
#     - edit distance, smaller edit distance = better