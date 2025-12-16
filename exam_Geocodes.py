#importing required modules
import geopy
import pandas as pd
from geopy.exc import GeocoderTimedOut
import time
import numpy as np

#reading our CSV dataset
data = pd.read_csv('Victims.csv')


#initialize geocoder.
locator = geopy.Nominatim(user_agent="jane.doe@gmail.com")

#the column of the CSV file we want to geocode is 'Birthplace'
Birthlocations = data['Birthplace']
#creating lists for longitude and latitude
Birthlatitudes = []
Birthlongitudes = []

#looping to geocode places
for i in range(len(Birthlocations)):
    print("Geocoding ...", Birthlocations[i])
    location = None
    try:
        Birthlocations[i] = Birthlocations[i]
        location = locator.geocode(Birthlocations[i],timeout=10)
        if location == None:
            Birthlatitudes.append(np.nan)
            Birthlongitudes.append(np.nan)
        else:
            Birthlatitudes.append(location.latitude)
            Birthlongitudes.append(location.longitude)
    except GeocoderTimedOut:
        print("Not able to geocode ...", Birthlocations[i])
        Birthlatitudes.append(np.nan)
        Birthlongitudes.append(np.nan)
    time.sleep(1)
    

#the column of the CSV file we want to geocode is 'Deathplace'    
Deathlocations = data['Deathplace']
#creating lists for longitude and latitude
Deathlatitudes = []
Deathlongitudes = []

#looping to geocode places
for i in range(len(Deathlocations)):
    print("Geocoding ...", Deathlocations[i])
    location = None
    try:
        Deathlocations[i] = Deathlocations[i]
        location = locator.geocode(Deathlocations[i],timeout=10)
        if location == None:
            Deathlatitudes.append(np.nan)
            Deathlongitudes.append(np.nan)
        else:
            Deathlatitudes.append(location.latitude)
            Deathlongitudes.append(location.longitude)
    except GeocoderTimedOut:
        print("Not able to geocode ...", Deathlocations[i])
        Deathlatitudes.append(np.nan)
        Deathlongitudes.append(np.nan)
    time.sleep(1)

#Making the lists into column in our dataset
data['Birthlatitude'] = Birthlatitudes
data['Birthlongitude'] = Birthlongitudes
data['Deathlatitude'] = Deathlatitudes
data['Deathlongitude'] = Deathlongitudes
#Saving the geocode columns to a new CSV file
data.to_csv('Victims_geocoded.csv', index=False, encoding='utf-8')