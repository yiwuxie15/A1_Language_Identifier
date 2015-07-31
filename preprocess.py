import re, os, sys
from PorterStemmer import PorterStemmer

def removeSGML(inStr):
#Function	that	removes	the	SGML	tags.
#Name:	removeSGML;	input: string;	output:	string   
    return re.sub('<.*?>', '', inStr)   
    
def tokenizeText(inStr):
##Function	that	tokenizes	the	text.	
##Name:	tokenizeText;	input:	string;	output:	list	(of	tokens)    
    words = inStr.replace('\n', ' ').split(" ")
    newwords = []
    for word in words:
        if word.endswith(',') or word.endswith('!') or word.endswith('?') or word.endswith(':') or word.endswith(';') or word.endswith(')'):
            word = word[:-1]
    
        puc = re.match("(\W+)", word)
        if puc or word == '':
            continue
        
        m = re.match("(I)('m)", word)
        d = re.match("(\w*)(n't)", word)
        l = re.match("(\w*)('s)", word) 
        r = re.match("(\w*)('re)", word)
        dig = re.match("(\d+)(\.)", word)
        num = re.search("(\,)(\d+)", word)    
        
        if m:
            newwords.append('I')
            newwords.append('am')
        elif d:
            if d.group(1)=='won':
                newwords.append('will')
            else:
                newwords.append(d.group(1))
            newwords.append('not')
        elif l:
            if l.group(1) == 'let':
                newwords.append('let')
                newwords.append('us')
            elif l.group(1) == 'it':
                newwords.append('it')
                newwords.append('is')
            else:
                newwords.append(l.group(1))
                newwords.append(l.group(2))
        elif r:
            newwords.append(r.group(1))
            newwords.append(r.group(2))
        elif dig:
            newwords.append(dig.group(1))
        elif num:
            if len(num.group(2)) != 3:
                for num in word.split(','):
                    newwords.append(num)
        else:
            newwords.append(word)
    
    return newwords
            
def removeStopwords(inList):    
#Function that removes the stopwords.	
#Name:	removeStopwords;input:list(of tokens);	output:	list(of tokens)
    newlist = []
    with open ("stopwords.txt", "r") as stopfile:
        stopdata=stopfile.read().replace('\n', ' ')
        stopwordlist = stopdata.split(' ')
        #print stopwords    
    
    for word in inList:
        if word.lower() in stopwordlist:
            continue
        else:
            newlist.append(word)
    
    stopfile.close()
    return newlist
    
def stemWords(inList):
##Function that stems the	words.
##Name: stemWords; input:	list (of tokens); output: list	(of stemmed tokens)
    outlist = []
    p = PorterStemmer()
    for word in inList:
        outlist.append(p.stem(word, 0, len(word)-1))
    return outlist


if len(sys.argv) == 2:
    filepath = str(sys.argv[1])
else:
    print "#Arguments Error"
    exit

path = os.getcwd()+'/' + filepath
wCount = 0
Count = {}
for filename in os.listdir(path):
    txt = open(filepath+filename)
    #txt = open("test")
    rSGML = removeSGML(txt)
    newwords = tokenizeText(rSGML)
    newer = removeStopwords(newwords)
    wCount += len(newer)
    newest = stemWords(newer)
    for word in newest:
        if word not in Count.keys():
            Count[word] = 1;
        else:
            Count[word] += 1;
    
    txt.close()
    
vCount = len(Count)
uniqueCount = sorted(Count.items(), key=lambda x:x[1], reverse=True)
print "Words " + str(wCount)
print "Vocabulary " + str(vCount)
print "Top 50 words"
for i in range(50):
    print uniqueCount[i][0] + ' ' + str(uniqueCount[i][1]) + '\n'

