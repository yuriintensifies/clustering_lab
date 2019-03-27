import clusters

docs,words,data=clusters.readfile('titles_vectors.txt')
distance_func = clusters.cosine

similarity_matrix = []
similarity_matrix.append([])
similarity_matrix[0].append("     ")
padded_docs = ["{:<5}".format(d) for d in docs]
similarity_matrix[0].extend(padded_docs)

for i in range(1, len(data)+1):
    similarity_matrix.append([])
    similarity_matrix[i].append(docs[i-1])
    similarity_matrix[i].extend([' '*5]*len(data))

print("Cosine distance between documents")
for i in range (len(data) - 1):
    for j in range (i+1, len(data)):
        dist=distance_func(data[i],data[j])
        sim=1.0-dist
        similarity_matrix[i+1][j+1] = "{:<5}".format("{:.2f}".format(sim))


clusters.print_2d_array(similarity_matrix)


