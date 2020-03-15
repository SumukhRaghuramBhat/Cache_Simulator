import math
from trace_parse import traceParse
#######################################
# defining cache class & methods
#######################################


class Cache(object):
    def __init__(self, blockSize, cacheSize, associativity, replacementPolicy, writePolicy):
        self.config = {}
        self.config['blockSize'] = blockSize
        self.config['cacheSize'] = cacheSize
        self.config['associativity'] = associativity
        self.config['replacementPolicy'] = replacementPolicy
        self.config['writePolicy'] = writePolicy
        self.config['numBlocks'] = cacheSize / blockSize
        self.config['numWays'] = associativity
        self.config['numSets'] = cacheSize // (blockSize * associativity)

        # cache variables
        self.stats = {}
        self.stats['Reads'] = 0
        self.stats['ReadHits'] = 0
        self.stats['ReadMisses'] = 0
        self.stats['Writes'] = 0
        self.stats['WriteHits'] = 0
        self.stats['WriteMisses'] = 0

        # state matrices
        self.rows = self.config['numSets']
        self.cols = self.config['numWays']
        self.TAG_MAT = [([(1)] * self.cols) for row in range((self.rows))]
        self.VALID_MAT = [([0] * self.cols) for row in range((self.rows))]
        self.DIRTY_MAT = [([0] * self.cols) for row in range((self.rows))]
        self.LRU_MAT = [([0] * self.cols) for row in range((self.rows))]
        self.LFU_MAT = [([0] * self.cols) for row in range((self.rows))]

    #issue read function
    def issueRead(self, address):
        return None

    #issue write function
    def issueWrite(self, address):
        return None

    def decodeAddress(self, address):
        # calclating length of tag, index & offset from cache configuration
        lenAddr = 32
        lenOffset = int(math.log(self.config['blockSize'], 2))
        lenIndex = int(math.log(self.config['numSets'], 2))
        lenTag = lenAddr - lenOffset - lenIndex
        trace = (int(address, 16))
        maskTag = int(('1' * lenTag + '0' * lenIndex + '0' * lenOffset), 2)
        tag = (trace & maskTag) >> (lenIndex + lenOffset)
        maskIndex = int(('0' * lenIndex + '1' *lenIndex + '0' * lenOffset), 2)
        index = (trace & maskIndex) >> (lenOffset)
        return (tag, index)

    def encodeAddress(self, tag, index):
        lenOffset = int(math.log(self.config['blockSize'], 2))
        lenIndex = int(math.log(self.config['numSets'], 2))
        address = (tag << (lenIndex + lenOffset)) + (index << lenOffset)
        return address

    def updateBlockUsed(self, index, way):
        # 0 for LRU
        if self.config['replacementPolicy'] == 0:
            self.LRU_MAT[index][way] = max(self.LRU_MAT[index]) + 1
        return None

    def chooseBlockToEvict(self, index):
        # 0 for LRU
        if self.config['replacementPolicy'] == 0:
            lru = min(self.LRU_MAT[index])
            lru_way = self.LRU_MAT[index].index(lru)
            return lru_way

    # read method
    def readFromAddress(self, currentAddress):
        (currentTag, currentIndex) = self.decodeAddress(currentAddress)
        self.stats['Reads'] += 1
        if self.config['writePolicy'] == 1:
            if (currentTag in self.TAG_MAT[currentIndex]) and self.VALID_MAT[currentIndex][self.TAG_MAT[currentIndex].index(currentTag)]:
                # Read Hit
                self.stats['ReadHits'] += 1
                foundWay = self.TAG_MAT[currentIndex].index(currentTag)
                # update matirces and counters
                self.updateBlockUsed(currentIndex, foundWay)
                return 1
            else:
                # Read Miss
                self.stats['ReadMisses'] += 1
                # if unused block, bring in block from next level, set V=1 & D=0
                if 0 in self.VALID_MAT[currentIndex]:
                    foundWay = self.VALID_MAT[currentIndex].index(0)
                    # bring in the block from next level
                    self.issueRead(self.encodeAddress(currentTag, currentIndex))
                    # update matirces and counters
                    self.VALID_MAT[currentIndex][foundWay] = 1
                    self.TAG_MAT[currentIndex][foundWay] = currentTag
                    self.updateBlockUsed(currentIndex, foundWay)
                else:
                    # if no unused block, evict LRU, allocate block, set V=1 & D=0, assign tag
                    foundWay = self.chooseBlockToEvict(currentIndex)
                    # if block not dirty, no worries, just bring in the block from next level
                    self.issueRead(self.encodeAddress(currentTag, currentIndex))
                    # update matirces and counters
                    self.VALID_MAT[currentIndex][foundWay] = 1
                    self.TAG_MAT[currentIndex][foundWay] = currentTag
                    self.updateBlockUsed(currentIndex, foundWay)
            return 0

    def writeToAddress(self, currentAddress):
        (currentTag, currentIndex) = self.decodeAddress(currentAddress)
        self.stats['Writes'] += 1
        # Wriye to cache
        if self.config['writePolicy'] == 1:
            if (currentTag in self.TAG_MAT[currentIndex]) and self.VALID_MAT[currentIndex][self.TAG_MAT[currentIndex].index(currentTag)]:
                self.stats['WriteHits'] += 1
                foundWay = self.TAG_MAT[currentIndex].index(currentTag)
                # Policy =1 =WTNA, write to cache, write to next level
                self.TAG_MAT[currentIndex][foundWay] = currentTag
                self.issueWrite(self.encodeAddress(currentTag, currentIndex))
                # update matirces and counters
                self.updateBlockUsed(currentIndex, foundWay)
                return 1
            else:
                # Write Miss
                self.stats['WriteMisses'] += 1
                self.issueWrite(self.encodeAddress(currentTag, currentIndex))
            return 0
