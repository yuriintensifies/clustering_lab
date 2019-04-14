from __future__ import print_function
warned_of_error = False
import csv
from nltk.corpus import stopwords
import pygame
import simplejson
from pytagcloud import create_tag_image, make_tags
import clusters

def create_cloud (oname, words,maxsize=120, fontname='Lobster'):
    '''Creates a word cloud (when pytagcloud is installed)
    Parameters
    ----------
    oname : output filename
    words : list of (value,str)
    maxsize : int, optional
        Size of maximum word. The best setting for this parameter will often
        require some manual tuning for each input.
    fontname : str, optional
        Font to use.
    '''

    # gensim returns a weight between 0 and 1 for each word, while pytagcloud
    # expects an integer word count. So, we multiply by a large number and
    # round. For a visualization this is an adequate approximation.


    #words = [(w,int(v*10000)) for w,v in words]
    tags = make_tags(words, maxsize=maxsize)
    create_tag_image(tags, oname, size=(1800, 1200), fontname=fontname)


def main():
    data = []
    with open('country_dimensions.csv') as csvfile:
        creader = csv.reader(csvfile, delimiter=',')
        for row, line in enumerate(creader):
            if row == 0:
                continue
            data.append(list(line))

    if type(data[0][0]) == str:
        if str.isalpha(data[0][0]):
            rowcopy = [row[2:] for row in data]
        else: rowcopy = data
    else: rowcopy = data
    for i in range(len(rowcopy[0])):
        for j, row in enumerate(rowcopy):
            for n in range(len(row)):
                try: row[n] = int(row[n])
                except: continue

    clust, _, _ = clusters.bisectingk(data, distance=clusters.pearson, k=6)

    word_counts = {}
    with open('dimensions_keywords.csv') as csvfile:
        csvreader = csv.reader(csvfile, delimiter=',', quotechar='"')

        count = 0
        high, low = [], []
        for n, row in enumerate(csvreader):
            if n == 0:
                continue
            high.append(row[1].split())
            low.append(row[2].split())

        #which cluster to do word cloud on
        x = 5
        print(high)

        cent = clust[x]
        for member in cent:
            for i, dim in enumerate(rowcopy[member]):
                if dim == '':
                    continue
                score = dim - 50
                if score > 0:
                    for j, word in enumerate(high[i]):
                        if word not in word_counts:
                            word_counts[word] = score
                            continue
                        word_counts[word] += score
                if score < 0:
                    for k, word in enumerate(low[i]):
                        if word not in word_counts:
                            word_counts[word] = -score
                            continue
                        word_counts[word] += -score



    word_counts = [(w,count/10) for w,count in word_counts.items()]
    create_cloud('cluster{}_wordcloud.png'.format(x+1), word_counts)


if __name__ == "__main__":
    main()


