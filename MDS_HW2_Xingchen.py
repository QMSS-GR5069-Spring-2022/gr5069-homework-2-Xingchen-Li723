#!/usr/bin/env python
# coding: utf-8

# In[1]:


import os
os.chdir('D:\columbia qmss\MDS\course_content21\Exercises\HW02')


# In[2]:


import pandas as pd
df = pd.read_csv("U.S._Chronic_Disease_Indicators__CDI_.csv")


# ## Selection of Data and Reshaping the Data

# In[3]:


# Glimpse the data
df.columns


# In[4]:


df['DataValueType'].unique()


# In[5]:


df['DataValueUnit'].unique()


# In[6]:


df["Topic"].unique()


# In[7]:


df["StratificationCategory1"].unique()


# In[15]:


df["Stratification1"].unique()


# In[8]:


df["Question"][df['Question'].str.startswith("Binge")].unique()


# The data contains lots of indicators and is in a long format format.
#
# 1. Remove all columns you do not need for the analysis (All done in Python, of course. No Excel acrobatics.). We are interested in two sets of variables. Select the following variables and remove all others:
#     a) **Binge Drinking**:
#     _Binge drinking prevalence among adults aged >= 18 years_, Crude Prevalence in Percent.
#     We would like to obtain this variable for the overall population, as well separately for _females_ and _males_.\
#     b) **Poverty**:
#     _Poverty, Crude Prevalence in Percent_. We only want the overall poverty prevalence to make things a bit easier.

# In[9]:


# Flitering
df_bp = df.query('DataValueType == "Crude Prevalence"                  & DataValueUnit == "%"                  & (Question == "Binge drinking prevalence among adults aged >= 18 years"                  & StratificationCategory1 == ["Overall", "Gender"])                  or (Question == "Poverty"                  & StratificationCategory1 =="Overall")                  ')[
    ['YearStart', 'LocationAbbr', 'LocationDesc',
     'Question', 'DataValueAlt',
     'StratificationCategory1', 'Stratification1']
]
print(df_bp.shape)
df_bp.head()


# 2. Convert the dataset to a wide format data set using the commands from the `pandas` package.

# In[20]:


df_bp_wide = df_bp.pivot(
    index = ['LocationDesc','LocationAbbr','YearStart'],
    columns = ['Question','Stratification1'],
    values = 'DataValueAlt')
df_bp_wide.columns = list(map("_".join, df_bp_wide.columns))
df_bp_wide.head()


# 3. Rename the variables to follow the format below.
#
#     Your dataset should now be in a wide state-year format with the following variables:
#       - `state`: Name of the State
#       - `stateabb`: State Abbreviation
#       - `year`: year of observation
#       - `binge_all`: Binge drinking prevalence among _all_ adults aged >= 18 years
#       - `binge_male`: Binge drinking prevalence among _male_ adults aged >= 18 years
#       - `binge_female`: Binge drinking prevalence among _female_ adults aged >= 18 years
#       - `poverty`: Poverty, Crude Prevalence in Percent
#
#     Provide an overview of the dataset by printing its size (using the `shape` command) and some summary statistics (using the `describe` command).
#
#     Save the cleaned dataset as `binge_clean.csv`. That file should be included in the uploaded files for your homework submission.

# In[27]:


binge_clean = df_bp_wide.reset_index()
binge_clean = binge_clean.rename(columns = {'LocationDesc':'state',
                                          'LocationAbbr': 'stateabb',
                                          'YearStart' : 'year',
                                          'Binge drinking prevalence among adults aged >= 18 years_Female': 'binge_female',
                                          'Binge drinking prevalence among adults aged >= 18 years_Male': 'binge_male',
                                          'Binge drinking prevalence among adults aged >= 18 years_Overall': 'binge_all',
                                          'Poverty_Overall': 'poverty'})

binge_clean.head()


# In[29]:


binge_clean.shape


# In[31]:


binge_clean.describe()


# In[32]:


binge_clean.to_csv('binge_clean.csv', index = False)


# ## Data Transformation and Summary Results

# 4. Produce a table that shows the overall, female, and male binge drinking prevalences across U.S. States in the most recent year of data for the Top 10 binge drinking states (i.e. the ones with the highest prevalence in the overall population). Use the relevant `pandas` commands to select the right variables, sort the data, and filter the data frame.

# In[33]:


top10_binge =  binge_clean.query('year==2019').drop('poverty',axis = 1).nlargest(10,'binge_all',keep='all')
#top10_binge =  binge_clean[binge_clean['year']==2019].drop('poverty',axis=1).nlargest(10,'binge_all',keep='all')
top10_binge


# 5. Calculate the average annual growth rates (in percent) of overall binge drinking across states for the years the data is available. One way to get these growth rates, is to group the data by state (`groupby`) and use the `first()` and `last()` commands to get the first and last non-NA percentage followed by dividing the calculated percentage increase by the number of years data is available for. Alternatively, you could use the `pct_change` function to help you out. Provide a table of the _5 states with the largest increases_ and the _5 states with the largest decreases_ in binge drinking prevalence over the time period.

# In[49]:


binge_clean_copy = binge_clean[["state","year","binge_all"]].dropna()
binge_clean_copy.head()


# In[63]:


avg_binge_clean_first = binge_clean_copy.groupby('state').first().rename(columns={"year":"first_year","binge_all":"binge_all_first"})
avg_binge_clean_last = binge_clean_copy.groupby('state').last().rename(columns={"year":"last_year","binge_all":"binge_all_last"})
avg_binge_clean = pd.merge(avg_binge_clean_first,avg_binge_clean_last, how='left',on='state')
avg_binge_clean['average_annual_growth_rates'] = (avg_binge_clean['binge_all_last']-avg_binge_clean['binge_all_first'])/(avg_binge_clean['last_year']-avg_binge_clean['first_year'])
avg_binge_clean


# In[65]:


avg_binge_clean.nlargest(5,'average_annual_growth_rates',keep='all')


# In[67]:


avg_binge_clean.nsmallest(5,'average_annual_growth_rates',keep='all')
