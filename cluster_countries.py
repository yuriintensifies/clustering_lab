from clusters import *
import csv

data = []
with open('country_dimensions.csv') as csvfile:
    creader = csv.reader(csvfile, delimiter=',')
    for row, line in enumerate(creader):
        if row == 0:
            continue
        data.append(list(line))
print(data)
"""
num_clusters = 5
print ('Grouping words into {} clusters:'.format(num_clusters))

print()
clust, _, error = bisectingk(data,distance=pearson,k=num_clusters)
print ('clusters by pearson correlation')
print ("sum of squared errors:" + str(error))
for i in range(num_clusters):
    print("cluster {}".format(i+1))
    print([data[r][1] for r in clust[i]])

print()
clust, _, error = bisectingk(data,distance=tanimoto,k=num_clusters)
print ('clusters by tanimoto coefficient')
print ("sum of squared errors:" + str(error))
for i in range(num_clusters):
    print("cluster {}".format(i+1))
    print([data[r][1] for r in clust[i]])

print()
clust, _, error = bisectingk(data,distance=euclidean,k=num_clusters)
print ('clusters by euclidean distance')
print ("sum of squared errors:" + str(error))
for i in range(num_clusters):
    print("cluster {}".format(i+1))
    print([data[r][1] for r in clust[i]])

print()
clust, _, error = bisectingk(data,distance=cosine,k=num_clusters)
print ('clusters by cosine distance')
print ("sum of squared errors:" + str(error))
for i in range(num_clusters):
    print("cluster {}".format(i+1))
    print([data[r][1] for r in clust[i]])
"""
num_clusters = 5
print ('Grouping words into {} clusters:'.format(num_clusters))

print()
clust = hcluster(data,distance=pearson)
print ('clusters by pearson correlation')
for i in range(num_clusters):
    print("cluster {}".format(i+1))
    print([data[r][1] for r in clust[i]])

print()
clust = hcluster(data,distance=tanimoto)
print ('clusters by tanimoto coefficient')
for i in range(num_clusters):
    print("cluster {}".format(i+1))
    print([data[r][1] for r in clust[i]])

print()
clust = hcluster(data,distance=euclidean)
print ('clusters by euclidean distance')
for i in range(num_clusters):
    print("cluster {}".format(i+1))
    print([data[r][1] for r in clust[i]])

print()
clust = hcluster(data,distance=cosine)
print ('clusters by cosine distance')
for i in range(num_clusters):
    print("cluster {}".format(i+1))
    print([data[r][1] for r in clust[i]])
