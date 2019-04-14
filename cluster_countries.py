from clusters import *
import csv
import json

data = []
with open('country_dimensions.csv') as csvfile:
    creader = csv.reader(csvfile, delimiter=',')
    for row, line in enumerate(creader):
        if row == 0:
            continue
        data.append(list(line))

num_clusters = 6
print ('Grouping words into {} clusters with bisecting k-means:'.format(num_clusters))

print()
clust, _, error = bisectingk(data,distance=pearson,k=num_clusters)
print ('clusters by pearson correlation')
print ("sum of squared errors:" + str(error))
print(clust)
for i in range(num_clusters):
    print("cluster {}".format(i+1))
    print([data[r][1] for r in clust[i]])

results = []
for i in range(num_clusters):
    results.append([data[r][1] for r in clust[i]])
fresults = [["Region", "Cluster"]]
for n, cluster in enumerate(results):
    for country in cluster:
        fresults.append([country, n])

jresults = json.dumps(fresults)
with open('data.js', 'w') as output:
    output.write("var results =")
    output.write(jresults)


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
print ('Grouping words into {} clusters with hierarchical clustering:'.format(num_clusters))

print()
clust = hcluster(data,distance=pearson)
print('clusters by pearson correlation')
drawdendrogram(clust, [row[0] for row in data], "hclusters_pearson.jpg")

print()
clust = hcluster(data,distance=tanimoto)
print ('clusters by tanimoto coefficient')
drawdendrogram(clust, [row[0] for row in data], "hclusters_tanimoto.jpg")

print()
clust = hcluster(data,distance=euclidean)
print ('clusters by euclidean distance')
drawdendrogram(clust, [row[0] for row in data], "hclusters_euclidean.jpg")

print()
clust = hcluster(data,distance=cosine)
print ('clusters by cosine distance')
drawdendrogram(clust, [row[0] for row in data], "hclusters_cosine.jpg")
"""