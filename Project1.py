#Author: Tian Wang
#Feb 21 2016

import numpy
from scipy import sparse
from scipy import linalg
from numpy.linalg import inv
from operator import itemgetter, attrgetter, methodcaller

#Read the tfidf matrix from txt file
TFIDFMatrix = open('matrix.txt','r')
# line.split() split() uses spaces as the delimiter
# line.strip() Remove left and right spaces.
#list comprehension with brackets and for loop in it
temp1 = [map(float,line.split()) for line in TFIDFMatrix if line.strip() != ""]
#create an array with whose __array__ method returns an array
A = numpy.array(temp1)

#Read the vocabulary matrix from txt file
indexList = open('index.txt', 'r')
temp2 = [map(str,line.split()) for line in indexList if line.strip() != "" ]
#print temp2[0]

query = ['computer','multicast','error','fear','prove','yicheng','professor','zoom','mouth','www']
runQueryDocResultComputer = []
runQueryDocResultMulticast = []
runQueryDocResultError = []
runQueryDocResultFear = []
runQueryDocResultProve = []
runQueryDocResultYicheng = []
runQueryDocResultProfessor = []
runQueryDocResultZoom = []
runQueryDocResultMouth = []
runQueryDocResultWww = []

for line in open("resultComputer.txt"):
    columns = line.split()
    runQueryDocResultComputer.append(columns[2])
    print columns[2]
print('#################################################################################')
for line in open("resultMulticast.txt"):
    columns = line.split()
    runQueryDocResultMulticast.append(columns[2])
    print columns[2]
print('#################################################################################')
for line in open("resultError.txt"):
    columns = line.split()
    runQueryDocResultError.append(columns[2])
    print columns[2]
print('#################################################################################')
for line in open("resultFear.txt"):
    columns = line.split()
    runQueryDocResultFear.append(columns[2])
    print columns[2]
print('#################################################################################')
for line in open("resultProve.txt"):
    columns = line.split()
    runQueryDocResultProve.append(columns[2])
    print columns[2]
print('#################################################################################')
for line in open("resultYicheng.txt"):
    columns = line.split()
    runQueryDocResultYicheng.append(columns[2])
    print columns[2]
print('#################################################################################')
for line in open("resultProfessor.txt"):
    columns = line.split()
    runQueryDocResultProfessor.append(columns[2])
    print columns[2]
print('#################################################################################')
for line in open("resultZoom.txt"):
    columns = line.split()
    runQueryDocResultZoom.append(columns[2])
    print columns[2]
print('#################################################################################')
for line in open("resultMouth.txt"):
    columns = line.split()
    runQueryDocResultMouth.append(columns[2])
    print columns[2]
print('#################################################################################')
for line in open("resultWww.txt"):
    columns = line.split()
    runQueryDocResultWww.append(columns[2])
    print columns[2]
print('#################################################################################')

