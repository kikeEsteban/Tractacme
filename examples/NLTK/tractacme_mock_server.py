#!/usr/bin/env python

import wikiquotes
import fileinput
import nltk
from nltk.corpus import stopwords
from nltk.probability import FreqDist

"""
 Process text using NLTK

The target is create a dictionary of words with associated sentences, and an array of sentences with the associated word list 

ie: 

Return the 10 most frequent words with their related sentences:

dictionay = {
    ...
    "love" : {"freq":2, "sents":[2,4]}, # indexes of the relative setence list
    "hate" : {"freq":2, "sents":[4,6]},
    ...
}

sentences = [
 {"text":"This is just the beginning"}, "words":["beginning"]},
 {"text":"And this is the second sentence","words":["sentence"]}
 {"text":"I want your love", "words":["love"]}
 {"text":"A guiven sentence ", "words":["sentence"]}   
 {"text":"love and hate is all what we feel", "words":["love","hate"]}
 {"text":"Element 14","words":[]}
 {"text":"I hate bananas","words":["hate"]}
 ...
]

"""

number_of_words = 3

def process_text(input_sentences, number_of_words):
    
    # Create a dictionary with the nouns arranged by frequency
    dictionary = {}
    noun_tokens = []
    fdist = FreqDist()

    # Create array of sentences with associated 
    all_sentences = []
    sentences = []
    for sentence in input_sentences :
        #print()
        #print(sentence)
        all_sentences.append({"text":sentence,"words":[]})
        tokens = nltk.word_tokenize(sentence)
        clean_tokens = []
        for token in tokens :
            if not token in stopwords.words('english'):
                clean_tokens.append(token.lower())
        # Filter by type of word or value (i.e. nouns and verbs, filter out specific words ...)
        tagged = nltk.pos_tag(clean_tokens,tagset='universal', lang='eng')
        for tag in tagged :
            if tag[1] == 'NOUN' and tag[0]!="i" and tag[0]!="—" and tag[0]!="]" and tag[0]!="[":
                noun_tokens.append(tag[0])
               
    # Frequency distribution of all the normalized words
    frequency_dist = nltk.FreqDist(noun_tokens)
    
    # Create the dictionary with
    dictionary = dict()
    for word, frequency in frequency_dist.most_common(number_of_words):
        sents = []
        for index in range(0,len(all_sentences)):
            tokens = nltk.word_tokenize(all_sentences[index]["text"])
            for token in tokens:
                if word == token.lower():
                    sents.append(index)
                    all_sentences[index]["words"].append(word)
                    break
        dictionary[word] = {"freq":frequency,"sents":sents}
    
    # Get a clean sentence array with only sentences linked to words
    for sentence in all_sentences :
        if len(sentence["words"])>0:
            sentences.append(sentence)
    
    print("Word Dictionary, number of words : " + str(number_of_words))
    print("------------------------------------------------")
    print()
    for key in dictionary:
        print(key)
        print("appears", dictionary[key]["freq"], "times")
        print("sentences: ")
        sents = []
        for index in range(0,len(sentences)):
            if key in sentences[index]["words"]:
                sents.append(index)
                print(sentences[index]["text"])
                print()
        dictionary[key]["sents"] = sents
        print()
    print()
    
    print("Sentence list, number of sentences : " + str(len(sentences)))
    print("------------------------------------------------")
    for sentence in sentences:
        print()
        print(sentence["text"])
        print(sentence["words"])
    



print("++++++++++++++ Start of tractacme mock server +++++++++++++++++")
print()
print("Please type an author or a concept")
search_result = []
language = "english" # "spanish"
for line in fileinput.input():
    search_result = wikiquotes.search(line, language)
    if len(search_result)>0 :
        print("Index : Option")
        for index in range(0,len(search_result)):
            print(str(index) + " : " + search_result[index])
        break
    else :
        print("No results found in Wikiquote database.")
        print("Please type again an author or a concept")
fileinput.close()
print()
print("Please select one of the results by index starting from 0 to " + str(len(search_result)-1))
for line in fileinput.input():
    try:
        index = int(line)
        print()
        print(str(index) + " ++++++++++++++ " + search_result[index] + " +++++++++++++++++++++++")
        print()
        quotes_result = wikiquotes.get_quotes(search_result[index], language)
        if len(quotes_result) > 0 :
            # process result and prepare for NLTK examples
            input_sentences = []
            for quote in quotes_result:
                input_sentences.append(quote.replace("«", "").replace("»", "").replace("[no sources]",""))
            process_text(input_sentences, number_of_words) 
            break
        else :
            print("No quotes are available for " + line)
            print("Please select again one of the results by index starting from 0 to " + str(len(search_result)-1))
    except :
        print("wrong index format")
        print("Please select again one of the results by index starting from 0 to " + str(len(search_result)-1))
fileinput.close()
print()
print(" ++++++++++++++++ End of tractacme mock server +++++++++++++++")