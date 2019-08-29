

import pandas as pd
import numpy as np
from scipy.stats import ttest_ind


# Definitions:
# * A _quarter_ is a specific three month period, Q1 is January through March, Q2 is April through June, Q3 is July through September, Q4 is October through December.
# * A _recession_ is defined as starting with two consecutive quarters of GDP decline, and ending with two consecutive quarters of GDP growth.
# * A _recession bottom_ is the quarter within a recession which had the lowest GDP.
# * A _university town_ is a city which has a high percentage of university students compared to the total population of the city.
# 
# **Hypothesis**: University towns have their mean housing prices less effected by recessions. Run a t-test to compare the ratio of the mean price of houses in university towns the quarter before the recession starts compared to the recession bottom. (`price_ratio=quarter_before_recession/recession_bottom`)
# 
# The following data files are available :
# * From the [Zillow research data site](http://www.zillow.com/research/data/) there is housing data for the United States. In particular the datafile for [all homes at a city level](http://files.zillowstatic.com/research/public/City/City_Zhvi_AllHomes.csv), ```City_Zhvi_AllHomes.csv```, has median home sale prices at a fine grained level.
# * From the Wikipedia page on college towns is a list of [university towns in the United States](https://en.wikipedia.org/wiki/List_of_college_towns#College_towns_in_the_United_States) which has been copy and pasted into the file ```university_towns.txt```.
# * From Bureau of Economic Analysis, US Department of Commerce, the [GDP over time](http://www.bea.gov/national/index.htm#gdp) of the United States in current dollars (use the chained value in 2009 dollars), in quarterly intervals, in the file ```gdplev.xls```. For this assignment, only look at GDP data from the first quarter of 2000 onward.



# Use this dictionary to map state names to two letter acronyms
states = {'OH': 'Ohio', 'KY': 'Kentucky', 'AS': 'American Samoa', 'NV': 'Nevada', 'WY': 'Wyoming', 'NA': 'National', 'AL': 'Alabama', 'MD': 'Maryland', 'AK': 'Alaska', 'UT': 'Utah', 'OR': 'Oregon', 'MT': 'Montana', 'IL': 'Illinois', 'TN': 'Tennessee', 'DC': 'District of Columbia', 'VT': 'Vermont', 'ID': 'Idaho', 'AR': 'Arkansas', 'ME': 'Maine', 'WA': 'Washington', 'HI': 'Hawaii', 'WI': 'Wisconsin', 'MI': 'Michigan', 'IN': 'Indiana', 'NJ': 'New Jersey', 'AZ': 'Arizona', 'GU': 'Guam', 'MS': 'Mississippi', 'PR': 'Puerto Rico', 'NC': 'North Carolina', 'TX': 'Texas', 'SD': 'South Dakota', 'MP': 'Northern Mariana Islands', 'IA': 'Iowa', 'MO': 'Missouri', 'CT': 'Connecticut', 'WV': 'West Virginia', 'SC': 'South Carolina', 'LA': 'Louisiana', 'KS': 'Kansas', 'NY': 'New York', 'NE': 'Nebraska', 'OK': 'Oklahoma', 'FL': 'Florida', 'CA': 'California', 'CO': 'Colorado', 'PA': 'Pennsylvania', 'DE': 'Delaware', 'NM': 'New Mexico', 'RI': 'Rhode Island', 'MN': 'Minnesota', 'VI': 'Virgin Islands', 'NH': 'New Hampshire', 'MA': 'Massachusetts', 'GA': 'Georgia', 'ND': 'North Dakota', 'VA': 'Virginia'}





def get_list_of_university_towns():
    #'''Returns a DataFrame of towns and the states they are in from the 
    #university_towns.txt list. The format of the DataFrame should be:
    #DataFrame( [ ["Michigan", "Ann Arbor"], ["Michigan", "Yipsilanti"] ], 
    #columns=["State", "RegionName"]  )

    
    towns = pd.read_table('university_towns.txt', header = -1, names = ['Town'])
    
    reverse_states = {v: k for k, v in states.items()}
    
    newtowns = list()
    
    [newtowns.append(towns.iloc[i]['Town'].split('(')[0]) for i in range(len(towns))]
    
    newstates = list()
    
    [newstates.append(newtowns[i].split('[')[0]) for i in range(len(newtowns))]
    
    finallist = list()
    
    for name in newstates:
        if name in reverse_states:
            state = name
        else:
            finallist.append([state, name])
           
    statenames = list()
    [statenames.append(finallist[i][0]) for i in range(len(finallist))]
    cities = list()
    [cities.append(finallist[i][1]) for i in range(len(finallist))]
    
    for i in range(len(cities)):
        cities[i] = cities[i].strip()
    
    
    data = {'State': statenames, 'RegionName': cities}
    
    university_towns = pd.DataFrame(data)

    return university_towns


def get_recession_start():
    #'''Returns the year and quarter of the recession start time as a 
    #string value in a format such as 2005q3'''
    
    gdp = pd.read_excel('gdplev.xls', header=5)
    
    columnskeep = ['Unnamed: 3', 'GDP in billions of current dollars.1', 'GDP in billions of chained 2009 dollars.1']
    
    gdp = (gdp[columnskeep]
           .reset_index()
          .drop([0,1])
          .rename(columns = {'Unnamed: 3': 'Quarter',
                   "GDP in billions of current dollars.1": 'Current GDP',
                   'GDP in billions of chained 2009 dollars.1': 'GDP chained 2009'}))
    
    gdp = (gdp[gdp['Quarter'] >= '2000q1']
           .drop('index', axis=1))
    
    for i in range(len(gdp['GDP chained 2009'])):
        if (i+2) > len(gdp):
            break
        first = gdp['GDP chained 2009'].iloc[i]
        second = gdp['GDP chained 2009'].iloc[i+1]
        third = gdp['GDP chained 2009'].iloc[i+2]
        
        if second < first:
            if third < second:
                return gdp['Quarter'].iloc[i+1]
         

def get_recession_end():
    

    #'''Returns the year and quarter of the recession end time as a 
    #string value in a format such as 2005q3'''
    
    gdp = pd.read_excel('gdplev.xls', header=5)
    
    columnskeep = ['Unnamed: 3', 'GDP in billions of current dollars.1', 'GDP in billions of chained 2009 dollars.1']
    
    gdp = (gdp[columnskeep]
           .reset_index()
          .drop([0,1])
          .rename(columns = {'Unnamed: 3': 'Quarter',
                   "GDP in billions of current dollars.1": 'Current GDP',
                   'GDP in billions of chained 2009 dollars.1': 'GDP chained 2009'}))
    
    
    gdp = (gdp[gdp['Quarter'] >= get_recession_start()]
           .drop('index', axis=1))
    
    for i in range(len(gdp['GDP chained 2009'])):
        if (i+2) > len(gdp):
            break
        first = gdp['GDP chained 2009'].iloc[i]
        second = gdp['GDP chained 2009'].iloc[i+1]
        third = gdp['GDP chained 2009'].iloc[i+2]
        
        if second > first:
            if third > second:
                return gdp['Quarter'].iloc[i+2]


def get_recession_bottom():
    #'''Returns the year and quarter of the recession bottom time as a 
    #string value in a format such as 2005q3'''
    
    gdp = pd.read_excel('gdplev.xls', header=5)
    
    columnskeep = ['Unnamed: 3', 'GDP in billions of current dollars.1', 'GDP in billions of chained 2009 dollars.1']
    
    gdp = (gdp[columnskeep]
           .reset_index()
          .drop([0,1])
          .rename(columns = {'Unnamed: 3': 'Quarter',
                   "GDP in billions of current dollars.1": 'Current GDP',
                   'GDP in billions of chained 2009 dollars.1': 'GDP chained 2009'}))
    
    
    gdp = (gdp[(gdp['Quarter'] >= get_recession_start()) & (gdp['Quarter'] <= get_recession_end()) ]
           .drop('index', axis=1))
    
   
    return list(gdp[gdp['GDP chained 2009'] == 14355.6]['Quarter'])[0]


def convert_housing_data_to_quarters():

    #'''Converts the housing data to quarters and returns it as mean 
    #values in a dataframe. This dataframe should be a dataframe with
    #columns for 2000q1 through 2016q3, and should have a multi-index
    #in the shape of ["State","RegionName"]  A quarter is a specific three month period, Q1 is January through March,
    #Q2 is April through June, Q3 is July through September, Q4 is October through December..

    import numbers
    
    housing = pd.read_csv('City_Zhvi_AllHomes.csv')
    
    cols = [c for c in housing.columns if c.lower()[:1] != '1']
    
    cols_copy = cols.copy()
    
    #['RegionID', 'RegionName', 'State', 'Metro', 'CountryName']
    
    quarterDict = {'-01': 'q1', '-02': 'q1', '-03':'q1',
                  '-04': 'q2', '-05': 'q2', '-06':'q2',
                  '-07':'q3', '-08': 'q3', '-09':'q3',
                  '-10':'q4', '-11':'q4', '-12':'q4'}
    
    for i in range(len(cols)):
        if cols[i][4] == '-':
            cols[i] = cols[i][0:4]  + quarterDict[cols[i][4:]]
        
    newhousing = housing[cols_copy]
    
    newhousing.columns = cols
    
    newhousing = (newhousing.groupby(by=newhousing.columns, axis=1).apply(
        lambda g: g.mean(axis=1) if isinstance(g.iloc[0,0],numbers.Number) else g.iloc[:,0])
                 .drop(['Metro', 'RegionID', 'CountyName', 'SizeRank'], axis=1))
    
    newhousing['State'] = [states[name] for name in newhousing['State']]    
    
    newhousing=newhousing.set_index(['State', 'RegionName'])
    
    return newhousing

def run_ttest():
    #'''First creates new data showing the decline or growth of housing prices
    #between the recession start and the recession bottom. Then runs a ttest
    #comparing the university town values to the non-university towns values, 
    #return whether the alternative hypothesis (that the two groups are the same)
    #is true or not as well as the p-value of the confidence. 
    
    #Return the tuple (different, p, better) where different=True if the t-test is
    #True at a p<0.01 (we reject the null hypothesis), or different=False if 
    #otherwise (we cannot reject the null hypothesis). 
    
    import statistics as st
    
    newdata = convert_housing_data_to_quarters()
    
    cols = list(newdata)
    
    beforeRecession = str()
    
    ####Find quarter before recession start
    for i in range(len(cols)):
        if cols[i] == get_recession_start():
            beforeRecession = cols[i-1]
            
    newdata = newdata[[beforeRecession, get_recession_bottom()]]
    
    newdata['Ratio'] = newdata[beforeRecession] / newdata[get_recession_bottom()]
    
    uni = get_list_of_university_towns().set_index(['State', 'RegionName'])
    
    newdata = newdata.sort_index()
    
    uni = uni.merge(newdata,how='inner', left_index = True, right_index= True)
    
    newdata = newdata.drop(labels = list(uni.index))
    
    ttest = ttest_ind(list(uni['Ratio']), list(newdata['Ratio']), nan_policy= 'omit')
    
    return (ttest[1] < 0.01, ttest[0], 'university town' if ttest[0] < 0 else 'university town')





