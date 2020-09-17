#!/usr/bin/env python
# coding: utf-8

# In[1]:


import json
import numpy as np
import pandas as pd
import requests


# In[2]:


#Making python function x with parameter y. This funtion will get back value as 
#python dictionary if status_code==200, else None

def get_json(url):
    response=requests.get(url)
    if response.status_code==200:
        return json.loads(response.content.decode('utf-8'))
    else:
        return None


# In[3]:


#Calling API Covid19
#recapitulation on 2020 Sept 01 di dunia
record_date = '2020-08-17'
covid_url = 'https://covid19-api.org/api/status?date='+record_date
df_covid_worldwide = pd.io.json.json_normalize(get_json(covid_url))
print(df_covid_worldwide.head())


# In[4]:


#Change date format
#change format column 'last_update' use to_datetime function
#with format 'YYYY-MM-DD HH:MM:SS'
df_covid_worldwide['last_update']=pd.to_datetime(df_covid_worldwide['last_update'],
                                                format='%Y-%m-%d %H:%M:%S')
#then change datetime format to date format with funtion date() by lambda funtion for each rows
df_covid_worldwide['last_update']=df_covid_worldwide['last_update'].apply(lambda x: x.date())


# In[5]:


#Take the data countries
#make a dataframe countries from url countries
countries_url = 'https://covid19-api.org/api/countries'
df_countries =pd.io.json.json_normalize(get_json(countries_url))
#rename "alpha2" to be "country" and then choose columns "name" and "country"
df_countries=df_countries.rename(columns={'alpha2':'country'})[['name','country']]
print(df_countries.head())


# In[6]:


#Merge Covid19 data and Countries using 'merge' function
df_covid_denormalized=pd.merge(df_covid_worldwide,df_countries,on='country')
print(df_covid_denormalized.head())


# In[7]:


#Counting the fatality ratio
#Fatality ratio is division between the columns deaths and cases
df_covid_denormalized['fatality_ratio']=df_covid_denormalized['deaths']/df_covid_denormalized['cases']
print(df_covid_denormalized.head())


# In[8]:


#Analysis country with high fatality ratio
#Take big 20 country using sort_values
df_top20_fatality=df_covid_denormalized.sort_values(by='fatality_ratio',ascending=False).head(20)
print(df_top20_fatality)


# In[9]:


#Visualisation
import matplotlib.pyplot as plt
plt.figure(figsize=(20,8))
#determine the x axis and y axis
#x is name ,y is number of fatality ratio
x=df_top20_fatality['name']
y=df_top20_fatality['fatality_ratio']
plt.bar(x,y)
plt.xlabel('Country Name')
plt.ylabel('Fatality Ratio')
plt.title("Top 20 Highest Fatality Rate Countries")
plt.xticks(rotation=90)
plt.tight_layout()
plt.show()


# In[10]:


#COVID-19 IN ASEAN
#combine dataframe
#comparing Covid19 in Indonesia with another country in ASEAN 
countries=['ID','MY','SG','TH','VN','PH','BN','LA','KH','MM','TL']
i=0
for country in countries:
    covid_timeline_url = 'https://covid19-api.org/api/timeline/'+country    
    df_covid_timeline = pd.io.json.json_normalize(get_json(covid_timeline_url))
    df_covid_timeline['last_update'] = pd.to_datetime(df_covid_timeline['last_update'], format='%Y-%m-%d %H:%M:%S')
    df_covid_timeline['last_update'] = df_covid_timeline['last_update'].apply(lambda x: x.date())
    if i==0:
        df_covid_timeline_merged = df_covid_timeline
    else:
        df_covid_timeline_merged = df_covid_timeline.append(df_covid_timeline_merged, ignore_index=True)
    i=i+1
        
print(df_covid_timeline_merged.head(30))
print(df_covid_timeline_merged.shape)


# In[11]:


#Merge Data Covid19 with data country
#Combine df_covid_timeline_merged and df_countries with country column as pivot
df_covid_timeline_denormalized=pd.merge(df_covid_timeline_merged,df_countries,on='country')
print(df_covid_timeline_denormalized.head())


# In[12]:


#Covid19 in March until now in ASEAN
import datetime
#get filter for 'last_update'. Take data from 1 March 2020 until now
#Change format datetime.date with YYYY mm dd
df_covid_timeline_denormalized=df_covid_timeline_denormalized[(df_covid_timeline_denormalized['last_update']>= datetime.date(2020,3,1))]
print(df_covid_timeline_denormalized.head())


# In[15]:


#Visualisation Covid19 in ASEAN
plt.clf()
countries=['ID','MY','SG','TH','VN','PH','BN','LA','KH','MM','TL']
for country in countries:
    country_data=df_covid_timeline_denormalized['country']==country
    x=df_covid_timeline_denormalized[country_data]['last_update']
    y=df_covid_timeline_denormalized[country_data]['cases']
    plt.plot(x,y,label=country)
    plt.legend()
    plt.xlabel('Record Date')
    plt.ylabel('Total Case')
    plt.title('ASEAN COVID-19 Cases Comparison')
    plt.show()


# In[13]:


print(df_covid_timeline_denormalized.head())
print(df_covid_timeline_denormalized.shape)


# In[23]:


plt.figure(figsize=(40,40))
df_covid_timeline_denormalized.groupby(['last_update','country'])['cases'].sum().unstack().plot()
plt.xlabel('Record Date')
plt.ylabel('Total Cases')
plt.title("Covid-19 in ASEAN",loc="center",color='blue')
plt.legend(title="Negara",ncol=2,fontsize=9)
plt.ylim(ymin=0)
#annotate
#plt.annotate('Kasus di Indonesia terus meningkat',xy=(6,200000),
 #          xytext=(3,220000),color='red',
  #        arrowprops=dict(arrowstyle='fancy',connectionstyle='arc3',color='red'))
plt.show()


# In[42]:


#Covid19 in Indonesia
dataset_id = df_covid_timeline_denormalized[(df_covid_timeline_denormalized['country']=='ID')]
print(dataset_id.head())


# In[43]:


#Visualisation
plt.figure(figsize=(10,7))
x=dataset_id['last_update']
y1=dataset_id['cases']
y2=dataset_id['deaths']
y3=dataset_id['recovered']
labelss=['cases','deaths','recovered']
plt.plot(x,y1,label=labelss[0])
plt.plot(x,y2,label=labelss[1])
plt.plot(x,y3,label=labelss[2])
plt.xlabel('Record Date')
plt.ylabel('People')
plt.title('COVID-19 in Indonesia')
plt.legend()
plt.ylim(ymin=0)
plt.show()


# In[ ]:




