from PIL import Image,ImageDraw
from math import *
import random
import operator
import sys

def readfile(file_name):
    f = open(file_name)
    lines=[line for line in f]
  
    # First line is the column titles
    colnames=lines[0].strip().split('\t')[:]
    print(colnames)
    rownames=[]
    data=[]
    for line in lines[1:]:
        p=line.strip().split('\t')
        # First column in each row is the rowname
        if len(p)>1:
            rownames.append(p[0])
            # The data for this row is the remainder of the row
            data.append([float(x) for x in p[1:]])
    return rownames,colnames,data


def rotatematrix(data):
    newdata=[]
    for i in range(len(data[0])):
        newrow=[data[j][i] for j in range(len(data))]
        newdata.append(newrow)
    return newdata


def print_2d_array(matrix):
    for i in range(len(matrix)):
        for j in range (len(matrix[i])):
            print (matrix[i][j], end = "")
        print('\n')


# different similarity metrics for 2 vectors
def manhattan(cluster,row):
    cluster = []
    row = []
    for n, val in enumerate(row):
        if val == -1:
            continue
        cluster.append(cluster[n])
        row.append(val)

    res=0
    dimensions=min(len(cluster),len(row))

    for i in range(dimensions):
        res+=abs(cluster[i]-row[i])

    return res


def euclidean(cluster,row):
    res=0
    dimensions=min(len(cluster),len(row))
    for i in range(dimensions):
        res+=pow(abs(cluster[i]-row[i]),2)

    return sqrt(float(res))


def cosine(cluster,row):
    dotproduct=0
    dimensions=min(len(cluster),len(row))

    for i in range(dimensions):
        dotproduct+=cluster[i]*row[i]

    clusterlen=0
    rowlen=0
    for i in range(dimensions):
        clusterlen+=cluster[i]*cluster[i]
        rowlen+=row[i]*row[i]

    clusterlen=sqrt(clusterlen)
    rowlen=sqrt(rowlen)

    return 1.0-(float(dotproduct)/(clusterlen*rowlen+0.0001))
  

def pearson(cluster,row):
    # Simple sums
    sum1=sum(cluster)
    sum2=sum(row)
  
    # Sums of the squares
    sum1Sq=sum([pow(v,2) for v in cluster])
    sum2Sq=sum([pow(v,2) for v in row])
  
    # Sum of the products
    pSum=sum([cluster[i]*row[i] for i in range(min(len(cluster),len(row)))])
  
    # Calculate r (Pearson score)
    num=pSum-(sum1*sum2/len(cluster))
    den=sqrt((sum1Sq-pow(sum1,2)/len(cluster))*(sum2Sq-pow(sum2,2)/len(cluster)))
    if den==0: return 1.0


    return 1.0-num/den


def tanimoto(cluster,row):

    c1,c2,shr=0,0,0

    for i in range(len(cluster)):
        if cluster[i]!=0: c1+=1 # in cluster
        if row[i]!=0: c2+=1 # in row
        if cluster[i]!=0 and row[i]!=0: shr+=1 # in both

    return 1.0-(float(shr)/(c1+c2-shr))


# Hierarchical clustering
class bicluster:
    def __init__(self,vec,left=None,right=None,distance=0.0,id=None):
        self.left=left
        self.right=right
        self.vec=vec
        self.id=id
        self.distance=distance


def hcluster(rows,distance=euclidean):
    distances={}
    currentclustid=-1
    rowcopy = [row[2:] for row in rows]
    sums = [0]*len(rowcopy[0])
    avgs = []
    for m, row in enumerate(rowcopy):
        for n, col in enumerate(row):
            try: rowcopy[m][n] = int(col)
            except: continue
    avgs = [s/len(rowcopy[0]) for s in sums]
    for m, row in enumerate(rowcopy):
        for n, col in enumerate(row):
            if col == '':
                rowcopy[m][n] = avgs[n]

    # Clusters are initially just the rows
    clust=[bicluster(rowcopy[i],id=i) for i in range(len(rowcopy))]

    while len(clust)>1:
        lowestpair=(0,1)
        closest=distance(clust[0].vec,clust[1].vec)

        # loop through every pair looking for the smallest distance
        for i in range(len(clust)):
            for j in range(i+1,len(clust)):
                # distances is the cache of distance calculations
                if (clust[i].id,clust[j].id) not in distances:
                    distances[(clust[i].id,clust[j].id)]=distance(clust[i].vec,clust[j].vec)

                d=distances[(clust[i].id,clust[j].id)]

                if d<closest:
                    closest=d
                    lowestpair=(i,j)

        # calculate the average of the two clusters
        mergevec=[
            (clust[lowestpair[0]].vec[i]+clust[lowestpair[1]].vec[i])/2.0
                    for i in range(len(clust[0].vec))]

        # create the new cluster
        newcluster=bicluster(mergevec,left=clust[lowestpair[0]],
                             right=clust[lowestpair[1]],
                             distance=closest,id=currentclustid)

        # cluster ids that weren't in the original set are negative
        currentclustid-=1
        del clust[lowestpair[1]]
        del clust[lowestpair[0]]
        clust.append(newcluster)

    return clust[0]

