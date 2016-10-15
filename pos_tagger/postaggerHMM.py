# -*- coding: utf-8 -*-
"""
Created on Thu Oct 06 20:30:36 2016

@author: keert
"""

#!/usr/bin/env python

from optparse import OptionParser
import os,logging
from collections import defaultdict
import utils
import re
def create_model(sentences):
    ## YOUR CODE GOES HERE: create a model
    model=[]
    wordtag=defaultdict(lambda:defaultdict(int))
    wordtag_count=defaultdict(lambda:defaultdict(int))
    bigramtag=defaultdict(lambda:defaultdict(int))
    unigramtag=defaultdict(int)
    wordcount=defaultdict(int)
    totalwordcount=0
    singlewordcount=0
    probunseenword=0.0
    tagset=[]
    wordlist=[]
    
    for sentence in sentences:
        unigramtag["<s>"]+=1
        bigramtag["<s>"][sentence[0].tag]+=1
        for i in range(len(sentence)-1):
            totalwordcount+=1
            unigramtag[sentence[i].tag]+=1
            wordcount[sentence[i].word]+=1
            bigramtag[sentence[i].tag][sentence[i+1].tag]+=1
            #wordtag_count[]
            wordtag[sentence[i].tag][sentence[i].word]+=1
            if not sentence[i].tag in tagset:
                tagset.append(sentence[i].tag)
            if sentence[i].word not in wordlist:
                wordlist.append(sentence[i].word)
        unigramtag[sentence[i+1].tag]+=1
        wordcount[sentence[i].word]+=1
        wordtag[sentence[i+1].tag][sentence[i+1].word]+=1
        if sentence[i+1].word not in wordlist:
            wordlist.append(sentence[i+1].word) 
        totalwordcount=totalwordcount+1
    dummytag=[]
    dummytag=['<s>']+tagset
    wordtag_count=wordtag
    wordlistset=set(wordlist)
    for k,v in wordcount.items():
        if v==1:
            singlewordcount+=1
    #print("bigram tag model: \n"+str(bigramtag))
    #print("word tag model:\n"+str(wordtag))
    #print(wordlist)
    for i in dummytag:
        for j in tagset:
            bigramtag[i][j]=float(bigramtag[i][j]+1)/(unigramtag[i]+len(tagset))
    for i in tagset:
        for j in wordlist:
                num=wordtag_count[i][j]
                den=unigramtag[i]
                #print(num,den)
                wordtag[i][j]=float((num + 0.0)/den)
                #print(wordtag[i][j])
   
    #print("prior model:\n"+str(bigramtag))
    #print("Likelihood model:\n"+str(wordtag)) 
    probunseenword=float(singlewordcount)/totalwordcount
    model.append(bigramtag)
    model.append(wordtag)
    model.append(tagset)
    model.append(wordlistset)
    model.append(probunseenword)
    #print("length of tagset:"+str(len(tagset)))
    #print(probunseenword)
    return model

