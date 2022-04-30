"""
##############################################################################
#######                 PROJECT NAME : CO2 EMISSIONS                   #######
##############################################################################
                                Synopsis:
Script which plots 4 charts to compare total co2 emission to total drugs price for 10 countries in set years.
"""
### Import necessary libraries
import pandas as pd
import numpy as np
from pandas_schema import Column, Schema
from pandas_schema.validation import CustomElementValidation, DateFormatValidation
import matplotlib.pyplot as plt
import pycountry

### Create data frames from 'fossil-fuel-co2-emissions-by-nation_csv' and 'pharmaceutical-drug-spending.csv'
data1 = pd.read_csv('fossil-fuel-co2-emissions-by-nation_csv.csv')
data2 = pd.read_csv('pharmaceutical-drug-spending.csv')
### Isolate necessary columns
data1 = data1[['Year', 'Country', 'Total']]
data2 = data2[['LOCATION','TIME','TOTAL_SPEND']]

### Create new column with full name of location based on alpha-3 code
data2['Country'] = data2['LOCATION'].apply(lambda x: pycountry.countries.get(alpha_3=x).name)
###Convert Country column into capitilized
data1['Country'] = data1['Country'].str.capitalize()
data2['Country'] = data2['Country'].str.capitalize()

### Custom number check function
def int_check(num):
    try:
        int(num)
    except ValueError:
        return False
    return True

### Custom float number check function
def float_check(num):
    try:
        float(num)
    except ValueError:
        return False
    return True



### Prepare validation rules for Schema
float_validation = [CustomElementValidation(lambda i: float_check(i),'is not float value')]
int_validation = [CustomElementValidation(lambda i: int_check(i),'is not integer value')]
null_validation = [CustomElementValidation(lambda a: a is not np.nan, 'cannot be empty')]

### Schema for pandas_schema validation data1
schema1 = Schema([
    Column('Year', [DateFormatValidation('%Y')]),
    Column('Total',null_validation+int_validation),
    Column('Country',null_validation)
])

### Schema for pandas_schema validation data2
schema2 = Schema([
    Column('TIME', [DateFormatValidation('%Y')]),
    Column('TOTAL_SPEND',null_validation+int_validation),
    Column('LOCATION',null_validation),
    Column('Country',null_validation)
])

### Validate with pandas_schema
errors1 = schema1.validate(data1)
errors_index_rows1 = [e.row for e in errors1]
errors2 = schema2.validate(data2)
errors_index_rows2 = [e.row for e in errors2]

#### Isolate validated data from invalid
data1_cleaned = data1.drop(index=errors_index_rows1)
data2_cleaned = data2.drop(index=errors_index_rows2)

## Export validated data and errors to csv file
pd.DataFrame({'Errors':errors1}).to_csv('errors1.csv')
data1_cleaned.to_csv('cleaned_data1.csv')
pd.DataFrame({'Errors':errors2}).to_csv('errors2.csv')
data2_cleaned.to_csv('cleaned_data2.csv')

### Merge dataframes into one on Year/TIME and Country and drop LOCATION and TIME columns
data = data1_cleaned.merge(data2_cleaned, how='inner' ,left_on=['Year', 'Country'], right_on=['TIME', 'Country']).drop(['LOCATION','TIME'], axis=1)

### Group by Year
data = data.groupby('Year')

### Declare groups for certain year
group1 = data.get_group(1980).set_index('Country')[:10]
group2 = data.get_group(1985).set_index('Country')[:10]
group3 = data.get_group(1990).set_index('Country')[:10]
group4 = data.get_group(1995).set_index('Country')[:10]


### Define number of rows and columns for subplots
nrow=2
ncol=2
width = 0.25

### Define axes and figure
fig, ax = plt.subplots(nrow, ncol, figsize=(30,15),sharey=True, constrained_layout=True)
plt.style.use('fivethirtyeight')

### First subplot
ax1 = ax[0,0]
ax1.plot(group1.index, group1['Total'], color='g')
ax1.set_ylabel('Carbon emissions', color='g')
ax2 = ax1.twinx() 
ax2.bar(group1.index, group1['TOTAL_SPEND'], alpha=0.5)
ax2.set_ylabel('Drug costs')
ax2.set_title('Total carbon emissions vs total cost of drugs in 1980')

#### Second subplot
ax1 = ax[0,1]
ax1.plot(group2.index, group2['Total'], color='g')
ax1.set_ylabel('Carbon emissions', color='g')
ax2 = ax1.twinx() 
ax2.bar(group2.index, group2['TOTAL_SPEND'], alpha=0.5)
ax2.set_ylabel('Drug costs')
ax2.set_title('Total carbon emissions vs total cost of drugs in 1985')


#### Third subplot
ax1 = ax[1,0]
ax1.plot(group3.index, group3['Total'], color='g')
ax1.set_ylabel('Carbon emissions', color='g')
ax2 = ax1.twinx() 
ax2.bar(group3.index, group3['TOTAL_SPEND'], alpha=0.5)
ax2.set_ylabel('Drug costs')
ax2.set_title('Total carbon emissions vs total cost of drugs in 1990')


#### Fourth subplot
ax1 = ax[1,1]
ax1.plot(group4.index, group4['Total'], color='g')
ax1.set_ylabel('Carbon emissions', color='g')
ax2 = ax1.twinx() 
ax2.bar(group4.index, group4['TOTAL_SPEND'], alpha=0.5)
ax2.set_ylabel('Drug costs')
ax2.set_title('Total carbon emissions vs total cost of drugs in 1995')

plt.show()