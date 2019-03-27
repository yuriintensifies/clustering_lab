# Clustering: tutorial and lab
## Part I. Tutorial
### Clustering small documents

To run the code you need to install the graphics library Pillow-Pil - the same library which we used in the decision tree lab.
<ol>
  <li>
    Read file `titles.txt`. Each line represents a paper title. There are 2 evident clusters: the first cluster represents papers on Human-Computer Interaction, and the second one on Theory of Computing. 
  </li>
  <li>
    Convert documents into word matrix using `titles_to_vectors.py`.
  </li>
  <li>
    Explore different distance metrics by running `cosine_documents.py`, `pearson_documents.py`, and `tanimoto_documents.py`. What do you observe? Are you satisfied with the distances between each p[air of documents? Maybe using euclidean distance will give better results? Check it out.
  </li>
  <li>
    Create 2 clusters using k-means algorithm implemented in `clusters.py`. For this run `kmclustertitles.py`. Maybe if we change the number of clusters, the results will be better? Explore.
  </li>
  <li> Now cluster words by the documents where they occur by running `kmclusterwords.py`. It seems that this clustering works better. Why doo you think that is?
  </li>
  <li>Finally, try hierarchical clustering of documents by running `hclustertitles.py`. Hierarchical clustering seems to work much better. Why do you think that is?
  </li>
</ol>
