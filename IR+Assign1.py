
# coding: utf-8

# In[130]:

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
direct = [f for f in glob.glob("E:/E/IIIT Delhi/IR/Assign 1/20_newsgroups/20_newsgroups/*", recursive=True)]
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
        input_str=list(set(input_str))
        pattern='[0-9][a-z]|[0-9]'
        input_str = [re.sub(pattern, '', j) for j in input_str]
        #input_str = str(input_str).translate(string.maketrans('',''), string.punctuation)
        #input_str = str(input_str).strip()

        stop_words = set(stopwords.words('english'))
        #from nltk.tokenize import word_tokenize
        #tokens = word_tokenize(str(input_str))
        result = [i for i in input_str if not i in stop_words]
        list1=[word.strip(string.punctuation) for word in result]
        for word in list1:
            list2.append(lemmatizer.lemmatize(word))

        
        #list2.remove("")
        filesRead[i]=list(set(list2))
        for words in filesRead[i]:
            if words in dictWords.keys():
                #dictWords[words].append(str(j)+"-"+str(i))
                dictWords[words].append(k)
            else:
                dictWords[words]=[]
                #dictWords[words].append(str(j)+"-"+str(i))
                dictWords[words].append(k)
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


# In[131]:

print(len(dictWords["ball"]))
i=0
for x in dictWords:
    print(x)
    if(i==4):
        break
    i=i+1
    
print(len(globalDocList))


# In[ ]:

query=input("Enter Query: ")


# In[150]:

query="ball and and || hit and not not & trustworthy"
query=query.lower()
print(query)
listQuery=query.split(" ")
listQuery = [re.sub(pattern, '', j) for j in listQuery]
#listQuery.remove(' ')

listQuery=[word.strip(string.punctuation) for word in listQuery]
tempi=0
for words in listQuery:
    if len(words)==0:
        listQuery.pop(tempi)
    tempi=tempi+1
#print(listQuery)

tempi=0
for words in listQuery:
    if words != "and" and words!= "or" and words!="not":
        listQuery[tempi]=lemmatizer.lemmatize(words)
    tempi=tempi+1
print("preprocessed Query = ",listQuery)
tempi=0
#==============
lq=[]
lq=listQuery
listQuery=[]
for i in range(len(lq)-1):
    if lq[i] != lq[i+1]:
        listQuery.append(lq[i])
listQuery.append(lq[len(lq)-1])
#==============
#===============
lqtemp=[] #For storing Duplicate words
for words in listQuery:
    if listQuery.count(words)>1 and words!="and" and words!="or" and words!="not":
        if words not in lqtemp:
            lqtemp.append(words)
            
for words in lqtemp:
    index=0
    tindex=0
    for w in listQuery:
        if words == w:
            index=index+1
        if words == w and index!=1:
            listQuery[tindex]=str(index)+listQuery[tindex]
            
        tindex=tindex+1
        
numList=['1','2','3','4','5','6','7','8','9']



#===============
tempList=[]
tempj=0
tempListQuery=[]
numberOfComp=0
for x in listQuery:
    if x=="not":
        tempListQuery.append(listQuery[tempj+1])
        listQuery.remove("not")
    tempj=tempj+1
print("TempListQuery=",tempListQuery," and ListQuery =",listQuery)
for x in listQuery:
    if x!="and" and x!="or":
        tempList.append(x)

tempDir={}
for words in tempList:
    if words[0] in numList:
        tempDir[words]=dictWords[words[1:]]
    else:
        tempDir[words]=dictWords[words]
    #print("Length of each Dict =",words,"= ",len(tempDir[words]))

for words in tempListQuery:
    temp1Dir=[]
    temp1Dir=tempDir[words]
    tempDir[words]=[]
    #print("Len of global lsit=",len(globalDocList))
    for x in globalDocList:
        numberOfComp=numberOfComp+1
        if x in temp1Dir:
            donin=""
        else:
            tempDir[words].append(x)
    #tempDir[words]=list(set(globalDocList)-set(tempDir[words]))
    #tempDir[words]=tempDir[words].sort()
    print("Len of not ",words,"=",len(tempDir[words]))
    
