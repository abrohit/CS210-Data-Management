import re, math

if __name__ == "__main__":

    file = open('tfidf_docs.txt', 'r')

    files = []

    for line in file:
        files.append(line.lstrip().rstrip())
    
    file.close()

    fileData = {}
    
    for file in files:

        f = open(file, 'r')

        fileStr = ''

        for line in f:

            line = line.strip().lower()
            line = re.sub(r'(http|https)://\S+', '', line)#Removes all websites.
            words = line.split()
            
            for i in range(len(words)):
                words[i] = re.sub(r'\W', '', words[i])#Removes all non-word characters.
            
            line = ' '.join(words)#Removes white spaces.

            fileStr += line.lower() + ' '
        
        fileStr = fileStr.strip()

        fileData[file] = fileStr
    
    stopwords = []
    stopwordFile = open('stopwords.txt', 'r')

    for line in stopwordFile:
        stopwords.append(line.lstrip().rstrip())
    
    
    for key, value in fileData.items():

        strData = value.split()

        index = 0
        while index < len(strData):
            
            word = strData[index]

            if word in stopwords:
                strData[index] = ''
            elif word[-3:] == 'ing':
                strData[index] = word[:-3]
            elif word[-2:] == 'ly':
                strData[index] = word[:-2]
            elif word[-4:] == 'ment':
                strData[index] = word[:-4]

            index += 1
        strData = [item for item in strData if item != '']
        fileData[key] = ' '.join(strData)
    
    for key, value in fileData.items():

        file = open('preproc_' + key , 'w')
        file.write(value)
        file.close()
    

    wordFreq = {}
    wordNum = {}
    for key, value in fileData.items():
        
        wordNum[key] = 0
        wordFreq[key] = {}
        strData = value.split()
        for word in strData:

            wordNum[key] += 1

            if word in wordFreq[key]:
                wordFreq[key][word] += 1
            else:
                 wordFreq[key][word] = 1
    
    tf = {}

    for key, value in wordFreq.items():

        tf[key] = {}
        for key2, val2 in value.items():
            tf[key][key2] = val2 / wordNum[key]
    
    idf = {}
    fileLen = len(files)

    for item in wordFreq.items():
        for key,value in item[1].items():
            for file in files:
                if key in wordFreq[file]:
                    if file in idf:
                        if key in idf[file]:
                            idf[file][key] += 1
                        else:
                            idf[file][key] = 1
                    else:
                        idf[file] = {key: 1}

    for item in idf.items():
        for key, value in item[1].items():
            idf[item[0]][key] = math.log((fileLen / value)) + 1
    
    tfIdf = {}
    
    for key, value in tf.items():
        for key2, value2 in value.items():
            if key in tfIdf:
                tfIdf[key][key2] = round(value2 * idf[key][key2], 2)
            else:
                tfIdf[key] = {key2: round(value2 * idf[key][key2], 2)}
    
    tfIdfSorted = {}
    for key, value in tfIdf.items():
        for key2, value2 in value.items():
            if key in tfIdfSorted:
                if value2 in tfIdfSorted[key]:
                    tfIdfSorted[key][value2].append(key2)
                else:
                    tfIdfSorted[key][value2] = [key2]
            else:
                tfIdfSorted[key] = {value2: [key2]}
    
    for key, value in tfIdfSorted.items():
        value = {k: v for k, v in sorted(value.items(), key = lambda _: _[0], reverse = True)}
        
        top5 = []
        for key2, value2 in value.items():

            tfIdfSorted[key][key2] = sorted(value2)
            
            for item in tfIdfSorted[key][key2]:
                if len(top5)>4:
                    break
                top5.append(f"('{item}', {key2})")
        
        f = open('tfidf_' + key, 'w')
        data = '['
        data += ', '.join(top5)
        data += ']'
        f.write(data)
        f.close()