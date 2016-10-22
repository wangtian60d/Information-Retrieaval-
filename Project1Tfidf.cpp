//Author: Tim Wang
//Time: Feb 10 2016
//Search Engine: the retrieval model implemented is Latent Semantic Indexing 
// Indri information retrieval toolkit used

#include <ctime>
#include <cmath>
#include <iostream>
#include <iomanip>
#include "indri/Repository.hpp"
#include <fstream>
#include <stdlib.h>


//Calculate the TFIDF value
double calTfidf(indri::index::DocListIterator::DocumentData* doc, indri::index::TermData* termData, indri::index::Index* index){
    double termFrequency = (double)(doc->positions.size())/(index->documentLength(doc->document));
    double InverseDocFrequency = (double)log((index->documentCount())/(termData->corpus.documentCount));
    return termFrequency * InverseDocFrequency;
}

int main(int argc, char** argv){
    
    if(argc < 2){
        std::cout << "Please Input the Index list:\n";
        return -1;
    }

//Note: place the index files in the same folder as this file!
    std::string tfidfMatrixPath = "matrix.txt";
    std::string indexListPath = "index.txt";    
    indri::collection::Repository r;
    std::string indexPath = argv[1];

    
    if(argc == 3){
        tfidfMatrixPath = argv[2] + tfidfMatrixPath;
    }

    clock_t startTime = clock();

    //open the output file
    ofstream tfidfMatrix;
    ofstream indexList;
    tfidfMatrix.open(tfidfMatrixPath.c_str(), ios::out);
    indexList.open(indexListPath.c_str(), ios::out);
    //First
    //get the index from repository
    r.openRead(indexPath);
    
    //from print_invfile( indri::collection::Repository& r ) from dumpIndex.cpp line 121
    indri::collection::Repository::index_state state = r.indexes();
    indri::index::Index* index = (*state)[0];
    indri::index::DocListFileIterator* iter = index->docListFileIterator();
    iter->startIteration();
    
    //void print_invfile( indri::collection::Repository& r ) from dumpIndex.cpp line 123
    UINT64 totalDocument = index->documentCount();
    //void print_repository_stats( indri::collection::Repository& r ) from dumpIndex.cpp 425
    UINT64 totalTerm = index->uniqueTermCount();

    //void print_invfile( indri::collection::Repository& r ) from dumpIndex.cpp line125 for every word
    //it's going to populate the tfidf matrix horizontally, that is, for each term, calculate their tfidf in each document which is column of the matrix
    while(!iter->finished()){
        //Get the term 
        indri::index::DocListFileIterator::DocListData* entry = iter->currentEntry();
        indri::index::TermData* termData = entry->termData;
	    indexList << termData->term << " ";
        entry->iterator->startIteration();
        //void print_invfile( indri::collection::Repository& r ) from dumpIndex.cpp line 136
        indri::index::DocListIterator::DocumentData* doc = entry->iterator->currentEntry();
        
        char point[256]; 
        bool finish = false;
        //for each document
        //UINT64 can also be replaced with int in this case where total num of document is 2540
	    UINT64 i = 1;
        for(i = 1; i <= totalDocument; i++){
            //UINT64 i is too long that can't be compared with normal int doc->document, thus needs to be converted into char*[]
            sprintf(point, "%lu", i);
            //if ith document contains the word, calculate the tf-idf and output
            //convert the char*[] back to integer so that can be compared with doc->document
            //if their name are equal that means the current document is one of documents in the inverted term list where a certain term appears.
            if(finish != true && atoi(point) == (int)doc->document){
                //calculate the value of tf-idf of a term and then write it into a file
                tfidfMatrix << ' ' << calTfidf(doc, termData, index);
                //point horizontally to the next document in the tfidf matrix
                entry->iterator->nextEntry();
                //check if the iterator hits the /null or called the end of the first term row in the tfidf matrix
                //void print_invfile( indri::collection::Repository& r ) from dumpIndex.cpp line 135
                if(!entry->iterator->finished()){
                    //if not hits the end, change the current document pointer
                    doc = entry->iterator->currentEntry();
                }else{
                    finish = true;
                }
            }else{
                //if this(current) term does not appear in this document, then write 0 as tfidf value.
                tfidfMatrix << ' ' << 0;
            }
        }
        //not a delimiter and should not be specified as delimiter when use matlab dlmread() function.
        tfidfMatrix << std::endl;
        //point vertically to the next term in tfidf matrix
	    iter->nextEntry();
    }
    
    //The 'g' version move the get pointer, the 'p' versions move the put pointer.
    //If memory serves, a particular implementation may use a single pointer for both. 
    //However if you are about to perform input you should definitely use seekg(), and seekp() in the other case.

    tfidfMatrix.seekp(0, ios::beg);
    clock_t endTime = clock();
    clock_t clockTicksTaken = endTime - startTime;
    double timeInSeconds = clockTicksTaken / (double) CLOCKS_PER_SEC;
    std::cout << "Completed in: " << timeInSeconds << "seconds\n";
    delete iter;
    tfidfMatrix.close();
    indexList.close();
    r.close();
    
    return 0;
}
