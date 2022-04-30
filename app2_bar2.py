"""
##############################################################################
#######                 PROJECT NAME : CO2 EMISSIONS                   #######
##############################################################################
                                Synopsis:
Script which plots horizontal bar chart showing top 20 countries with highest total co2 emission broken into separete sources.
"""
### Import necessary libraries
import pandas as pd
import numpy as np
from pandas_schema import Column, Schema
from pandas_schema.validation import CustomElementValidation
import matplotlib.pyplot as plt


### Create data frame from 'fossil-fuel-co2-emissions-by-nation_csv' data
### Isolate necessary columns ('Country', 'Total', 'Solid Fuel', 'Liquid Fuel', 'Gas Fuel', 'Cement', 'Gas Flaring') and group data by Country and sum all values in columns
data = pd.read_csv('fossil-fuel-co2-emissions-by-nation_csv.csv')
### Sort from highest value in 'Total' column and then drop it
data = data[['Country', 'Solid Fuel','Liquid Fuel', 'Gas Fuel', 'Cement','Gas Flaring', 'Total']].groupby('Country').sum().sort_values('Total', ascending=False).drop('Total', axis=1)

### Custom number check function
def int_check(num):
    try:
        int(num)
    except ValueError:
        return False
    return True

### Prepare validation for Schema
int_validation = [CustomElementValidation(lambda i: int_check(i),'is not integer value')]
null_validation = [CustomElementValidation(lambda a: a is not np.nan, 'cannot be empty')]

### Schema for pandas_schema validation
schema = Schema([
    Column('Solid Fuel',null_validation+int_validation),
    Column('Liquid Fuel',null_validation+int_validation),
    Column('Gas Fuel',null_validation+int_validation),
    Column('Cement',null_validation+int_validation),
    Column('Gas Flaring',null_validation+int_validation)
])

### Validation with pandas_schema
errors = schema.validate(data)
errors_index_rows = [e.row for e in errors]


#### Isolate validated data from invalid
data_cleaned = data.drop(index=errors_index_rows)[:20]


## Export validated data and errors to csv file
pd.DataFrame({'Errors':errors}).to_csv('errors.csv')
data_cleaned.to_csv('cleaned_data.csv')

### Defining list of indexes in dataframe
keys = data_cleaned.index.values
nrows = len(keys)

### Defining subplots
fig, axes = plt.subplots(nrows, sharex=True, figsize=(35, 15), constrained_layout=True)   
fig.suptitle('Total Carbon Emission by each country')
plt.style.use('fivethirtyeight')


### Loop through each axis and plotting chart for each country found in keys
counter = 0
for r in range(nrows):
    data[data.index.values == keys[counter]].plot(kind='barh', ax=axes[r], legend=False)
    counter += 1

### Setting Xlabel and scale it
plt.xlabel('Total Carbon Emission (million metric tons of C)')
plt.xscale('log')

### Display legend and title
plt.legend()

### Show chart
plt.show()