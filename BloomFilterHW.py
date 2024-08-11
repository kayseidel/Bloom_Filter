from BitHash import BitHash
from BitVector import BitVector

class BloomFilter(object):
    # Return the estimated number of bits needed (N in the slides) in a Bloom 
    # Filter that will store numKeys (n in the slides) keys, using numHashes 
    # (d in the slides) hash functions, and that will have a
    # false positive rate of maxFalsePositive (P in the slides).
    # See the slides for the math needed to do this.  
    # You use Equation B to get the desired phi from P and d
    # You then use Equation D to get the needed N from d, phi, and n
    # N is the value to return from bitsNeeded
    def __bitsNeeded(self, numKeys, numHashes, maxFalsePositive):
        
        # find proportion of bits that are still 0 using equation B
        bitsStillZero = 1 - (maxFalsePositive**(1 / numHashes))
        
        # find number of bits needed using equation D
        numBits = numHashes / (1 - bitsStillZero**(1 / numKeys))
        
        return int(numBits) # change number of bits into an int
    
    # Create a Bloom Filter that will store numKeys keys, using 
    # numHashes hash functions, and that will have a false positive 
    # rate of maxFalsePositive.
    # All attributes must be private.
    def __init__(self, numKeys, numHashes, maxFalsePositive):
        # will need to use __bitsNeeded to figure out how big
        # of a BitVector will be needed
        # In addition to the BitVector, might you need any other attributes?
        self.__numKeys = numKeys
        self.__numHashes = numHashes
        self.__maxFalsePositive = maxFalsePositive
        
        self.__numBits = self.__bitsNeeded(numKeys, numHashes, maxFalsePositive)
        self.__bitVector = BitVector(size=self.__numBits)
        
        self.__bitsSet = 0  # attribute to keep track of how many bits are set
    
    # insert the specified key into the Bloom Filter.
    # Doesn't return anything, since an insert into 
    # a Bloom Filter always succeeds!
    # See the "Bloom Filter details" slide for how insert works.
    def insert(self, key):
        for i in range(1, self.__numHashes):
            a = BitHash(key, i) % self.__numBits # hash to find index to insert
            self.__bitVector[a] = 1              # set bit in that location
            self.__bitsSet += 1                  # increase # of bits set by 1
    
    # Returns True if key MAY have been inserted into the Bloom filter. 
    # Returns False if key definitely hasn't been inserted into the BF.
    # See the "Bloom Filter details" slide for how find works.
    def find(self, key):
        # loop for number of hashes
        for i in range(1, self.__numHashes):
            a = BitHash(key, i) % self.__numBits # hash to find index to check
            if self.__bitVector[a] == 0:         # if bit in this location in
                return False                     # vector isn't set, return False
        return True
       
    # Returns the PROJECTED current false positive rate based on the
    # ACTUAL current number of bits actually set in this Bloom Filter. 
    # This is NOT the same thing as trying to use the Bloom Filter and
    # measuring the proportion of false positives that are actually encountered.
    # In other words, you use equation A to give you P from d and phi. 
    # What is phi in this case? it is the ACTUAL measured current proportion 
    # of bits in the bit vector that are still zero. 
    def falsePositiveRate(self):
        
        # actual current proportion of bits in bit vector that are still zero
        bitsStillZero = (self.__numBits - self.numBitsSet()) / self.__numBits
        
        # find the projected false positive rate using equation A
        falsePosRate = (1 - bitsStillZero)**self.__numHashes
        
        return falsePosRate
       
    # Returns the current number of bits ACTUALLY set in this Bloom Filter
    # WHEN TESTING, MAKE SURE THAT YOUR IMPLEMENTATION DOES NOT CAUSE
    # THIS PARTICULAR METHOD TO RUN SLOWLY.
    def numBitsSet(self):
        return self.__bitsSet


def __main():
    numKeys = 100000
    numHashes = 4
    maxFalse = .05

    # create the Bloom Filter
    b = BloomFilter(numKeys, numHashes, maxFalse)

    t = open("wordlist.txt") # open text file
    
    # read the first numKeys words from the file and insert them 
    # into the Bloom Filter. Close the input file.
    for i in range(numKeys):
        word = t.readline()
        b.insert(word)
    
    t.close()                # close text file
    
    # Print out what the PROJECTED false positive rate should 
    # THEORETICALLY be based on the number of bits that ACTUALLY ended up being set
    # in the Bloom Filter. Use the falsePositiveRate method.
    print("The projected false positive rate is:", b.falsePositiveRate())

    # Now re-open the file, and re-read the same bunch of the first numKeys 
    # words from the file and count how many are missing from the Bloom Filter, 
    # printing out how many are missing. This should report that 0 words are 
    # missing from the Bloom Filter. Don't close the input file of words since
    # in the next step we want to read the next numKeys words from the file.
    t = open("wordlist.txt")
    
    count = 0
    for i in range(numKeys):
        word = t.readline()
        if b.find(word) == False:
            count += 1
    print(count, "words are missing from the Bloom Filter")

    # Now read the next numKeys words from the file, none of which 
    # have been inserted into the Bloom Filter, and count how many of the 
    # words can be (falsely) found in the Bloom Filter.
    count2 = 0
    for i in range(numKeys):
        word = t.readline()
        if b.find(word) == True:
            count2 += 1
    print(count2, "words can be falsely found in the Bloom Filter")
    
    # Print out the percentage rate of false positives.
    # THIS NUMBER MUST BE CLOSE TO THE ESTIMATED FALSE POSITIVE RATE ABOVE
    print("The percentage rate of false positives is:", (count2 / numKeys))

    
if __name__ == '__main__':
    __main()       

