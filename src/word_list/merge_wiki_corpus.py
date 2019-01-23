#merge the visit counts from the wikipedia pages
#with the word counts from the corpus
import csv
import sys

#spitballing for a couple similar words between datasets (eg country names) it looks like the wikipedia articles are sampled 6x more?
#so multiply the word_freq by 6 and add / merge
if __name__ == "__main__":
    cnts = {}

    CORPUS_MULTIPLIER = 6
    #corpus
    with open(sys.argv[1]) as fin:
        reader = csv.reader(fin)
        for r in reader:
            cnts[r[0]] = 6 * int(r[1])

    #wiki visits
    with open(sys.argv[2]) as fin:
        reader = csv.reader(fin)
        for r in reader:
            cnts[r[0]] = int(r[1]) + cnts.get(r[0],0)

    cnts = sorted(cnts.items(),key=lambda x: x[1], reverse=True)

    writer = csv.writer(sys.stdout)
    for [word,cnt] in cnts:
        writer.writerow([word,cnt])