counter=0
while len(listQuery) > 1:
    minLen=999999999999
    tempString=""
    for words in tempList:
        if "and" in listQuery: 
            if len(tempDir[words])<minLen:
                if listQuery.index(words)!=(len(listQuery)-1):
                    if listQuery[listQuery.index(words)+1]=="and":
                        tempString=words
                        minLen=len(tempDir[words])
                else:
                    if listQuery[listQuery.index(words)-1]=="and":
                        tempString=words
                        minLen=len(tempDir[words])
        else:
            if len(tempDir[words])<minLen:
                tempString=words
                minLen=len(tempDir[words])

    #minLen=999999
#     for x in range(len(listQuery)):
#         if listQuery[x+1]=="and":
#             if min(len(tempDir[listQuery[x]]),len(tempDir[listQuery[x+2]])) < minLen:
#                 tempString=listQuery[x]
#                 minLen=len(tempDir[listQuery[x]])
#         if listQuery[x+1]=="or":
#             if min(len(tempDir[listQuery[x]])+len(tempDir[listQuery[x+2]])) < minLen:
#                 tempString=listQuery[x]
#                 minLen=len(tempDir[listQuery[x]])
#         x=x+2       
    print("minLenString=",tempString)
    index=listQuery.index(tempString)
    #print("index word= ",index)
    flag=0
    if index == len(listQuery)-1:
        tempList1=tempDir[listQuery[index-2]]
        tempList2=tempDir[listQuery[index]]
        flag=1
    else:
        tempList1=tempDir[listQuery[index]]
        tempList2=tempDir[listQuery[index+2]]

    finalAns=[]
    temp1=0
    temp2=0
    pointer=min(len(tempList1),len(tempList2))
    if (flag==1 and listQuery[index-1]=="and") or (flag==0 and listQuery[index+1]=="and"):
        while temp1<len(tempList1) and temp2<len(tempList2):
            if tempList1[temp1]==tempList2[temp2]:
                #print("In =")
                finalAns.append(tempList1[temp1])
                temp1=temp1+1
                temp2=temp2+1
            elif tempList1[temp1]>tempList2[temp2]:
                #print("In >")
                temp2=temp2+1
            else:
                temp1=temp1+1
            numberOfComp=numberOfComp+1    
    elif (flag==1 and listQuery[index-1]=="or") or (flag==0 and listQuery[index+1]=="or"):
        while temp1<len(tempList1) and temp2<len(tempList2):
            if tempList1[temp1]==tempList2[temp2]:
                #print("In =")
                finalAns.append(tempList1[temp1])
                temp1=temp1+1
                temp2=temp2+1
            elif tempList1[temp1]>tempList2[temp2]:
                #print("In >")
                finalAns.append(tempList2[temp2])
                temp2=temp2+1
            else:
                finalAns.append(tempList1[temp1])
                temp1=temp1+1
            numberOfComp=numberOfComp+1
        if temp1==len(tempList1):
            for x in range(temp2,len(tempList2)):
                finalAns.append(tempList2[x])
                
        elif temp2==len(tempList2):
            for x in range(temp1,len(tempList1)):
                finalAns.append(tempList1[x])
     
    
    
    if flag==1:
        #print("length of Original dir = ",len(tempDir[listQuery[index-2]]))
        tempDir[listQuery[index-2]]=finalAns
        #print("length of Updated dir = ",len(tempDir[listQuery[index-2]]))
        #print("length of Updated dir set = ",len(set(tempDir[listQuery[index-2]])))
        del tempDir[listQuery[index]]
        tempList.remove(listQuery[index])
        listQuery.pop(index)
        listQuery.pop(index-1)
        #listQuery.remove(listQuery[index-1])
    else:
        #print("length of Original dir = ",len(tempDir[listQuery[index]]))
        tempDir[listQuery[index]]=finalAns
        #print("length of updated dir = ",len(tempDir[listQuery[index]]))
        #print("length of Updated dir set = ",len(set(tempDir[listQuery[index]])))
        del tempDir[listQuery[index+2]]
        tempList.remove(listQuery[index+2])
        listQuery.pop(index+2)
        listQuery.pop(index+1)
        #tempList.remove(listQuery[index+1])
    counter=counter+1
    print("List Query = ",listQuery)
    #print("Length of final ans = ",len(finalAns))

print("Total number of comparisons = ",numberOfComp)
print("Total number of documents = ",len(tempDir[listQuery[0]]))
print("List of documents retrived are ",tempDir[listQuery[0]])




# In[ ]:



