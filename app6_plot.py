"""
##############################################################################
#######                 PROJECT NAME : CO2 EMISSIONS                   #######
##############################################################################
                                Synopsis:
Script which plots 6 charts to compare co2 emission to gas price in 6 countries (India, Poland, Sweden, Japan, Germany, Belgium) over years.
"""
### Import necessary libraries
import pandas as pd
import numpy as np
from pandas_schema import Column, Schema
from pandas_schema.validation import CustomElementValidation, DateFormatValidation
import matplotlib.pyplot as plt

### Create data frame from 'fossil-fuel-co2-emissions-by-nation_csv' data and 'natural_gas_price_monthly_csv.csv'
data1 = pd.read_csv('fossil-fuel-co2-emissions-by-nation_csv.csv', parse_dates=['Year'])
data2 = pd.read_csv('natural_gas_price_monthly_csv.csv', parse_dates=['Month'])

### Change column Year into datetime object as year
data1['Year'] = data1['Year'].dt.strftime('%Y')
### Create column Year into datetime object as year
data2['Year'] = data2['Month'].dt.strftime('%Y')

### Isolate necessary columns ('Country', 'Year', 'Gas Fuel')
data1 = data1[['Year', 'Gas Fuel', 'Country']]
### Isolate necessary columns ('Year', 'Price')
data2 = data2[['Price', 'Year']]

### Custom number check function
def float_check(num):
    try:
        float(num)
    except ValueError:
        return False
    return True


### Prepare validation for Schema
float_validation = [CustomElementValidation(lambda i: float_check(i),'is not float value')]
null_validation = [CustomElementValidation(lambda a: a is not np.nan, 'cannot be empty')]

### Schema for pandas_schema validation data1
schema1 = Schema([
    Column('Year', [DateFormatValidation('%Y')]),
    Column('Gas Fuel',null_validation+float_validation),
    Column('Country',null_validation)
])

### Schema for pandas_schema validation data2
schema2 = Schema([
    Column('Year', [DateFormatValidation('%Y')]),
    Column('Price',null_validation+float_validation)
])

### Validation with pandas_schema
errors1 = schema1.validate(data1)
errors_index_rows1 = [e.row for e in errors1]
errors2 = schema2.validate(data2)
errors_index_rows2 = [e.row for e in errors2]

#### Isolate validated data from invalid
data1_cleaned = data1.drop(index=errors_index_rows1)
data2_cleaned = data2.drop(index=errors_index_rows2)

### Export validated data and errors to csv file
# pd.DataFrame({'Errors':errors}).to_csv('errors.csv')
# data1_cleaned.to_csv('cleaned_data1.csv')
# data2_cleaned.to_csv('cleaned_data2.csv')

### Group data2 by year and retrieve mean price for each year
data_2 = data2_cleaned.groupby('Year').mean()

### Create new dataframe by merging validated dataframes
data = data1_cleaned.merge(data_2, how='inner', on=['Year'])

### Groupby column Country 
data = data.groupby('Country')

### Retrieve groups for plotting
poland = data.get_group('POLAND')
india = data.get_group('INDIA')
swe = data.get_group('SWEDEN')
jap = data.get_group('JAPAN')
ger = data.get_group('GERMANY')
bel = data.get_group('BELGIUM')


### Define number of rows and columns for subplots
nrow=3
ncol=2
### Define axes and figure
fig, ax = plt.subplots(nrow, ncol, figsize=(30,15),constrained_layout=True, sharex=True)
plt.style.use('fivethirtyeight')

### First subplot
ax1 = ax[0,0]
ax1.bar(poland['Year'], poland['Gas Fuel'], color='g', alpha=0.5)
ax1.set_ylabel('Gas Fuel emissions', color='g')
ax2 = ax1.twinx() 
ax2.plot(poland['Year'], poland['Price'])
ax2.set_ylabel('Gas Price', color='b')
ax1.set_title('Carbon emmision by Gas Fuel vs Gas Price in Poland')



#### Second subplot
ax1 = ax[0,1]
ax1.bar(india['Year'], india['Gas Fuel'], color='g', alpha=0.5)
ax1.set_ylabel('Gas Fuel emissions', color='g')
ax2 = ax1.twinx() 
ax2.plot(india['Year'], india['Price'])
ax2.set_ylabel('Gas Price', color='b')
ax1.set_title('Carbon emmision by Gas Fuel vs Gas Price in India')

#### Third subplot
ax1 = ax[1,0]
ax1.bar(swe['Year'], swe['Gas Fuel'], color='g', alpha=0.5)
ax1.set_ylabel('Gas Fuel emissions', color='g')
ax2 = ax1.twinx() 
ax2.plot(swe['Year'], swe['Price'])
ax2.set_ylabel('Gas Price', color='b')
ax1.set_title('Carbon emmision by Gas Fuel vs Gas Price in Sweden')

#### Fourth subplot
ax1 = ax[1,1]
ax1.bar(jap['Year'], jap['Gas Fuel'], color='g', alpha=0.5)
ax1.set_ylabel('Gas Fuel emissions', color='g')
ax2 = ax1.twinx() 
ax2.plot(jap['Year'], jap['Price'])
ax2.set_ylabel('Gas Price', color='b')
ax1.set_title('Carbon emmision by Gas Fuel vs Gas Price in Japan')

#### Fifth subplot
ax1 = ax[2,0]
ax1.bar(ger['Year'], ger['Gas Fuel'], color='g', alpha=0.5)
ax1.set_ylabel('Gas Fuel emissions', color='g')
ax2 = ax1.twinx() 
ax2.plot(ger['Year'], ger['Price'])
ax2.set_ylabel('Gas Price', color='b')
ax1.set_title('Carbon emmision by Gas Fuel vs Gas Price in Germany')

#### Sixth subplot
ax1 = ax[2,1]
ax1.bar(bel['Year'], bel['Gas Fuel'], color='g', alpha=0.5)
ax1.set_ylabel('Gas Fuel emissions', color='g')
ax2 = ax1.twinx() 
ax2.plot(bel['Year'], bel['Price'])
ax2.set_ylabel('Gas Price', color='b')
ax1.set_title('Carbon emmision by Gas Fuel vs Gas Price in Belgium')

plt.show()