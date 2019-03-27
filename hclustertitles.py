import clusters

docs,words,data=clusters.readfile('titles_vectors.txt')

clust=clusters.hcluster(data,distance=clusters.pearson)
print ('clusters by pearson correlation')
clusters.printhclust(clust,labels=docs)
clusters.drawdendrogram(clust,docs,jpeg='docsclust_pearson.jpg')

clust=clusters.hcluster(data,distance=clusters.tanimoto)
print ('clusters by tanimoto coefficient')
clusters.printhclust(clust,labels=docs)
clusters.drawdendrogram(clust,docs,jpeg='docsclust_tanimoto.jpg')

clust=clusters.hcluster(data,distance=clusters.euclidean)
print ('clusters by euclidean distance')
clusters.printhclust(clust,labels=docs)
clusters.drawdendrogram(clust,docs,jpeg='docsclust_euclidean.jpg')

clust=clusters.hcluster(data,distance=clusters.cosine)
print ('clusters by euclidean distance')
clusters.printhclust(clust,labels=docs)
clusters.drawdendrogram(clust,docs,jpeg='docsclust_cosine.jpg')