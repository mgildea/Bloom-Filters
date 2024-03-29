# -*- coding: utf-8 -*-
#argparse allows the parsing of command line arguments
import argparse
#utility functions for the bloom filter project
import bfProjectUtils as util
#numpy numerical library - use for random values only
import numpy.random as random
#USAGE : 
#random.seed(x) : sets seed to x
#random.randint(a,b) : returns random integer in range [a,b) (inclusive beginning and exclusive ending values)


class HashType1(object):
    #Implement Hash Type 1
    
    def __init__(self, config, genHashes):
        """
        Args:
            config (dictionary) : contains configuration data for this hashing object 
            genHashes (boolean) : whether or not to generate new hash seeds/coefficients 
                                    (Task 2 provides hash seeds/coefficients, 
                                    Tasks 1 and 3 require you to make them yourself) 
        """
        self.k = config['k']
        self.n = config['n']
        #set random seed to be generated seed at config load
        #random.seed(config['genSeed'])
        #if generate new random hashes
        if genHashes :
             #set random seed to be generated seed at config load
            random.seed(config['genSeed'])
            self.seeds = random.randint(config['N'], size=self.k).tolist()
          
            #build seed list self.seeds
            #pass
        #if not gen (task 2), then use hashes that are in config dictionary
        else :
            self.seeds = config['seeds']
    
    def getHashList(self, x):
        """
        Return list of k hashes of the passed integer, using self.seeds[i]+x to 
        seed random number gen to give i'th hash value
        Args :
            x (int) : element to hash
        Returns list of k hashes of this element
        """
        res = []

        for seed in self.seeds:
            random.seed(seed + x)
            res.append(random.randint(0, self.n))


        ''' for seed in self.seeds:
            random.seed(seed + x)
            
        res = random.randint(self.n, size=self.k).tolist()
 '''
        #your code goes here
        return res


class HashType2(object):
    #Implement Hash Type 2

    def __init__(self, config, genHashes):
        """
        Args:
            config (dictionary):contains configuration data for this hashing object            
            genHashes (boolean) : whether or not to generate new hash seeds/coefficients 
                                    (Task 2 provides hash seeds/coefficients, 
                                    Tasks 1 and 3 require you to make them yourself) 
        """
        self.k = config['k']
        self.n = config['n']
        self.N = config['N']
        self.P = util.findNextPrime(self.N)
        #generate new random hashes, or not if task2
        if genHashes :
            #set random seed to be generated seed at config load
            random.seed(config['genSeed'])
            #build lists of coefficients self.a and self.b

            self.a = random.randint(1, config['N'], size=self.k).tolist()
            self.b = random.randint(0, config['N'], size=self.k).tolist()

        #if not gen (task 2), then use hashes that are in config dictionary
        else :
            self.a = config['a']
            self.b = config['b']           
            
            
    def getHashList(self, x):
        """
        Return list of k hashes of the passed integer, using 
        (self.a[i] * x + self.b[i] mod P) mod n 
        to give i'th hash value - remember P and n must be prime, and P >= N
        
        Args :
            x (int) : element to hash
        Returns list of k hashes of this element
        """
        res = []
    
        for a,b in zip(self.a, self.b):
        #for i in xrange(self.k):
            res.append((((a * x) + b) % self.P) % self.n)
            #random.seed((((a * x) + b) % self.P) % self.n)
            #random.seed(((self.a[i] * x + self.b[i]) % self.P) % self.n)
            #res.append(random.randint(0,self.n))
        
       # res = random.randint(self.n, size=self.k).tolist()
        #your code goes here
        return res
    
    


class BloomFilter(object):     
    #Implement a Bloom Filter data structure."""

    def __init__(self, config):
        """        
        Args:
            config (dictionary): Configuration of this bloom filter
            config['N'] (int) universe size
            config['m'] (int) number of elements to add to filter
            config['n'] (int) number of bits in bloom filter storage array
            config['k'] (int) number of hash functions to use
            config['task'] (int) the task this bloom filter is to perform (1,2,3)
            config['type'] (int) type of hash function (1, 2, -1==unknown type)
            if type 1 hash :
                config['seeds'] (list of k ints) : seed values for k hash functions for type 1 hash function
            if type 2 hash : 
                config['a'] (list of k ints) : a coefficients for k hash functions for type 2 hash function
                config['b'] (list of k ints) : b coefficients for k hash functions for type 2 hash function
            
            genHashes (boolean) : whether or not to generate new hash seeds/coefficients 
                                    (Task 2 provides hash seeds/coefficients, 
                                    Tasks 1 and 3 require you to make them yourself) 
        """
        #task this boom filter is performing
        self.task = config['task']
        #task 1 and 3 reguire generated seeds for hashes, task 2 uses provided seeds/coefficients
        genHashes = (self.task != 2)
        #type of hash for this bloom filter
        self.type = config['type']
        if(self.type == 1):
            self.hashFunc = HashType1(config,genHashes)
        elif(self.type == 2):
            self.hashFunc = HashType2(config,genHashes)
        #elif(self.type == 3): #add your own hashes
        else:
            print('BloomFilter for task ' + str(self.task) + ' ctor : Unknown Hash type : ' + str(self.type))
            
        
        #your code goes here
        self.table = [False] * config['n']

    def add(self, x):
        """Adds x to the data structure, using self.hashFunc     
        Args:
            x (int): The integer to add to the bloom filter
        """
        for h in self.hashFunc.getHashList(x):
            self.table[h] = True
    

    def contains(self, x):
        """Indicates whether data structure contains x, using self.hashFunc, with the possibility of false positives
        
        Args:
            x (int): The integer to test.
        Returns:
            True or False whether structure contains x or not
        """
                
        for h in self.hashFunc.getHashList(x):
            if(not self.table[h]):
                return False
        
        return True




