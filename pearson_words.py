import clusters

docs,words,data=clusters.readfile('titles_vectors.txt')
distance_func = clusters.pearson

print()
print("Pearson coefficient between words")
wordvectors=clusters.rotatematrix(data)

for i in range(len(wordvectors)-1):
    for j in range(i+1, len(wordvectors)):
        dist=distance_func(wordvectors[i], wordvectors[j])
        sim=1.0-dist
        print('distance between words <'+words[i-1]+'> and <'+words[j-1]+'>=',
          dist, ', and similarity =',sim)