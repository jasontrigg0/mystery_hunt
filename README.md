#tools for mystery_hunt

#frequency sorted word lists in src/word_list, including:
#wiki_1m.txt - a list of most common proper nouns (as measured by wikipedia page visits)
#corpus_1m.txt - a list of most common words (pulled from a corpus of wiki articles)
#word_list_1m.txt - the above two combined

#anagrammer tool
#generate list of k words that anagram to a given list
#(+ potentially several unknown 'wildcard' characters)
#uses tries to do it quickly

#note: for anagrams try something like easy like this first
#example searching 5-15 length windows of an input string for anagrams
#if this is too slow then anagrammer tool may word
#SEARCH=$(paste | pawk -p 'print(re.sub("[^a-z]","",l.lower()))'); echo $SEARCH; less /home/jtrigg/files/misc/word_list.txt | head -500000 | pawk -b 'search="'$SEARCH'"; g = GroupBy({},key=lambda x: tuple(sorted(Counter(x).items()))); for length in range(5,15): for i in range(len(search)-length+1): g.update([search[i:i+length]]); end;' -p 'w = r[0].strip().lower(); if w in g and g[w] != [w]: write_line([r[0],r[1],g[w]])' > /tmp/matches.csv