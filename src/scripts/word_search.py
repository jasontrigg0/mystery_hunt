import csv

six_letters = ["REPUTE","RASCAL","ALGIER","NAPLES","PYTHON","GODLEY","MOTOWN","FOODIE","SPOTON","COUSIN","MOTHER","FATHER","SISTER","HAAGEN","TRIFLE","STRAND","FIGARO","FAVELA","WAITER","MANTRA","MEDALS","BRILLO","BIGTOE","INSTEP","CANADA","BONITO","RUBBLE","VIRAGO","CENSOR","SCRIBE"]

triples = ["NEME"] #"IKS","TIT","OFT","NOL","SLA","SHA","FSA","EBR"]

def load_words(keep_spaces = False):
    words = {}
    cnt = 0
    with open("/tmp/word_list.txt") as f_in:
        reader = csv.reader(f_in)
        for row in reader:
            if not keep_spaces:
                row[0] = row[0].replace(" ","")
            words[row[0].upper()] = row[1]
            cnt += 1
            if cnt > 2000000: break
    return words

def word_search(words, fn):
    for w in words:
        if fn(w):
            print(w,words[w])

if __name__ == "__main__":
    words = load_words()

    word_search(words, lambda x: len(x) == 8 and x[:2] == "MI" and x[-1:] == "L")

    # for x in triples:
    #     for w in words:
    #         w = w.upper()
    #         forward_combo = w + w
    #         backward_combo = w[::-1] + w[::-1]
    #         if x in forward_combo:
    #             print(x,w,words[w])
    #         if x in backward_combo:
    #             print(x,w,words[w])
