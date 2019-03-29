import clusters

docs,words,data=clusters.readfile('titles_vectors.txt')
distance_func = clusters.pearson

print()
print("Pearson correlation coefficient between words")
wordvectors=clusters.rotatematrix(data)

for i in range(len(wordvectors)-1):
    for j in range(i+1, len(wordvectors)):
        dist=distance_func(wordvectors[i], wordvectors[j])
        sim=1.0-dist
        print('Correlation between words <'+words[i]+
              '> and <'+words[j]+'>=',sim)