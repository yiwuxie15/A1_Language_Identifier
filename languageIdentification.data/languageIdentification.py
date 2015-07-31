import re, os, sys, math

def trainBigramLanguageModel(inStr):
#input:	 string	 (training	 text	 in	 a	 given	 language);	 output:	
#dictionary with character frequencies	collected from	the string; output: dictionary	with characterbigram
#frequencies collected from the	string
    Biagdict = {}
    Singdict = {}
    for i in range(len(inStr)-1):
        bigram = inStr[i]+inStr[i+1]
        if bigram not in Biagdict.keys():
            Biagdict[bigram] = 1
        else:
            Biagdict[bigram] += 1
        
        if inStr[i] not in Singdict.keys():
            Singdict[inStr[i]] = 1
        else:
            Singdict[inStr[i]] += 1
            
    return [Biagdict, Singdict] 
    
    
def identifyLanguage(inStr, strList, singList, bigramList):
#input:	string (text for which the language is	to be identified); input: list	of	
#strings (each string corresponding to a language name); input:	list of dictionaries with single	
#character frequencies	 (each	 dictionary corresponding to the single	 character frequencies in a	
#language); list of dictionaries with bigram character	frequencies (each dictionary corresponding to	
#the bigram character frequencies in a language); output: string (the name of of the most likely	
#language).Note: in the	input lists,elements at	a given	position K in the lists	correspond to the same	
#language L.

    testLang = [0, 0, 0] #store possiblity of each language
    
    for j in range(len(strList)):#0--English, 1--French, 2--Italian    
        for i in range(len(inStr)-1):
            testBigram = inStr[i]+inStr[i+1]
            if testBigram in bigramList[j].keys():
                biagFreq = bigramList[j][testBigram]
            else:
                biagFreq = 0
                
            if testBigram[0] in singList[j].keys():
                charFreq = singList[j][testBigram[0]]
            else:
                charFreq = 0
                
            newFreq = math.log((biagFreq+1)*1.0/(charFreq+len(singList[j])),2)
            testLang[j] += newFreq
    
    if max(testLang) == testLang[0]:
        return strList[0]
    elif max(testLang) == testLang[1]:
        return strList[1]
    else:
        return strList[2]           
         
    
    
if len(sys.argv) == 2:
    testpath = str(sys.argv[1])
else:
    print "#Arguments Error"
    exit
    

    

filepath = "training/" 
dir_entry_path = os.listdir(filepath)

singleList = []
biagramList = []

for f in dir_entry_path:
    file_path = filepath+f
    with open (file_path, "r") as trainfile:  
        traintxt=trainfile.read().replace(' \n', ' ')
        #traintxt1 = re.sub("[\~\!\@\#\$\%\^\&\*\(\)\-\+\{\}\[\]\:\;\"\'\,\.\<\>\?\/]+", "", train1file.read())
        eng = trainBigramLanguageModel(traintxt)
        singleList.append(eng[1])
        biagramList.append(eng[0])

with open (testpath, "r") as testfile:
    line = 1
    #testtxt = re.sub("[\~\!\@\#\$\%\^\&\*\(\)\-\+\{\}\[\]\:\;\"\'\,\.\<\>\?\/]+", "", testfile.readline())
    testtxt = testfile.readline().replace(' \n', '')
    while testtxt:  
        language = identifyLanguage(testtxt, dir_entry_path, singleList, biagramList)
        print str(line) + ' ' + language
        line += 1
        testtxt = testfile.readline().replace(' \n', '')       
        #testtxt = re.sub("[\~\!\@\#\$\%\^\&\*\(\)\-\+\{\}\[\]\:\;\"\'\,\.\<\>\?\/]+", "", testfile.readline())

trainfile.close()
testfile.close()
    
    
    