def printhclust(clust,labels=None,n=0):
    # indent to make a hierarchy layout
    for i in range(n):
        print (' ', end="")
    if clust.id<0:
    # negative id means that this is branch
        print ('-')
    else:
    # positive id means that this is an endpoint
        if labels==None: print (clust.id)
        else:
            print(labels[clust.id])

    # now print the right and left branches
    if clust.left!=None: printhclust(clust.left,labels=labels,n=n+1)
    if clust.right!=None: printhclust(clust.right,labels=labels,n=n+1)


# draw hierarchical clusters
def getheight(clust):
    # Is this an endpoint? Then the height is just 1
    if clust.left==None and clust.right==None: return 1

    # Otherwise the height is the same of the heights of
    # each branch
    return getheight(clust.left)+getheight(clust.right)


def getdepth(clust):
    # The distance of an endpoint is 0.0
    if clust.left==None and clust.right==None: return 0

    # The distance of a branch is the greater of its two sides
    # plus its own distance
    return max(getdepth(clust.left),getdepth(clust.right))+clust.distance


def drawdendrogram(clust,labels,jpeg='clusters.jpg'):
    # height and width
    h=getheight(clust)*20
    w=1200
    depth=getdepth(clust)

    # width is fixed, so scale distances accordingly
    scaling=float(w-150)/depth

    # Create a new image with a white background
    img=Image.new('RGB',(w,h),(255,255,255))
    draw=ImageDraw.Draw(img)

    draw.line((0,h/2,10,h/2),fill=(255,0,0))

    # Draw the first node
    drawnode(draw,clust,10,(h/2),scaling,labels)
    img.save(jpeg,'JPEG')


def drawnode(draw,clust,x,y,scaling,labels):
    if clust.id<0:
        h1=getheight(clust.left)*20
        h2=getheight(clust.right)*20
        top=y-(h1+h2)/2
        bottom=y+(h1+h2)/2
        # Line length
        ll=clust.distance*scaling
        # Vertical line from this cluster to children
        draw.line((x,top+h1/2,x,bottom-h2/2),fill=(255,0,0))

        # Horizontal line to left item
        draw.line((x,top+h1/2,x+ll,top+h1/2),fill=(255,0,0))

        # Horizontal line to right item
        draw.line((x,bottom-h2/2,x+ll,bottom-h2/2),fill=(255,0,0))

        # Call the function to draw the left and right nodes
        drawnode(draw,clust.left,x+ll,top+h1/2,scaling,labels)
        drawnode(draw,clust.right,x+ll,bottom-h2/2,scaling,labels)
    else:
        # If this is an endpoint, draw the item label
        draw.text((x+5,y-7),labels[clust.id],(0,0,0))


# k-means clustering
def kcluster(rows,distance=euclidean,k=2):
    # Determine the minimum and maximum values for each point
    ranges = []
    if type(rows[0][0]) == str:
        if str.isalpha(rows[0][0]):
            rowcopy = [row[2:] for row in rows]
        else: rowcopy = rows
    else: rowcopy = rows
    for i in range(len(rowcopy[0])):
        sys.stdout.flush()
        runningmin = int(rowcopy[0][i])
        runningmax = int(rowcopy[0][i])
        for j, row in enumerate(rowcopy):
            for n in range(len(row)):
                try: row[n] = int(row[n])
                except:
                    row[n] = -1
                    continue
            if type(row[i]) != int:
                continue
            if row[i] < runningmin:
                runningmin = row[i]
            if row[i] > runningmax:
                runningmax = row[i]
        ranges.append((runningmin, runningmax))

    #ranges=[(min([row[i] for row in rows]),max([row[i] for row in rows]))
    #for i in range(len(rows[0]))]

    #for j in range(k):
    #    for i in range(len(rows[0])):
    #        clusters.append([random.random()])
    # Create k randomly placed centroids

    clusters=[[random.random()*(ranges[i][1]-ranges[i][0])+ranges[i][0] for i in range(len(rowcopy[0]))] for j in range(k)]

    lastmatches = None
    bestmatches = None

    for t in range(100):
        bestmatches=[[] for i in range(k)]

        # Find which centroid is the closest for each row
        for j in range(len(rowcopy)):
            row=rowcopy[j]
            bestmatch = 0
            for i in range(k):
                ncluster = []
                bcluster = []
                nrow = []
                for n, val in enumerate(row):
                    if val == -1:
                        continue
                    ncluster.append((clusters[i])[n])
                    bcluster.append((clusters[bestmatch][n]))
                    nrow.append(val)
                d = distance(ncluster,nrow)
                if d<distance(bcluster,nrow): bestmatch=i
            bestmatches[bestmatch].append(j)

        # If the results are the same as last time, this is complete
        if bestmatches==lastmatches: break
        lastmatches=bestmatches
    
        # Move the centroids to the average of their members
        for i in range(k):
            avgs=[0.0]*(len(rowcopy[0]))
            if len(bestmatches[i])>0:
                for rowid in bestmatches[i]:
                    for m, val in enumerate(rowcopy[rowid]):
                        if val == -1:
                            continue
                        avgs[m]+= val
                for j in range(len(avgs)):
                    avgs[j]/=len(bestmatches[i])
                clusters[i]=avgs
    return bestmatches, clusters

