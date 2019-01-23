#Wikipedia Corpus downloaded here:
#http://www.psych.ualberta.ca/%7Ewestburylab/downloads/westburylab.wikicorp.download.html
#total size: "990,248,478 words, over 2 million documents"

#taken from this list of NLP datasets:
#https://github.com/niderhoff/nlp-datasets
import re
import collections

def run_counter():
    # MAX_WORDS = float("inf") #100000000
    with open("/home/jtrigg/Downloads/WestburyLab/WestburyLab.Wikipedia.Corpus.txt") as fin:
        i = 0
        next_write = 2**20
        counter = collections.Counter()
        for l in fin:
            for w in l.split():
                w = re.sub("\.$","",w)
                w = re.sub(",$","",w)
                w = w.lower()
                if not re.findall("^[a-z]*$",w):
                    continue
                counter[w] += 1
                i += 1
                if i >= next_write:
                    write_counter(i,counter)
                    next_write = 2 * next_write
        write_counter(i,counter)

def write_counter(word_cnt, counter):
    with open("/tmp/word_freq_{word_cnt}.txt".format(**vars()),'w') as fout:
        for word, freq in counter.most_common():
            fout.write(str(word)+","+str(freq)+"\n")

if __name__ == "__main__":
    run_counter()
