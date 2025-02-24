import re
import string
import shutil
import os
import time
import datetime
import math
import urllib
#import numpy
from array import array

from HTMLParser import HTMLParser

class MLStripper(HTMLParser):
    def __init__(self):
        self.reset()
        self.fed = []
    def handle_data(self, d):
        self.fed.append(d)
    def get_data(self):
        return ''.join(self.fed)

#High frequency words to exclude
highFreq = ["the", "or", "out", "its",
            "of", "by", "them", "who",
            "and", "one", "then", "now",
            "a","had","she","people",
            "to","not","many","my",
            "in","but","some","made",
            "is","what","so","over",
            "you","all","these","did",
            "that","were","would","down",
            "it","when","other","only",
            "he","we","into","way",
            "for","there","has","find",
            "was","can","more","use",
            "on","an","her","may",
            "are","your","two","water",
            "as","which","like","long",
            "with","their","him","little",
            "his","said","see","very",
            "they","if","time","after",
            "at","do","could","words",
            "be","will","no","called",
            "this","each","make","just",
            "from","about","than","where",
            "i","how","first","most",
            "have","up","been","know"]

highFreq = ["the", "or", "out", "its",
            "of", "by", "them", "who",
            "and", "one", "then", "now",
            "a","had","she",
            "to","not","many","my",
            "in","but","some","made",
            "is","what","so","over",
            "you","all","these","did",
            "that","were","would","down",
            "it","when","other","only",
            "he","we","into",
            "for","there","has",
            "was","can","more","use",
            "on","an","her",
            "are","your","two",
            "as","which",
            "with","their","him",
            "his",
            "they","if",
            "at","do",
            "be","will",
            "this","each","make",
            "from","about","than","where",
            "i","how",
            "have","up","been"]

#remove the files we'll be building if they already exist
os.remove("KIRK.txt")
os.remove("SPOCK.txt")
    
'''
Take an html file, remove tags
'''
def strip_tags(html):
    s = MLStripper()
    s.feed(html)
    return s.get_data()

'''
Take a url of a script like ... and a character (e.g. ), 
'''
def getLines(url,char):
    #Get ST script 
    filehandle = urllib.urlopen(url)
    #A file to copy the script into as is
    script = open('script.html','w')#gets overwritten
    #Files for character's lines
    char = char.upper()
    charFile = open(char+'.txt','a')
    hugeString = ""

    #Read in lines and write them to file and string as a giant string for regex to search over
    for line in filehandle.readlines():
        script.write(line.rstrip()+" ")
        hugeString+=line.rstrip()+" "
    script.close()

    charLines = re.findall(r'%s.*?<\s*(?:/p|br)\s*>'%char,hugeString)#still need </p> etc.

    for c in charLines:
        charFile.write(strip_tags(c)+"\n")

    charFile.close()

    filehandle.close()

#Build Kirk's file
getLines('http://www.chakoteya.net/startrek/24.htm',"kirk")#Space Seed
getLines('http://www.chakoteya.net/startrek/25.htm',"kirk")#This Side of Paradise
getLines('http://www.chakoteya.net/startrek/26.htm',"kirk")#The Devil in the Dark
getLines('http://www.chakoteya.net/startrek/27.htm',"kirk")#Errand of Mercy
getLines('http://www.chakoteya.net/startrek/28.htm',"kirk")#The City on the Edge of Forever
getLines('http://www.chakoteya.net/startrek/29.htm',"kirk")#Operation: Annihilate!
#Build Spock's file
getLines('http://www.chakoteya.net/startrek/24.htm',"spock")#Space Seed
getLines('http://www.chakoteya.net/startrek/25.htm',"spock")#This Side of Paradise
getLines('http://www.chakoteya.net/startrek/26.htm',"spock")#The Devil in the Dark
getLines('http://www.chakoteya.net/startrek/27.htm',"spock")#Errand of Mercy
getLines('http://www.chakoteya.net/startrek/28.htm',"spock")#The City on the Edge of Forever
getLines('http://www.chakoteya.net/startrek/29.htm',"spock")#Operation: Annihilate!

##ch = ""
##while ch == "":
##    ch = input("Pick a character: ")
##ep = ""
##while ep == "":
##    season = input("Pick a season, 1-3: ")
##    if season == "1":
##        ep = "1-29"
##    elif season == "2":
##        ep = "34-55"
##    elif season == "3":
##        ep = "61-79"
##ur = ""
##while ur == "":
##    episode = input("Pick an episode, "+ep+": ")
##    ur = "http://www.chakoteya.net/startrek/"+episode+".html"
##    getLines(ur,ch)
###txt to compare
##fi = ""
##fi = input("Enter file name for comparison: ")

#vs char=".txt"
#Make it "are you a kirk or a spock"?

#getLines('http://www.chakoteya.net/startrek/25.htm',"kirk")

#Should probably put above into functions
############
############
#Now to make dicationaries for the files
#Haven't touched punctuation, capitalization, "KIRK:" so far


