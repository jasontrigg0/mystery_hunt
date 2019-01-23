#for finding phrases that have certain letters in certain patterns
from collections import Counter
import csv
import math
import sys
from trie import Trie, counter_to_list

def counter_diff_with_failures(cntr1, cntr2):
    #extend cntr1 - cntr2 to handle cases where cntr2 may have some values greater than cntr1
    keys = set(list(cntr1.keys()) + list(cntr2.keys()))
    intersection = cntr1 & cntr2

    diff = cntr1 - intersection
    failure_cnt = sum((cntr2 - intersection).values())
    return diff, failure_cnt

def find_anagrams(letter_bank, word_cnt, wildcards, all_tries, find_subsets=False, test=None):
    if word_cnt > 3:
        raise

    #@arg all_tries: a list of tries, each greater than the one before
    #print the results for the smallest / most interesting trie first
    #and then run the larger ones in succession, printing the less
    #interesting results

    #@arg test is a function from a partial list of [words] to screen them out
    #if they can't possibly be the answer
    #for example, maybe we know that the answer is "O?(X|E)?(E|X)?ORELION"
    #then after we pick the first word we may be able to eliminate if for not fitting
    #this pattern


    #idea: start with the smallest tries
    #and then increase one at a time, starting with the *innermost*
    #because that one should be the fastest / easiest to match
    #eg with 3 words:
    #first try with
    #[trie1_id, trie2_id, trie3_id] = 0,0,0
    #then 0,0,1
    #then 0,0,2
    #...  0,0,len(all_tries)-1
    #then 0,1,len(all_tries)-1
    #     0,2,len(all_tries)-1
    #...  0,len(all_tries)-1,len(all_tries)-1
    #then 1,len(all_tries)-1,len(all_tries)-1
    #then 2,len(all_tries)-1,len(all_tries)-1
    #...  len(all_tries)-1,len(all_tries)-1,len(all_tries)-1

    def anagram_helper(letter_bank, wildcards, tries, selected_words):
        if len(tries) == 1:
            if find_subsets:
                #TODO: test this
                for (w, _) in tries[0].find_subsets(letter_bank, wildcards):
                    if test and not test(selected_words+[w]): continue
                    yield [w]
            else:
                for (w, _) in tries[0].find(letter_bank, wildcards):
                    if test and not test(selected_words+[w]): continue
                    yield [w]
        else:
            for (w1, _) in tries[0].find_subsets(letter_bank, wildcards):
                cntr, failures = counter_diff_with_failures(Counter(letter_bank),Counter(w1))
                new_bank = counter_to_list(cntr)
                new_wc = wildcards - failures
                if test and not test(selected_words+[w1]): continue #test on first iteration
                for word_list in anagram_helper(new_bank, new_wc, tries[1:], selected_words + [w1]):
                    if test and not test(selected_words + [w1] + word_list): continue
                    yield [w1] + word_list

    for i in range(word_cnt*len(all_tries) - word_cnt + 1):
        trie_ids = [i - j*len(all_tries) for j in range(word_cnt)]
        trie_ids = [min(max(0,idx),len(all_tries)-1) for idx in trie_ids]
        tries = [all_tries[idx] for idx in trie_ids]

        for words in anagram_helper(letter_bank, wildcards, tries, []):
            yield(words)



if __name__ == "__main__":
    WORD_CNT = 1
    progress = [] #[([indices],score)]

    #try to find three words that fit the anagram

    letter_bank = list("OXEORELION".lower())
    wildcards = 3

    t = Trie(list)
    WIKI_DATASET = "/home/jtrigg/files/misc/word_list.txt"

    cnt = 0
    with open(WIKI_DATASET) as fin:
        reader = csv.reader(fin)
        for r in reader:
            #only read in relevant words
            letters = r[0].replace(" ","")

            #NOTE: "" is counted as a word, which means any search for k
            #words will automatically include fewer words

            #IMPORTANT: memory issues are binding, need to limit the
            #amount of input words to <50k if possible
            if (len(letters) > 16): continue
            _, failures = counter_diff_with_failures(Counter(letter_bank),Counter(letters))
            if failures > 3: continue

            cnt += 1
            #load into the trie
            l = list(letters)
            val = (letters,r)
            t.insert(l, val)

    #TODO: create tries for each 2**k top scoring words?
    #starting with ~2**10
    #all_tries = [trie_2_10, trie_2_11, ...]
    all_tries = [t]

    def test_function(w):
        all_letters = [l for word in w for l in word]
        if len(all_letters) >= 1 and all_letters[0] != "o":
            return False
        if len(all_letters) >= 3 and all_letters[2] not in ["x","e"]:
            return False
        if len(all_letters) >= 5 and all_letters[4] not in ["x","e"]:
            return False
        if len(all_letters) >= 7 and all_letters[6:] != list("orelion")[:len(all_letters)-6]:
            return False
        return True

    #find_anagrams(['e', 'e', 'i', 'l', 'n', 'o', 'o', 'r'],2,2,[t])
    writer = csv.writer(sys.stdout)
    for words in find_anagrams(letter_bank,3,wildcards,[t], test=test_function):
        score = sum([math.log(int(v[1][1])) for w in words for v in t.find(list(w)) if v[1]])
        writer.writerow([words, score])
