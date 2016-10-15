#!/usr/bin/env python
# -*- coding: utf-8 -*-
from optparse import OptionParser
import os, logging 
from collections import defaultdict
import math 
import re
def create_model(path):
    unigrams=defaultdict(int)
    bigrams=defaultdict(lambda:defaultdict(int))
    model=[]
    tokencount=0    
    f = open(path, 'r')
    for l in f.readlines():
        for token in l.split(' '):
            token='$'+token+'$'
            tokencount+=1
            token=token.lower()
            #preprocessing for removing punctuations           
            token=re.sub('[^0-9A-Za-zñáéíóúü]','',token)
            for i in range(len(token)-1):
                    unigrams[token[i]]+=1
                    bigrams[token[i]][token[i+1]]+=1
                    unigrams['$']+=1
    model.append(unigrams)
    model.append(bigrams)
    return model
def predict(file, model_en, model_es):
    prediction = None      
    prob_en=calc_prob(file,model_en)
    prob_es=calc_prob(file,model_es)    
    if(prob_en>prob_es):
        prediction='English'
    else:
        prediction="Spanish"
    return prediction
def calc_prob(file,model):
     model_uni=model[0]
     model_bi=model[1]
     prob=0.0
     f = open(file, 'r')
     for l in f.readlines():
        for token in l.split(' '):
            token='$'+token+'$'
            token=token.lower()
            token=re.sub('[^0-9A-Za-zñáéíóúü]','',token)
            # foe each bigram we check if it is present in train model if not we perform smoothing 
            for i in range(len(token)-1): 
                prob1=float(model_bi[token[i]][token[i+1]]+1)/(model_uni[token[i]]+27)
                prob+=math.log1p(prob1-1)
     return prob
def main(en_tr, es_tr, folder_te):
  ## STEP 1: create a model for English with file en_tr
    model_en = create_model(en_tr)
    ## STEP 2: create a model for Spanish with file es_tr
    model_es = create_model(es_tr)
    ## STEP 3: loop through all the files in folder_te and print prediction
    folder = os.path.join(folder_te, "en")
    print ("Prediction for English documents in test:")
    for f in os.listdir(folder):
        f_path =  os.path.join(folder, f)
        print ("%s\t%s" % (f, predict(f_path, model_en, model_es)))
    
    folder = os.path.join(folder_te, "es")
    print ("\nPrediction for Spanish documents in test:")
    for f in os.listdir(folder):
        f_path =  os.path.join(folder, f)
        print ("%s\t%s" % (f, predict(f_path, model_en, model_es)))

if __name__ == "__main__":
    usage = "usage: %prog [options] EN_TR ES_TR FOLDER_TE"
    parser = OptionParser(usage=usage)

    parser.add_option("-d", "--debug", action="store_true",
                      help="turn on debug mode")

    (options, args) = parser.parse_args()
    if len(args) != 3:
        parser.error("Please provide required arguments")

    if options.debug:
        logging.basicConfig(level=logging.DEBUG)
    else:
        logging.basicConfig(level=logging.CRITICAL)
    #main(os.path.abspath("data/train/en/all_en.txt"),os.path.abspath("data/train/es/all_es.txt"),os.path.abspath("data/test/"))
    main(args[0],args[1],args[2])