"""
function will take data list, insert first m elements into bloom filter, and check all elements in datalist for membership, returning a list of results of check
    Args : 
        data (list) : list of integer data to add 
        bf (object) : bloom filter object
        m (int) : number of elements to add to bloom filter from data (first m elements)
    Returns : 
        list of results of checking 
    
"""
def testBF(data, bf, m):
    #add first m elements
    for i in range(0,m):
        bf.add(data[i]) 
    print('Finished adding '+ str(m) +' integers to bloom filter')
    resList =[]
    #test membership of all elements
    for i in range(0,len(data)):
        resList.append(str(bf.contains(data[i])))
    return resList


"""
function will support required test for Task 2.  DO NOT MODIFY.
    configData : dictionary of configuration data required to build and test bloom filter
"""
def task2(configData):        
    #instantiate bloom filter object    
    bf = BloomFilter(configData)    

    #bfInputData holds a list of integers.  Using these values you must :
    #   insert the first configData['m'] of them into the bloom filter
    #   test all of them for membership in the bloom filter
    bfInputData = util.readIntFileDat(configData['inFileName'])
    if(len(bfInputData) == 0):
        print('No Data to add to bloom filter')
        return
    else :
        print('bfInputData has '+str(len(bfInputData)) +' elements')
    #testBF will insert elements and test membership
    outputResList = testBF(bfInputData, bf, configData['m'])            
    #write results to output file
    util.writeFileDat(configData['outFileName'],outputResList)
    #load appropriate validation data list for this hash function and compare to results    
    util.compareResults(outputResList,configData)    
    print('Task 2 complete')    



def task1Tests(configData, inputData, hashType):
    numTests = configData['iterations']
    results = [[0] * configData['n'] for x in xrange(numTests)]
    stats = [None] * numTests

    print hashType.__name__,'running',numTests,'tests of',configData['m'],'records each'

    for i, result in enumerate(results):
        hashList = []
        configData['genSeed'] =  random.randint(0, configData['N'])
        hashFunc = hashType(configData,True)

        for j in xrange(configData['m']):
            for h in hashFunc.getHashList(inputData[j]):
                result[h] = result[h] + 1
                hashList.append(h)

        util.writeFileDat("task1Output/" + hashType.__name__ + "/Iter" + str(i) +".txt", hashList)

    print('Done generating data')

    return results

def task1Stats(results,hashType):
    
    print('generating stats')
    statistics = [dict() for x in xrange(len(results))]

    for i,result in enumerate(results):
        statistics[i]['maxCollisions'] = max(result)
        #statistics[i][0] = maxCollisions
       

        #hashList = []
        bucketUsage = [0]*(statistics[i]['maxCollisions'] + 1)
        for k,j in enumerate(result):
            bucketUsage[j] = bucketUsage[j] + 1
            #if(j > 0):
            #    hashList.append(k)

        statistics[i]['bucketUsage'] = bucketUsage
        #util.writeFileDat("task1Output/" + hashType.__name__ + "/Iter" + str(i) +".txt", hashList)

        totalCollisions = 0
        for j in xrange(len(statistics[i]['bucketUsage'])):
            if(j > 1):
                totalCollisions = totalCollisions + (statistics[i]['bucketUsage'][j])*(j-1)

        statistics[i]['totalCollisions'] = totalCollisions

   

    print('done generating stats')
    return statistics






"""     
these two functions are added for your convenience, if you choose to use this code to perform tasks 1 and 3
"""     
def task1(configData):
    #if you wish to use this code to perform task 1, you may do so
    #NOTE : task 1 does not require you to instantiate a bloom filter
    
    bfInputData = util.readIntFileDat(configData['inFileName'])
    if(len(bfInputData) == 0):
        print('No Data to add to bloom filter')
        return
    else :
        print('bfInputData has '+str(len(bfInputData)) +' elements')

    task1Data = task1Tests(configData, bfInputData, HashType1)
    type1Results = task1Stats(task1Data, HashType1)
    util.writeFileDat("task1Output/" + HashType1.__name__ + "/Stats.txt", type1Results)

    task2Data = task1Tests(configData, bfInputData, HashType2)
    type2Results = task1Stats(task2Data, HashType2)
    util.writeFileDat("task1Output/" + HashType2.__name__ + "/Stats.txt", type2Results)

    #type1AveResults = dict()
    total = 0
    for result in type1Results:
        total = total + result['totalCollisions']

    type1AverageCollisions = total / len(type1Results)
    print 'type 1 average collisions = ', type1AverageCollisions
    print 'type 1 average collision rate = ', type1AverageCollisions / float(configData['m'])

    total = 0
    for result in type2Results:
        total = total + result['totalCollisions']

    type2AverageCollisions = total / len(type2Results)
    print 'type 2 average collisions = ', type2AverageCollisions
    print 'typ1 2 average collision rate = ', type2AverageCollisions / float(configData['m'])
   

    print('Task 1 complete')