def predict_tags(sentences, model):
    ## YOU CODE GOES HERE: use the model to predict tags for sentences
    prior=model[0]
    likelihood=model[1]
    tags=model[2]
    wordset=model[3]
    goodturingvalue=model[4]
    
    #viterbi=defaultdict(lambda:defaultdict(float))
    #viterbi2=defaultdict(lambda:defaultdict(list))
    priortagindex=0
    priorwordindex=0
    endtag=0
    tagpos=[] 
    for sentence in sentences:
        viterbi=[[0 for x in range(len(tags))] for y in range(len(sentence))] 
        viterbi2=[[[0 for z in range(2)]for x in range(len(tags))] for y in range(len(sentence))]
        for wordindex in range(len(sentence)):
            currentword=sentence[wordindex].word
            for tagindex in range(len(tags)):
                currenttag=tags[tagindex]
                if sentence[wordindex].word in wordset:
                    likelihoodvalue=likelihood[currenttag][currentword]
                else:
                    if (currenttag==tagForUnknownWord(sentence[wordindex].word)):
                        likelihoodvalue=goodturingvalue
                max=0.0
                if wordindex==0:
                    viterbi[wordindex][tagindex]= (likelihoodvalue)*(prior["<s>"][currenttag])
                    viterbi2[wordindex][tagindex]=[0,0]
                else:
                    for tagbefore in range(len(tags)):
                        viterbi[wordindex][tagindex]=((viterbi[wordindex-1][tagbefore])*(likelihoodvalue)*(prior[tags[tagbefore]][currenttag]))
                        if(max<viterbi[wordindex][tagindex]):
                            max=viterbi[wordindex][tagindex]
                            priortagindex=tagbefore
                            priorwordindex=wordindex-1
                    viterbi[wordindex][tagindex]=max
                    viterbi2[wordindex][tagindex]=[priorwordindex,priortagindex]
        for tokenindex in range(len(sentence)-1,-1,-1):
            if tokenindex==(len(sentence)-1): 
                currentendprob=0.0
                endtag=0
                for taglastindex in range(len(tags)):
                    if(currentendprob<viterbi[tokenindex][taglastindex]):
                       currentendprob= viterbi[tokenindex][taglastindex]
                       endtag=taglastindex
                sentence[tokenindex].tag=tags[endtag] 
            else:
               tagpos=viterbi2[tokenindex+1][endtag]
               sentence[tokenindex].tag=tags[tagpos[1]]
               endtag=tagpos[1]
        #for i in sentence:
    return sentences
def tagForUnknownWord(word):
    if(word == "."):
        tag="."                              
    elif(re.compile("^[a-z]+al$").match(word)):
        tag="JJ"
    elif(re.compile("^[a-z]+-[a-z]+$").match(word)):
        tag="JJ"                                                                         
    elif(re.compile("^[a-z]+al$").match(word)):
        tag="JJ"
    elif(re.compile("^[a-z]+es$").match(word)):
        tag="NNS"
    elif(re.compile("^[a-z]+ation$").match(word)):
        tag="NN"
    elif(re.compile("^[a-z]+ations$").match(word)):
        tag="NNS"
    elif(re.compile("a|an|the").match(word)):
        tag="DT"
    elif(re.compile("^[a-z]+ly$").match(word)):
        tag="RB"
    elif(re.compile("^[a-z]+ing$").match(word)):
        tag="VBG"
    elif(re.compile("^[a-z]+ed$").match(word)):
        tag="VBD"
    elif(re.compile("^[0-9]+$").match(word)):
        tag="CD"                                
    elif(re.compile("^[a-z]+ize$").match(word)):
        tag="VB"                                
    elif(re.compile("^[a-z]+ized").match(word)):
        tag="VBD" 
    else:
           if(str.endswith(word,"s")):
                tag="NNS"
           else:
                tag="NN"
    return tag
if __name__ == "__main__":
    usage = "usage: %prog [options] GOLD TEST"
    parser = OptionParser(usage=usage) 

    parser.add_option("-d", "--debug", action="store_true",
                      help="turn on debug mode")

    (options, args) = parser.parse_args()
    if len(args) != 2:
        parser.error("Please provide required arguments")

    if options.debug:
        logging.basicConfig(level=logging.DEBUG)
    else:
        logging.basicConfig(level=logging.CRITICAL)

    training_file = args[0]
    training_sents = utils.read_tokens(training_file)
    test_file = args[1]
    test_sents = utils.read_tokens(test_file)

    model = create_model(training_sents)
    
    ## read sentences again because predict_tags(...) rewrites the tags
    sents = utils.read_tokens(training_file)
    predictions = predict_tags(sents, model)
    accuracy = utils.calc_accuracy(training_sents, predictions)
    print "Accuracy in training [%s sentences]: %s" % (len(sents), accuracy)

    ## read sentences again because predict_tags(...) rewrites the tags
    sents = utils.read_tokens(test_file)
    predictions = predict_tags(sents, model)
    accuracy = utils.calc_accuracy(test_sents, predictions)
    print "Accuracy in training [%s sentences]: %s" % (len(sents), accuracy)