def sse(cluster, members):
    total = 0
    for member in members:
        ccopy = []
        cmember = []
        for n, val in enumerate(member):
            if val == '':
                continue
            ccopy.append(cluster[n])
            cmember.append(member[n])
        cmember = list(map(int, cmember))
        oof = list(map(operator.sub, ccopy, cmember))
        total += sum(list(num*num for num in oof))
    return total

def bisectingk(rows, distance, k):
    if type(rows[0][0]) == str:
        if str.isalpha(rows[0][0]):
            rowcopy = [row[2:] for row in rows]
        else: rowcopy = rows
    else: rowcopy = rows
    bestmatches, coordinates = kcluster(rows, distance, 2)
    k -= 1
    while k > 1:
        lcluster = []
        lerror = 0
        clusterind = 0

        totalsse = 0

        for r in range(len(bestmatches)):
            sumsq = sse(coordinates[r], [rowcopy[num] for num in range(len(bestmatches[r]))])
            if sumsq > lerror:
                lerror = sumsq
                clusterind = r
            totalsse += sumsq
        totalsse -= lerror
        for member in bestmatches[clusterind]:
            lcluster.append(rowcopy[member])

        bestmatches2, coordinates2 = kcluster(lcluster, distance, 2)
        for h, cluster in enumerate(bestmatches2):
            for i, member in enumerate(cluster):
                bestmatches2[h][i] = bestmatches[clusterind][member]
        del bestmatches[clusterind]
        del coordinates[clusterind]
        bestmatches = bestmatches + bestmatches2
        coordinates = coordinates + coordinates2
        k -= 1


    return bestmatches, coordinates, totalsse/k


def scaledown(data,distance=pearson,rate=0.01):
    n=len(data)

    # The real distances between every pair of items
    realdist=[[distance(data[i],data[j]) for j in range(n)]
             for i in range(0,n)]

    # Randomly initialize the starting points of the locations in 2D
    loc=[[random.random(),random.random()] for i in range(n)]
    fakedist=[[0.0 for j in range(n)] for i in range(n)]
  
    lasterror=None
    for m in range(0,1000):
        # Find projected distances
        for i in range(n):
            for j in range(n):
                fakedist[i][j]=sqrt(sum([pow(loc[i][x]-loc[j][x],2)
                                 for x in range(len(loc[i]))]))
  
        # Move points
        grad=[[0.0,0.0] for i in range(n)]
    
        totalerror=0
        for k in range(n):
            for j in range(n):
                if j==k: continue
                # The error is percent difference between the distances
                errorterm=(fakedist[j][k]-realdist[j][k])/realdist[j][k]
        
                # Each point needs to be moved away from or towards the other
                # point in proportion to how much error it has
                grad[k][0]+=((loc[k][0]-loc[j][0])/fakedist[j][k])*errorterm
                grad[k][1]+=((loc[k][1]-loc[j][1])/fakedist[j][k])*errorterm

                # Keep track of the total error
                totalerror+=abs(errorterm)
        print ("Total error:",totalerror)

        # If the answer got worse by moving the points, we are done
        if lasterror and lasterror<totalerror: break
        lasterror=totalerror
    
        # Move each of the points by the learning rate times the gradient
        for k in range(n):
            loc[k][0]-=rate*grad[k][0]
            loc[k][1]-=rate*grad[k][1]

    return loc


def draw2d(data,labels,jpeg='mds2d.jpg'):
    img=Image.new('RGB',(2000,2000),(255,255,255))
    draw=ImageDraw.Draw(img)
    for i in range(len(data)):
        x=(data[i][0]+0.5)*1000
        y=(data[i][1]+0.5)*1000
        draw.text((x,y),labels[i],(0,0,0))
    img.save(jpeg,'JPEG')

