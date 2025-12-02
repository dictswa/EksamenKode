import os
from bs4 import BeautifulSoup
import pandas

'''
Here we create a csv file containg all the victims:
Their Id, Name, Birthplace, Birthday, Deathplace and Deathday
'''

data = []

files = sorted(os.listdir('sinti-en-roma-namenlijst'))
for file in files:
    text = open('sinti-en-roma-namenlijst/'+file,'r',encoding='utf-8').read()
    soup = BeautifulSoup(text,features="lxml")
    # pID, name, date of birth and death, place of birth and death og alder
    names = soup.findAll('header',attrs={'class':'c-warvictim-intro'})
    for name in names:
        person_info = name.find('p',attrs={'class':'c-warvictim-intro__sub'}).text
        person_info = person_info.strip()
        person_info = " ".join(person_info.split())
        #looks at html files and takes their person ID
        pID = file.split("-")[0]
        #looks at our html files and takes their names
        pName = file.replace(pID+'-',"")
        pName = pName.replace(".html","")
        #looks at our list of person_info and splits
        splitted = person_info.split(", ")
        Birthplace = splitted[0]
        Deathdate = splitted[2]
        Birthdate = splitted[1].split(" – ",1)[0]
        Deathplace = splitted[1].split(" – ",1)[1]
       # age = name.find #færdiggør den her :)
        data.append([pID,pName,Birthplace,Birthdate,Deathplace,Deathdate])

df = pandas.DataFrame(data,columns = ["ID","Name","Birthplace","Birthdate",
                                      "Deathplace","Deathdate"])
df.to_csv('Victims.csv', index=False, encoding='utf-8')

'''
Here we create a csv file containing all relationships between the victims
Their ID, the ID of their relative, general relationsship type and detailed relationship type
'''

relationships = []

for file in files:
    text = open('sinti-en-roma-namenlijst/'+file,'r',encoding='utf-8').read()
    soup = BeautifulSoup(text,features="lxml")
    family_tree = soup.findAll('div',attrs={'class':'c-warvictim-family-tree'})
    for family in family_tree:
        relations = family.findAll('div',attrs={'class':"c-warvictim-family-tree__block"})
        for relation in relations:
            general = relation.find('h3',attrs={'class':'c-warvictim__subtitle'})
            if general == None:
                general_type = 'spouse'
            else:
                general_type = general.text
            people = relation.findAll('h4',attrs={'class':'c-card-family__title'})
            specific = relation.findAll('div',attrs={'class':'c-card-family__relation'})
            for i in range(len(people)):
                pID = file.split("-")[0]
                link = people[i].find('a')
                rID = link['href'].split("/")[-2]
                specific_type = specific[i].text.strip()
                if specific_type == '' or specific_type == 'Survivor':
                    specific_type = 'Unknown'
                if pID != rID:
                    relationships.append([pID,rID,general_type,specific_type])
    family_other = soup.find('div',attrs={'class':'c-warvictim-family-other'})
    if family_other != None:
        general_type = 'other'
        people = family_other.findAll('h4',attrs={'class':'c-card-family__title'})
        for person in people:
            pID = file.split("-")[0]
            link = person.find('a')
            rID = link['href'].split("/")[-2]
            relationships.append([pID,rID,general_type,'Unknown'])
                    
df = pandas.DataFrame(relationships,columns = ["ID1","ID2","General relationship type",
                                               "Detailed relationship type"])
df.to_csv('Relationships.csv', index=False, encoding='utf-8')