# Factorize the Matrix A into U, S, V
U, S, V = numpy.linalg.svd(A,full_matrices=False)
#print U.shape, S.shape, V.shape
recallResultList = []
precisionResultList = []
kList=[1,10,50,100,150,200,250,300,350,400,450,500,550,600,650,700,750,800,1000,1500,2000]
for k in kList:
    print k
    sumRecall = 0
    sumPrecision = 0
    for term in query:
        print term
        #Set K value on U S V
        Uk = U[:,:k]
        Sk = S[:k]
        Vk = V[:k,:]
        #Extract a diagonal or construct a diagonal array.
        diagonalS = numpy.diag(Sk)
        #Calculate the inversed matrix of S
        inverseS = inv(diagonalS)
        #print Uk
        #print inverseS

        queryVectorlist = []
        for item in temp2[0]:
            if item in query:
                queryVectorlist.append(1)
            else:
                queryVectorlist.append(0)
        #create the query vectory array
        queryVector = numpy.array(queryVectorlist)
        #print queryVector.shape

        #the order of multiplication between matrix matters!
        queryVector = numpy.dot(queryVector,Uk)
        queryVector = numpy.dot(queryVector,inverseS)
        cosSimiList =[]
        cosSimiDocList = []

        #shape is an attribute of numpy and returns the dimensions of the array: 1 for column
        for i in range(Vk.shape[1]):
            #Calculate the cosine similarity value
            #Transpose the ith row
            #the expression Reference to the StackOverflow
            cosValue = numpy.dot(queryVector,Vk.T[i])/linalg.norm(queryVector)/linalg.norm(Vk.T[i])
            cosSimiList.append((cosValue,i))

        #print cosValue, i
        #sort the cosSimiList with its value
        cosSimiList = sorted(cosSimiList,key=itemgetter(0),reverse=True)
        cosSimiDocList = [row[1] for row in cosSimiList if row[0] > 0]

        common = []
        statistics = []
        if str(term) == 'computer':
            for i in range(len(cosSimiDocList)):
                for j in range(len(runQueryDocResultComputer)):
                    if int(cosSimiDocList[i]) == int(runQueryDocResultComputer[j]):
                        common.append(runQueryDocResultComputer[j])
            print common
            print "Relevant retrieved: ", len(common)
            print "All relevant: ", len(runQueryDocResultComputer)
            print "All retrieved: ", len(cosSimiDocList)
            recall = round((float(len(common)) / float(len(runQueryDocResultComputer))), 8)
            precision = round((float(len(common)) / float(len(cosSimiDocList))), 8)
            print "Recall: ",recall * 100, "%"
            print "Precision: ", precision * 100, "%"
            sumRecall += recall
            sumPrecision += precision
            print('#################################################################################')
        elif str(term) == 'multicast':
            for i in range(len(cosSimiDocList)):
                for j in range(len(runQueryDocResultMulticast)):
                    if int(cosSimiDocList[i]) == int(runQueryDocResultMulticast[j]):
                        common.append(runQueryDocResultMulticast[j])
            print common
            print "Relevant retrieved: ", len(common)
            print "All relevant: ", len(runQueryDocResultMulticast)
            print "All retrieved: ", len(cosSimiDocList)
            recall = round((float(len(common)) / float(len(runQueryDocResultMulticast))), 8)
            precision = round((float(len(common)) / float(len(cosSimiDocList))), 8)
            print "Recall: ",recall * 100, "%"
            print "Precision: ", precision * 100, "%"
            sumRecall += recall
            sumPrecision += precision
            print('#################################################################################')
        elif str(term) == 'error':
            for i in range(len(cosSimiDocList)):
                for j in range(len(runQueryDocResultError)):
                    if int(cosSimiDocList[i]) == int(runQueryDocResultError[j]):
                        common.append(runQueryDocResultError[j])
            print common
            print "Relevant retrieved: ", len(common)
            print "All relevant: ", len(runQueryDocResultError)
            print "All retrieved: ", len(cosSimiDocList)
            recall = round((float(len(common)) / float(len(runQueryDocResultError))), 8)
            precision = round((float(len(common)) / float(len(cosSimiDocList))), 8)
            print "Recall: ",recall * 100, "%"
            print "Precision: ", precision * 100, "%"
            sumRecall += recall
            sumPrecision += precision
            print('#################################################################################')
        elif str(term) == 'fear':
            for i in range(len(cosSimiDocList)):
                for j in range(len(runQueryDocResultFear)):
                    if int(cosSimiDocList[i]) == int(runQueryDocResultFear[j]):
                        common.append(runQueryDocResultFear[j])
            print common
            print "Relevant retrieved: ", len(common)
            print "All relevant: ", len(runQueryDocResultFear)
            print "All retrieved: ", len(cosSimiDocList)
            recall = round((float(len(common)) / float(len(runQueryDocResultFear))), 8)
            precision = round((float(len(common)) / float(len(cosSimiDocList))), 8)
            print "Recall: ",recall * 100, "%"
            print "Precision: ", precision * 100, "%"
            sumRecall += recall
            sumPrecision += precision
            print('#################################################################################')
        elif str(term) == 'prove':
            for i in range(len(cosSimiDocList)):
                for j in range(len(runQueryDocResultProve)):
                    if int(cosSimiDocList[i]) == int(runQueryDocResultProve[j]):
                        common.append(runQueryDocResultProve[j])
            print common
            print "Relevant retrieved: ", len(common)
            print "All relevant: ", len(runQueryDocResultProve)
            print "All retrieved: ", len(cosSimiDocList)
            recall = round((float(len(common)) / float(len(runQueryDocResultProve))), 8)
            precision = round((float(len(common)) / float(len(cosSimiDocList))), 8)
            print "Recall: ",recall * 100, "%"
            print "Precision: ", precision * 100, "%"
            sumRecall += recall
            sumPrecision += precision
            print('#################################################################################')
        elif str(term) == 'yicheng':
            for i in range(len(cosSimiDocList)):
                for j in range(len(runQueryDocResultYicheng)):
                    if int(cosSimiDocList[i]) == int(runQueryDocResultYicheng[j]):
                        common.append(runQueryDocResultYicheng[j])
            print common
            print "Relevant retrieved: ", len(common)
            print "All relevant: ", len(runQueryDocResultYicheng)
            print "All retrieved: ", len(cosSimiDocList)
            recall = round((float(len(common)) / float(len(runQueryDocResultYicheng))), 8)
            precision = round((float(len(common)) / float(len(cosSimiDocList))), 8)
            print "Recall: ",recall * 100, "%"
            print "Precision: ", precision * 100, "%"
            sumRecall += recall
            sumPrecision += precision
            print('#################################################################################')
        elif str(term) == 'professor':
            for i in range(len(cosSimiDocList)):
                for j in range(len(runQueryDocResultProfessor)):
                    if int(cosSimiDocList[i]) == int(runQueryDocResultProfessor[j]):
                        common.append(runQueryDocResultProfessor[j])
            print common
            print "Relevant retrieved: ", len(common)
            print "All relevant: ", len(runQueryDocResultProfessor)
            print "All retrieved: ", len(cosSimiDocList)
            recall = round((float(len(common)) / float(len(runQueryDocResultProfessor))), 8)
            precision = round((float(len(common)) / float(len(cosSimiDocList))), 8)
            print "Recall: ",recall * 100, "%"
            print "Precision: ", precision * 100, "%"
            sumRecall += recall
            sumPrecision += precision
            print('#################################################################################')
        elif str(term) == 'zoom':
            for i in range(len(cosSimiDocList)):
                for j in range(len(runQueryDocResultZoom)):
                    if int(cosSimiDocList[i]) == int(runQueryDocResultZoom[j]):
                        common.append(runQueryDocResultZoom[j])
            print common
            print "Relevant retrieved: ", len(common)
            print "All relevant: ", len(runQueryDocResultZoom)
            print "All retrieved: ", len(cosSimiDocList)
            recall = round((float(len(common)) / float(len(runQueryDocResultZoom))), 8)
            precision = round((float(len(common)) / float(len(cosSimiDocList))), 8)
            print "Recall: ",recall * 100, "%"
            print "Precision: ", precision * 100, "%"
            sumRecall += recall
            sumPrecision += precision
            print('#################################################################################')
        elif str(term) == 'mouth':
            for i in range(len(cosSimiDocList)):
                for j in range(len(runQueryDocResultMouth)):
                    if int(cosSimiDocList[i]) == int(runQueryDocResultMouth[j]):
                        common.append(runQueryDocResultMouth[j])
            print common
            print "Relevant retrieved: ", len(common)
            print "All relevant: ", len(runQueryDocResultMouth)
            print "All retrieved: ", len(cosSimiDocList)
            recall = round((float(len(common)) / float(len(runQueryDocResultMouth))), 8)
            precision = round((float(len(common)) / float(len(cosSimiDocList))), 8)
            print "Recall: ",recall * 100, "%"
            print "Precision: ", precision * 100, "%"
            sumRecall += recall
            sumPrecision += precision
            print('#################################################################################')
        elif str(term) == 'www':
            for i in range(len(cosSimiDocList)):
                for j in range(len(runQueryDocResultWww)):
                    if int(cosSimiDocList[i]) == int(runQueryDocResultWww[j]):
                        common.append(runQueryDocResultWww[j])
            print common
            print "Relevant retrieved: ", len(common)
            print "All relevant: ", len(runQueryDocResultWww)
            print "All retrieved: ", len(cosSimiDocList)
            recall = round((float(len(common)) / float(len(runQueryDocResultWww))), 8)
            precision = round((float(len(common)) / float(len(cosSimiDocList))), 8)
            print "Recall: ",recall * 100, "%"
            print "Precision: ", precision * 100, "%"
            sumRecall += recall
            sumPrecision += precision
            print('#################################################################################')
    averageRecall = float(sumRecall / len(query))
    averagePrecision = float(sumPrecision /len(query))
    recallResultList.append(averageRecall)
    precisionResultList.append(averagePrecision)
    print('-----------------------------------------------------------------------------------------------')

recallResultList = numpy.array(recallResultList)
precisionResultList = numpy.array(precisionResultList)
print "AverageRecallList: ",recallResultList, "\n"
print "AveragePrecisionList: ",precisionResultList, "\n"
print "Max average recall value: ", max(recallResultList), " where k is: ", kList[numpy.argmax(recallResultList)]
print "Max average precision value: ", max(precisionResultList), " where k is: ", kList[numpy.argmax(precisionResultList)]

TFIDFMatrix.close()
indexList.close()