def popDict(popFile):
    """
    Takes a txt file and builds a dictionary of all words in the file mapped to their counts
    Returns the dictionary of words in that file (minus the "CHAR:"). Removes generally high freq words
    and words that appear rarely in these scripts
    """
    char = (str(popFile).split("."))[0]
    aDict = {}
    newDict = {}
    newerDict = {}
    with  open(popFile,'r') as f:
        for line in f:
            #Remove "CHAR:"
            line = re.sub(r'%s.*:.'%char, "", line)
            print line
            #Take of eol chars and split at space
            words = line.rstrip().split(" ")
            #Remove . , ! ? : ; ) ( and make lowercase
            for i in range(0,len(words)):
                word = words[i]
                if len(word) > 1:
                    if word[-1]=="." or word[-1]=="," or word[-1]=="!" or word[-1]=="?" or word[-1]==":" or word[-1]==";" or word[-1]==")":
                        words[i] = word[:-1]
                    if word[0]=="(":
                        words[i] = word[1:]
                words[i] = string.lower(words[i])
            #Add to/update dictionary
            for word in words:
                if word not in highFreq:
                    if aDict.has_key(word):
                        aDict[word]+=1
                    else:
                        aDict[word]=1
                    
        #To make %
        totWds = float(sum(aDict.values()))
        print "before", totWds
        for key in aDict:
            newDict[key]=aDict[key]/totWds
        

        #go through and remove the ~0 ones
        deleteList = []
        for key in aDict:
            #print newDict[key]
            if newDict[key] < .001:
                #print newDict[key]
                deleteList.append(key)
        for key in deleteList:
            #print "Deleting", aDict[key] 
            del aDict[key]
        totWds = float(sum(aDict.values()))
        for key in aDict:
            newerDict[key] = aDict[key]/totWds
        #print deleteList
        print "after ", totWds
    return newerDict

#Build dictionaries of word frequencies for Kirk and Spock
dictKirk = popDict('KIRK.txt')
dictSpock = popDict('SPOCK.txt')
dictTest1 = popDict('test1.txt')
dictTest2 = popDict('test2.txt')


#print dictKirk.items()

##def categorize(test,option1,option2):
##    #positive 1 wins, negative 2 wins
##    testDict = popDict(test)
##    oneDict = popDict(option1)
##    twoDict = popDict(option2)
##    scoreDict = {}
##    score = 0
##
##    for key in testDict:
##        one = oneDict.get(key)
##        two = twoDict.get(key)
##        if one != None and two != None:
##            scoreDict[key]=one-two
##            score += one-two
##        elif one != None:
##            scoreDict[key]= one - 0
##            score += one
##        elif two != None:
##            scoreDict[key]= 0 - two
##            score -= two
##    print "Score ",score
##    if score>0:
##        print option1, " wins"
##    elif score<0:
##        print option2, " wins"
##    return scoreDict


##def vectorCat(test,option1,option2):
##    #positive 1 wins, negative 2 wins
##    testDict = popDict(test)
##    oneDict = popDict(option1)
##    twoDict = popDict(option2)
##
##    #All the words in all the docs (ignore values)
##    allDict = dict(testDict.items()+oneDict.items()+twoDict.items())
##    testDictAll={}
##    oneDictAll={}
##    twoDictAll={}
##
##    for key in allDict:
##        testDictAll[key]=testDict.get(key,0)
##        oneDictAll[key]=oneDict.get(key,0)
##        twoDictAll[key]=twoDict.get(key,0)
##
##    testVector = testDictAll.values()
##    oneVector = oneDictAll.values()
##    twoVector = twoDictAll.values()
##
##    cos1 = numpy.dot(oneVector,testVector)/(numpy.linalg.norm(oneVector)*numpy.linalg.norm(testVector))
##    cos2 = numpy.dot(twoVector,testVector)/(numpy.linalg.norm(twoVector)*numpy.linalg.norm(testVector))
##    
##    if cos1 > cos2:
##        print option1, " wins"
##    elif cos1 < cos2:
##        print option2, " wins"
##    print "Cosines ",cos1,cos2
##    wait = raw_input("PRESS ENTER TO CONTINUE.")
##    print option1,": ",oneDictAll
##    wait = raw_input("PRESS ENTER TO CONTINUE.")
##    print option2,": ",twoDictAll
##    return [cos1,cos2]

#print vectorCat("test1.txt","test1.txt","test2.txt")
#print vectorCat("KIRK.txt","KIRK.txt","SPOCK.txt")
#print vectorCat(".txt",".txt",".txt")




#Print out a js file with variables option1, option2, and can use reserved
f = open('supplements.js', 'w')
f.write("var dictKirk = "+str(dictKirk)+";\n")
f.write("\n")
f.write("var dictSpock = "+str(dictSpock)+";\n")
f.write("\n")
f.write("var highFreq = "+str(highFreq)+";")

f.write("\n")
f.write("var dictTest1 = "+str(dictTest1)+";")
f.write("\n")
f.write("var dictTest2 = "+str(dictTest2)+";")
f.close()
           