def testTask3(data, bf, m):

    numTests =  (len(data) - m)  
    print("Adding " + str(m) + " distinct integers to bloom filter, then testing " + str(numTests) + " new integers")
    fpCount = 0
    for i,input in enumerate(data):
        if(i < m):
            bf.add(input)
        else:
            if bf.contains(input):
                fpCount = fpCount + 1

    fpRate = float(fpCount) / numTests          


    print("False-Postive rate: " + str(fpRate))
    return fpRate


def task3(configData):
    #if you wish to use this code to perform task 3, you may do so
    #NOTE task 3 will require you to remake your bloom filter multiple times to perform the appropriate trials
    #this will necessitate either making a new bloom filter constructor or changing the config dictionary to 
    #hold the appropriate values for k and n (filter size) based on c value, derived as in the notes
    #REMEMBER for type 2 hashes n must be prime.  util.findNextPrime(n) is provided for you to use to find the next largest
    #prime value of some integer.
    
    bfInputData = util.readIntFileDat(configData['inFileName'])

    results = []
    for t in range(1,3):
     
        print("Type " + str(t) + ":")
        for c in xrange(10,16,5):
            result = dict()
            result['Type'] = t
            result['c'] = c
            result['k-fpRate'] = []
            print("c = "+ str(c) + ":")
            for k in range(4,11):
                print("k = " + str(k) + ":")
                configData['type'] = t
                configData['k'] = k
                configData['n'] = util.findNextPrime(configData['m'] * c)

                cumFpRate = 0
                for i in range(0,configData['iterations']):
                    configData['genSeed'] =  random.randint(0, configData['N'])
                    cumFpRate = cumFpRate + testTask3(bfInputData, BloomFilter(configData), configData['m'])
                      
                aveFpRate = cumFpRate / configData['iterations']
                print("Type " + str(t) + ", c="+ str(c) +", k="+ str(k) + ", ave. fp rate=" + str(aveFpRate))

                result['k-fpRate'].append(aveFpRate)
            
            results.append(result)

    util.writeFileDat("task3Output/results.txt", results)
    print('Task 3 complete')    
    

"""     
main
"""     
def main():	
    #DO NOT REMOVE ANY ARGUMENTS FROM THE ARGPARSER BELOW
    parser = argparse.ArgumentParser(description='BloomFilter Project')
    parser.add_argument('-c', '--configfile',  help='File holding configuration of Bloom Filter', default='testConfigHashType2.txt', dest='configFileName')
    parser.add_argument('-i', '--infile',  help='Input file of data to add to Bloom Filter', default='testInput.txt', dest='inFileName')
    parser.add_argument('-o', '--outfile',  help='Output file holding Bloom Filter results', default='testOutput.txt', dest='outFileName')	
    #you may use this argument to distinguish between tasks - default is task 2 - do not change
    #you are not required to use this code template for tasks 1 and 3.
    parser.add_argument('-t', '--task',  help='Which task to perform (1,2,3)', type=int, choices=[1, 2, 3], default=2, dest='taskToDo')	
    parser.add_argument('-v', '--valfile',  help='Validation file holding Bloom Filter expected results', default='validResHashType2.txt', dest='valFileName')	
    
    #args for autograder, do not modify
    parser.add_argument('-n', '--sName',  help='Student name, used by autograder', default='GT', dest='studentName')	
    parser.add_argument('-a', '--autograde',  help='Autograder-called (2) or not (1=default)', type=int, choices=[1, 2], default=1, dest='autograde')	
    args = parser.parse_args()
        
    #configData is a dictionary that holds the important info needed to build your bloom filter
    #this includes the hash functon coefficients for the hash calculation for Task 2 (do not use these for Tasks 1 and 3)
    #buildBFConfigStruct prints out to the console all the elements in configData
    configData = util.buildBFConfigStruct(args) 
    
    #perform appropriate task - 2 is default and the task2 code execution will be tested for your grade    
    if configData['task'] == 2 :
        task2(configData)
    elif configData['task'] == 1 :
        #you are not required to use this code template for tasks 1 and 3.
        task1(configData)
    elif configData['task'] == 3 :
        #you are not required to use this code template for tasks 1 and 3.
        task3(configData)
    else :
        print ('Unknown Task : ' + str(configData['task']))  



if __name__ == '__main__':
    main()
    