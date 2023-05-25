import nltk,string,pickle
from nltk.stem.lancaster import LancasterStemmer
stemmer = LancasterStemmer()
from autocorrect import Speller
spell=Speller(lang='en')

import numpy
import tflearn
import tensorflow
import random,wikipedia
# MODEL CREATE
redo=1
import json
file=open("intents.json")
data = json.load(file)

# PRE PROCESSING
try:
    f   = open('data.pickle','rb')
    words,labels,training,output    = pickle.load(f)
except:
    words = []
    labels = []
    docs_x = []
    docs_y = []

    for intent in data['intents']:
        #   Label collection     
        labels.append(intent['tag'])
        
        #   words collection
        for pattern in intent['patterns']:
            #   Tokenization
            wrds = nltk.word_tokenize(pattern)
            words.extend(wrds)
            docs_x.append(wrds)
            docs_y.append(intent["tag"])

    #   Stem the words and remove the duplicates
    words   = [stemmer.stem(w.lower()) for w in words if w!=string.punctuation] 
    words   = sorted(list(set(words)))

    #   Sorting the labels
    labels  = sorted(labels)

    # print(words,len(words))
    # print(labels)
    # print(docs_x,len(docs_x))
    # print(docs_y,len(docs_y))

    training    = []
    output      = []

    out_empty   = [0 for _ in range(len(labels))]

    # BAG OF WORD
    for x,doc in enumerate(docs_x):
        bag     = []

        wrds    = [stemmer.stem(w) for w in doc]

        for w in words:
            if w in wrds:
                bag.append(1)
            else:
                bag.append(0)

        out_row                             = out_empty[:]
        out_row[labels.index(docs_y[x])]    = 1
        
        training.append(bag)
        output.append(out_row)

    training    = numpy.array(training)
    output      = numpy.array(output)

    f   = open('data.pickle','wb')
    pickle.dump((words,labels,training,output),f)

# print("INPUT data with shape")
# print(training,training.shape)
# print("OUTPUT data with shape")
# print(output,output.shape)
# print(len(training[0]))

#   clearing previus data in our model
tensorflow.compat.v1.reset_default_graph()

#   Setting up of neural network
# IP LAYER
net     = tflearn.input_data(shape=[None,len(training[0])])
# HIDDEN LAYER
net     = tflearn.fully_connected(net,8)
net     = tflearn.fully_connected(net,8)
# OP LAYER
net     = tflearn.fully_connected(net,len(output[0]),activation='softmax')
net     = tflearn.regression(net)

# testing and debugging
# -----------------------
# print(len(training[0]))
# print(len(output[0]))

#   Train our model
model   = tflearn.DNN(net)


if (redo==1):
    model.fit(X_inputs=training,Y_targets=output,n_epoch=1900,batch_size=8,show_metric=True)
    model.save('model.tflearn') 
else:
    model.load('model.tflearn')

# print(training)
# print(output)


def bag_of_words(s,words):
    bag     = [0 for i in range(len(words))]
    # print(words)
    s_words =nltk.word_tokenize(s)
    # print(s_words)
    s_words = [stemmer.stem(w.lower()) for w in s_words if w!=string.punctuation]
    # print(s_words)

    for sw in s_words:
        for i,w in enumerate(words):
            # if sw=='shop':
                # print(w,sw)
            if w==sw:
                bag[i]=1
    return numpy.array(bag)
    # print(bag)
# print(bag_of_words('name of a shop',words))


def chat(inp):
    # print("Start talking with the bot . . .")
    
    # BELOW COMMENTS USED FOR TESTING AND DEBUGGING 
    # while True:
        # inp     = input("You: ")
        
        # if inp.lower()=='quit':
        #     break
        c=''
        result          = model.predict([bag_of_words(inp,words)])
        result_index    = numpy.argmax(result)
        tag             = labels[result_index]

        # DEBUGGING
        print(result,tag)
        responses=[]
        if(result[0][result_index]>.75):
            print("valid")
            for intent in data["intents"]:
                if intent['tag']==tag:
                    responses   = intent['responses']
                    c           = intent['context_set']
                    print("context:",c)
        else:
            print("invalid")        #DEBUGGING
            text=[]
            text = nltk.word_tokenize(inp)
            for i,value in enumerate(text):
                text[i]=spell(value)
            text = nltk.pos_tag(text)
            print(text)             # DEBUGGING
            for i in text:
                try:
                    # print(i[0])
                    if (i[1] in ('NNP', "NNS", "JJ", "NN", "VBN")) and (i[0] not in ("search", "meaning", "internet")):
                        # print("Not search,meaning,internet:\t",i[0])
                        if len(i[0])>2:
                            # print("Great than 2:\t",i[0])
                            def ans():
                                try:
                                    search=wikipedia.search(i[0])
                                    search=random.choice(search)
                                    return wikipedia.summary(title=search, sentences=1,auto_suggest=False)
                                except:
                                    ans()
                            responses.append(ans())
                except:
                    pass
                # print(responses)
                # input()
            if responses==[]:
                responses=['Nice, continue . . . ',"I am still in training phase, excuse me",'Kinda confused over here!!']
        return [random.choice(responses),c]
        # print(random.choice(responses))
