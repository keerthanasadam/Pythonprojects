#!/usr/bin/env python

from optparse import OptionParser
import os,logging
from collections import defaultdict
import utils
import operator

def create_model(sentences):
    ## YOUR CODE GOES HERE: create a model
    tagmodel=defaultdict(lambda:defaultdict(int))
    for sentence in sentences:
        for token in sentence:
            tagmodel[token.word][token.tag]+=1
    #print(tagmodel)   
   
    return tagmodel

def predict_tags(sentences, model):
    ## YOU CODE GOES HERE: use the model to predict tags for sentences
    for sentence in sentences:
        for token in sentence:
            ## you can access token.word and self.tag (see utils.py for details)
            if model.has_key(token.word):
                token.tag=max(model[token.word].iteritems(), key=operator.itemgetter(1))[0]
            else:
                token.tag = "NN"
            
    return sentences

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
