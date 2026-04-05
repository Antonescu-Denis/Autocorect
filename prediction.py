import wordfreq, Levenshtein

maximum = [0, '']
lengths = {}
for thing in wordfreq.get_frequency_list('ro'):
    if thing:
        for th in thing:
            if len(th) > maximum[0]:
                maximum = [len(th), th]
            if len(th) in lengths.keys():
                lengths[len(th)] += 1
            else:
                lengths[len(th)] = 1
for key, val in lengths.items():
    print(f"{key} - {val}")

# don't make suggestions until len(fv.word) == 2
# suggestions should have same/greater length than fv.word
