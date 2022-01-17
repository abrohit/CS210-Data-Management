import csv

if __name__ == "__main__":

    covidFile = open('covidTrain.csv', 'r')

    reader = csv.reader(covidFile)

    next(reader)#Skips the header.
    
    reader = list(reader)#Converts Reader into a 2d list.

    lats = {}
    lons = {}

    cityCounter = {}
    symptomCounter = {}

    for item in reader:

        if '-' in item[1]:
            
            age1, age2 = item[1].split('-')
            avg = round((int(age1) + int(age2))/2)

            item[1] = avg
        
        dd, mm, yyyy = item[8].split('.')
        item[8] = f"{mm}.{dd}.{yyyy}"

        dd, mm, yyyy = item[9].split('.')
        item[9] = f"{mm}.{dd}.{yyyy}"

        dd, mm, yyyy = item[10].split('.')
        item[10] = f"{mm}.{dd}.{yyyy}"

        if item[6].lower() != 'nan':

            if item[4] in lats:

                lats[item[4]][0] += float(item[6])
                lats[item[4]][1] += 1
            else:
                lats[item[4]] = [float(item[6]), 1]
        
        if item[7].lower() != 'nan':

            if item[4] in lons:

                lons[item[4]][0] += float(item[7])
                lons[item[4]][1] += 1
            else:
                lons[item[4]] = [float(item[7]), 1]
        
        if item[3].lower() != 'nan':
            if item[4] in cityCounter:
                
                if item[3] in cityCounter[item[4]]:

                    cityCounter[item[4]][item[3]] += 1
                else:
                    cityCounter[item[4]][item[3]] = 1
            else:
                cityCounter[item[4]] = {item[3]: 1}
        
        if item[11].lower() != 'nan':
            
            symptoms = item[11].rstrip().lstrip().split(';')
            
            for i in range(len(symptoms)):
                symptoms[i] = symptoms[i].rstrip().lstrip().strip(' ').strip()
            
            if item[4] in symptomCounter:

                for _ in symptoms:
                    if _ in symptomCounter[item[4]]:
                        symptomCounter[item[4]][_] += 1
                    else:
                        symptomCounter[item[4]][_] = 1
            else:
                symptomCounter[item[4]] = {_ : symptoms.count(_) for _ in symptoms}
    
    for key, value in symptomCounter.items():
        
        symptomCounter[key] = {k: v for k, v in sorted(value.items(), key = lambda _: _[1], reverse = True)}
        
        firstKey = list(symptomCounter[key].values())[0]
        
        symptomCounter[key] = [k for k, v in value.items() if v == firstKey]
        symptomCounter[key] = sorted(symptomCounter[key])

    for key, value in cityCounter.items():
        
        cityCounter[key] = {k: v for k, v in sorted(value.items(), key = lambda _: _[1], reverse = True)}
        
        firstKey = list(cityCounter[key].values())[0]
        
        cityCounter[key] = [k for k, v in value.items() if v == firstKey]
        cityCounter[key] = sorted(cityCounter[key])
        
    for item in reader:

        if item[6].lower() == 'nan':

            if item[4] in lats:
                item[6] = str(round((lats[item[4]][0] / lats[item[4]][1]), 2))
            else:
                item[6] = 0.00

        if item[7].lower() == 'nan':

            if item[4] in lons:
                item[7] = str(round((lons[item[4]][0] / lons[item[4]][1]), 2))
            else:
                item[7] = 0.00
        
        if item[3].lower() == 'nan':

            item[3] = cityCounter[item[4]][0]
        
        if item[11].lower() == 'nan':

            item[11] = symptomCounter[item[4]][0]

    columns = ['ID', 'age', 'sex', 'city', 'province', 'country', 'latitude', 'longitude', 'date_onset_symptoms', 'date_admission_hospital', 'date_confirmation', 'symptoms']
    Cwriter = open('covidResult.csv', 'w', newline='')
    csvWriter = csv.writer(Cwriter, delimiter = ',')
    csvWriter.writerow(columns)
    csvWriter.writerows(reader)

    covidFile.close()