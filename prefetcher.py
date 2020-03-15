import sys
import math
#######################################
# stride prefetcher
#######################################

def input(file):                              # takeinputing the input file as a combined memory
    global fetches
    fetches=0
    total = []
    with open(file) as f:                            # open file
        lines = f.readlines()
        for line in lines:
            fetches=fetches+1
            if(fetches<4000000):
                data = line.split(' ')
                t = int(data[2], 16)
                total.append(t)

    print("Total fetches : " +str(fetches))
    return[total]



def prefetch(tot):
    i=0
    b=0
    j=0
    for a in range(2000000):
        if(a>5 and a<2000000):
            tmat[b][0] = tot[a]
            tmat[b+1][0] = tot[a+1]
            tmat[b][1]=tot[a]-tot[a-1]
            tmat[b+1][1]=tot[a]-tot[a-2]
            tmat[b][2]=tmat[b][0]+tmat[b][1]
            tmat[b+1][2]=tmat[b][0]+tmat[b+1][1]


            if(tot[a+1]==tmat[b][2]):
                tmat[b][0]=tmat[b][2]
                tmat[b][2]=tmat[b][0]+tmat[b][1]
                tmat[b][3] = tmat[b][3]+1

                if (tmat[b][3] >= 3000):
                    i=i+1


            if(tot[a+1]==tmat[b+1][2]):
                tmat[b+1][0]=tmat[b+1][2]
                tmat[b+1][2]=tmat[b][0]+tmat[b+1][1]
                tmat[b+1][3] =tmat[b+1][3] +1

                if (tmat[b+1][3] >= 3000):

                    j=j+1

        b=b+2
        if (b >= 32):
            b = 0;

    print("Prefetched Hit rate "+str(j))



def cache_sim(tot):                                                                 # takeinputing the entire data
    miss = 0
    hit = 0
    prefetch(tot)
    for addr in tot:                                                               # using the hit and miss counter
        if counter(addr) is 1:
            hit += 1
        else:
            miss = miss + 1
    print("Total misses : " + str(miss))
    print("Total miss rate : " + str((miss)/(fetches)*100))
    print("Total hits : " + str(hit))
    print("Total hit rate : " + str((hit) / (fetches)*100))
	
	
def counter(addr):
    val=[]
    i=0
    trace = addr
    addr_length = 48
    offsetlen = int(math.log(block, 2))                                            # separate offset
    Index_len = int(math.log(cache / (assoc * block), 2))                          # separate index
    Tag_len = addr_length - offsetlen - Index_len                                  # separate tag
    maskTag = int(('1' * Tag_len + '0' * Index_len + '0' * offsetlen), 2)          # mask tag
    tag =(trace & maskTag) >> (Index_len + offsetlen)                              # shift to get tag value
    maskIndex = int(('0' * Tag_len + '1' * Index_len + '0' * offsetlen), 2)        # mask index
    index = (trace & maskIndex) >> (offsetlen)                                     # shift to get tag value
    mask = int(('1' * Tag_len + '1' * Index_len + '0' * offsetlen), 2)             # mask tag
    all = (trace & mask) >> (offsetlen)                                            # shift to get tag value

    if tag in tagmatrix[index]:                                                    # check tag matrix
        empty = tagmatrix[index].index(tag)                                        # if empty then put the called tag
        replacementmatrix[index][empty] = max(replacementmatrix[index]) + 1        # increment LRU counter
        return 1
    else:
        if 0 in tagmatrix[index]: 
            empty = tagmatrix[index].index(0)
            tagmatrix[index][empty] = tag
            replacementmatrix[index][empty] = max(replacementmatrix[index]) + 1     # increment LRU counter

        else:
            lru = min(replacementmatrix[index]) 
            lru_tag = replacementmatrix[index].index(lru)
            tagmatrix[index][lru_tag] = tag
            replacementmatrix[index][lru_tag] = max(replacementmatrix[index]) + 1   # increment LRU counter

        return 0
