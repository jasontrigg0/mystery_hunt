import sys
import re
import csv

if __name__ == "__main__":
    infile = sys.argv[1]
    with open(infile) as fin:
        reader = csv.reader(fin, delimiter=',')
        writer = csv.writer(sys.stdout)
        cnts = {}
        for r in reader:
            w = r[0].strip()
            w = re.sub("_\(.*\)$","",w) #drop suffix _(.*)
            w = w.replace("_"," ") #"_" -> " "
            w = w.lower()
            if not re.findall("^[a-z ]+$",w):
                continue
            cnts[w] = cnts.get(w,0) + int(r[1])
        for k in cnts:
            writer.writerow([k,cnts[k]])
