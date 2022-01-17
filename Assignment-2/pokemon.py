import csv, math

#Problem 1

if __name__ == "__main__":

    pokemonFile = open('pokemonTrain.csv', 'r')

    reader = csv.reader(pokemonFile)

    next(reader)#Skips the header.
    
    reader = list(reader)#Converts Reader into a 2d list.
    
    totalPokemon = len(reader)
    totalFireAboveForty = 0
    totalfire = 0

    HtotalAttack = [0,0]
    HtotalDef = [0,0]
    HtotalHP = [0,0]
    LtotalAttack = [0,0] 
    LtotalDef = [0,0]
    LtotalHP = [0,0]
    
    for item in reader:
        
        if item[4] == 'fire' and float(item[2]) >= 40:

            totalFireAboveForty += 1
        
        if item[4] == 'fire':

            totalfire += 1
        
        if item[4] == 'NaN':
            
            weakness = item[5]
            typeCounter = {}
            
            for check in reader:

                if check[4] != 'NaN' and check[5] == weakness:
                    
                    if check[4] in typeCounter:
                        
                        typeCounter[check[4]] += 1
                    else:
                        
                        typeCounter[check[4]] = 1
            
            typeCounter = {key: value for key, value in sorted(typeCounter.items(), key = lambda _: _[1], reverse = True)}
            
            firstKey = list(typeCounter.values())[0]

            unsorted = [key for key, value in typeCounter.items() if value == firstKey]
            unsorted.sort()

            Type = unsorted[0]
            
            item[4] = Type
        
        if float(item[2]) > 40:
            
            if item[6] != 'NaN':
                
                HtotalAttack[0] += float(item[6])
                HtotalAttack[1] += 1
            
            if item[7] != 'NaN':

                HtotalDef[0] += float(item[7])
                HtotalDef[1] += 1
            
            if item[8] != 'NaN':
                
                HtotalHP[0] += float(item[8])
                HtotalHP[1] += 1

        else:
            
            if item[6] != 'NaN':
                
                LtotalAttack[0] += float(item[6])
                LtotalAttack[1] += 1
            
            if item[7] != 'NaN':

                LtotalDef[0] += float(item[7])
                LtotalDef[1] += 1
            
            if item[8] != 'NaN':
                
                LtotalHP[0] += float(item[8])
                LtotalHP[1] += 1

    
    percentage = round((totalFireAboveForty / totalfire) * 100)
    
    output = f'Percentage of fire type Pokemons at or above level 40 = {percentage}'

    f = open("pokemon1.txt", "w")
    f.write(output)
    f.close()
    
    try:
        HavgAttack = round(HtotalAttack[0] / HtotalAttack[1], 1)
    except:
        HavgAttack = 0.0
    
    try:
        LavgAttack = round(LtotalAttack[0] / LtotalAttack[1], 1)
    except:
        LavgAttack = 0.0

    try:
        HavgDef = round(HtotalDef[0] / HtotalDef[1], 1)
    except:
        HavgDef = 0.0

    try:
        LavgDef = round(LtotalDef[0] / LtotalDef[1], 1)
    except:
        LavgDef = 0.0

    try:
        HavgHP = round(HtotalHP[0] / HtotalHP[1], 1)
    except:
        HavgHP = 0.0
    
    try:
        LavgHP = round(LtotalHP[0] / LtotalHP[1], 1)
    except:
        LavgHP = 0.0

    for item in reader:

        if float(item[2]) > 40:
            
            if item[6] == 'NaN':

                item[6] = HavgAttack
            
            if item[7] == 'NaN':

                item[7] = HavgDef
            
            if item[8] == 'NaN':

                item[8] = HavgHP

        else:
            
            if item[6] == 'NaN':

                item[6] = LavgAttack
            
            if item[7] == 'NaN':

                item[7] = LavgDef
            
            if item[8] == 'NaN':

                item[8] = LavgHP

    pokemonFile.close()
    
    columns = ['id', 'name', 'level', 'personality', 'type', 'weakness', 'atk', 'def', 'hp', 'stage']
    Cwriter = open('pokemonResult.csv', 'w', newline='')
    csvWriter = csv.writer(Cwriter, delimiter = ',')
    csvWriter.writerow(columns)
    csvWriter.writerows(reader)

    #---------------------------------------------------------------------------------------------------

    personalityMapping = {}
    total_HP = [0,0]
    
    for item in reader:

        if item[4] in personalityMapping:

            if item[3] not in personalityMapping[item[4]]:
                personalityMapping[item[4]].append(item[3])
                personalityMapping[item[4]].sort()

        else:

            personalityMapping[item[4]] = [item[3]]
            personalityMapping[item[4]].sort()


        if float(item[9]) == 3.0:
            
            total_HP[0] += float(item[8])
            total_HP[1] += 1

    personalityMapping = {key: value for key, value in sorted(personalityMapping.items(), key= lambda item: item[0])}
    
    data = """Pokemon type to personality mapping:\n"""
    for key, value in personalityMapping.items():

        line = "\n\t" + f"{key}: "

        for item in value:

            line += f"{item}, "
        
        data += line[0:-2]

    f = open("pokemon4.txt", "w")
    f.write(data)
    f.close()

    try:
        avgHP = round(total_HP[0] / total_HP[1])
    except:
        avgHP = 0

    f = open("pokemon5.txt", "w")
    f.write(str(avgHP))
    f.close()