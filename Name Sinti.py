# -*- coding: utf-8 -*-
"""
Created on Mon Nov 24 12:32:52 2025

@author: jonas
"""

import urllib
import os
from bs4 import BeautifulSoup
import pandas

vname = []

files = sorted(os.listdir('sinti-en-roma-namenlijst'))
for file in files:
    text = open('sinti-en-roma-namenlijst/'+file,'r',encoding='utf-8').read()
    soup = BeautifulSoup(text,features="lxml")
    # pID, name, date of birth and death, place of birth and death
    #matchday = file[:-6]
    names = soup.findAll('header',attrs={'class':'c-warvictim-intro'})
    for name in names:
        wname = name.find("h1", attrs={"class":"c-warvictim-intro__title"}).text
        wname = wname.strip()
        wname = " ".join(wname.split())
        #wname = wname.split()
        vname.append(wname)
        print(vname)
                  
    ######tester 
    
    
    # for name in names:
    #     #date
    #     birthdate = name.find('p',attrs={'class':'c-warvictim-intro__sub'}).text
    #     birthdate = birthdate.strip().split() #få den  til at stoppe ved - og splitte fødselssted ved første , komma
    #     print(birthdate)
    #     for j in birthdate:
    #         j = j.replace("\n","")
    #         data.append(j)
