"""
##############################################################################
#######                 PROJECT NAME : CO2 EMISSIONS                   #######
##############################################################################
                                Synopsis:
Script which plots 4 charts to compare total co2 emission to total drugs expenses for 4 countries (USA, Belgium, Poland, Australia) over the years.
"""
### Import necessary libraries
import pandas as pd
import numpy as np
from pandas_schema import Column, Schema
from pandas_schema.validation import CustomElementValidation, DateFormatValidation
import matplotlib.pyplot as plt

### Create data frames from 'fossil-fuel-co2-emissions-by-nation_csv' and 'pharmaceutical-drug-spending.csv'
data1 = pd.read_csv('fossil-fuel-co2-emissions-by-nation_csv.csv')
data2 = pd.read_csv('pharmaceutical-drug-spending.csv')
### Isolate necessary columns
data1 = data1[['Year', 'Country', 'Total']]
data2 = data2[['LOCATION','TIME','TOTAL_SPEND']]

### Custom number check function
def int_check(num):
    try:
        int(num)
    except ValueError:
        return False
    return True


### Prepare validation rules for Schema
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
    Column('LOCATION',null_validation)
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
pd.DataFrame({'Errors':errors2}).to_csv('errors2.csv')
data1_cleaned.to_csv('cleaned_data1.csv')
data2_cleaned.to_csv('cleaned_data2.csv')

### Group data1 by country
data_1 = data1_cleaned.groupby('Country')
### Group data2 by location
data_2 = data2_cleaned.groupby('LOCATION')

### Isolate data for USA from both dataframes and merge them
usa1 = data_1.get_group('UNITED STATES OF AMERICA')
usa2 = data_2.get_group('USA')
usa = usa1.merge(usa2, how='inner', left_on='Year', right_on='TIME')
### Isolate data for BELGIUM from both dataframes and merge them
bel1 = data_1.get_group('BELGIUM')
bel2 = data_2.get_group('BEL')
bel = bel1.merge(bel2, how='inner', left_on='Year', right_on='TIME')
### Isolate data for POLAND from both dataframes and merge them
pol1 = data_1.get_group('POLAND')
pol2 = data_2.get_group('POL')
pol = pol1.merge(pol2, how='inner', left_on='Year', right_on='TIME')
### Isolate data for AUSTRIA from both dataframes and merge them
aus1 = data_1.get_group('AUSTRALIA')
aus2 = data_2.get_group('AUS')
aus = aus1.merge(aus2, how='inner', left_on='Year', right_on='TIME')

### Define number of rows and columns for subplots
nrow=2
ncol=2

### Define axes and figure
fig, ax = plt.subplots(nrow, ncol, figsize=(30,15),constrained_layout=True)
plt.style.use('fivethirtyeight')

### First subplot
ax1 = ax[0,0]
ax1.bar(usa['Year'], usa['Total'], color='g', alpha=0.5)
ax1.set_ylabel('Carbon emissions', color='g')
ax2 = ax1.twinx() 
ax2.plot(usa['Year'], usa['TOTAL_SPEND'])
ax2.set_ylabel('Total Drugs Expense (mln)', color='b')
ax1.set_title('Carbon emmision against drugs spend in USA')

#### Second subplot
ax1 = ax[0,1]
ax1.bar(bel['Year'], bel['Total'], color='g', alpha=0.5)
ax1.set_ylabel('Carbon emissions', color='g')
ax2 = ax1.twinx() 
ax2.plot(bel['Year'], bel['TOTAL_SPEND'])
ax2.set_ylabel('Total Drugs Expense (mln)', color='b')
ax1.set_title('Carbon emmision against drugs spend in Belgium')

#### Third subplot
ax1 = ax[1,0]
ax1.bar(pol['Year'], pol['Total'], color='g', alpha=0.5)
ax1.set_ylabel('Carbon emissions', color='g')
ax2 = ax1.twinx() 
ax2.plot(pol['Year'], pol['TOTAL_SPEND'])
ax2.set_ylabel('Total Drugs Expense (mln)', color='b')
ax1.set_title('Carbon emmision against drugs spend in Poland')

#### Fourth subplot
ax1 = ax[1,1]
ax1.bar(aus['Year'], aus['Total'], color='g', alpha=0.5)
ax1.set_ylabel('Carbon emissions', color='g')
ax2 = ax1.twinx() 
ax2.plot(aus['Year'], aus['TOTAL_SPEND'])
ax2.set_ylabel('Total Drugs Expense (mln)', color='b')
ax1.set_title('Carbon emmision against drugs spend in Australia')

plt.show()