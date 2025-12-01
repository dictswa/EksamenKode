import os
from bs4 import BeautifulSoup
import pandas

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

relationships = []

for file in files:
    text = open('sinti-en-roma-namenlijst/'+file,'r',encoding='utf-8').read()
    soup = BeautifulSoup(text,features="lxml")
    names = soup.findAll('div',attrs={'class':'c-warvictim-family-tree'})
    for name in names:
        general_relations = name.findAll('h3',attrs={'class':'c-warvictim__subtitle'})
        for relation in general_relations:
            general_relation = relation.text
            print(general_relation)
            person_links = name.findAll('h4',attrs={'class':'c-card-family__title'})
            for person_link in person_links:
                person_link = person_link.text
                print(person_link)


df = pandas.DataFrame(data,columns = ["ID","Name","Birthplace","Birthdate","Deathplace","Deathdate"])

df.to_csv('Victims.csv', index=False, encoding='utf-8')
