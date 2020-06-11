
# coding: utf-8

# In[137]:

import glob
import re
import string
from nltk.stem import WordNetLemmatizer
from nltk.tokenize import RegexpTokenizer
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
lemmatizer=WordNetLemmatizer()
path="E:/E/IIIT Delhi/IR/Assign 1/20_newsgroups/temp/alt.atheism"
j=1
k=1
globalDocList=[]
direDict={}
dictWords={}
direct = [f for f in glob.glob("E:/E/IIIT Delhi/IR/Assign 1/20_newsgroups/Q2/*", recursive=True)]
for d in direct:
    files = [f for f in glob.glob(d+"/*", recursive=True)]
    filesRead={}
    i=1
    
    tokenizer = RegexpTokenizer(r'\w+')
    for f in files:
        list1=[]
        list2=[]
        fileRead = open(f, "r")
        input_str=tokenizer.tokenize(fileRead.read().lower())
        #input_str = input_str.lower()
        #input_str=list(set(input_str))
        pattern='[0-9][a-z]|[0-9]'
        input_str = [re.sub(pattern, '', j) for j in input_str]
        #input_str = str(input_str).translate(string.maketrans('',''), string.punctuation)
        #input_str = str(input_str).strip()

        #stop_words = set(stopwords.words('english'))
        #from nltk.tokenize import word_tokenize
        #tokens = word_tokenize(str(input_str))
        #result = [i for i in input_str if not i in stop_words]
        list1=[word.strip(string.punctuation) for word in input_str]
        for word in list1:
            list2.append(lemmatizer.lemmatize(word))

        
        #list2.remove("")
        filesRead[i]=list2
        tempDict={}
        index=0
        for words in filesRead[i]:
            if words in tempDict.keys():
                tempDict[words].append(index)
            else:
                tempDict[words]=[]
                tempDict[words].append(index)
            index=index+1   
                
        for words in filesRead[i]:
            temp={}
            #temp[str(j)+'-'+str(i)]=tempDict[words]
            temp[k]=tempDict[words]
            if words in dictWords.keys():
                #if (str(j)+'-'+str(i)) not in dictWords[words]:
                if k not in dictWords[words].keys():
                    dictWords[words][k]=[]
                    for x in temp[k]:
                        if x not in dictWords[words][k]:
                            dictWords[words][k].append(x)
                    #dictWords[words].append(temp)
                else:
                     for x in temp[k]:
                        if x not in dictWords[words][k]:
                            dictWords[words][k].append(x)
            else:
                dictWords[words]={}
                dictWords[words][k]=[]
                for x in temp[k]:
                    if x not in dictWords[words][k]:
                        dictWords[words][k].append(x)
        #globalDocList.append(str(j)+"-"+str(i))
        globalDocList.append(k)
        i=i+1
        k=k+1
   # print(filesRead)
    
    direDict[j]=filesRead
    j=j+1
    print(j)
print(len(direDict))
print(len(dictWords))
print(len(globalDocList))


# In[138]:

print(len(dictWords["great"]))


# In[142]:

query="please $ email me"
listQuery=query.split()
print(listQuery)
listQuery = [re.sub(pattern, '', j) for j in listQuery]
#listQuery.remove(' ')

listQuery=[word.strip(string.punctuation) for word in listQuery]
tempi=0
for words in listQuery:
    if len(words)==0:
        listQuery.pop(tempi)
    tempi=tempi+1

print(listQuery)
numberOfComp=0

tempDir={}
for words in listQuery:
    tempDir[words]=dictWords[words]
index=0   
#print(len(tempDir))
while index != len(listQuery)-1: 
    keyList=[]
    tempList1=tempDir[listQuery[index]]
    tempList2=tempDir[listQuery[index+1]]
   # print("length of templist are ",len(tempList1)," ",len(tempList2))
    for keys in tempList1:
        if keys in tempList2:
            keyList.append(keys)
    keyList2=[]
   # print("length of keylist ",len(keyList))
    for keys in keyList:
        for x in tempList1[keys]:
            for y in tempList2[keys]:
                if(y-x)==1:
                    keyList2.append(keys)
                
    index=index+1           
    
    tempdic2={}
    for keys in tempDir[listQuery[index]]:
        if keys in keyList2:
            tempdic2[keys]=tempDir[listQuery[index]][keys]
    tempDir[listQuery[index]]=tempdic2
    
print("Number of Documents = ",len(tempDir[listQuery[index]]))
print("Documents retrived are",tempDir[listQuery[index]].keys())


# In[ ]:



