"""
##############################################################################
#######                 PROJECT NAME : CO2 EMISSIONS                   #######
##############################################################################
                                Synopsis:
Script which plots 6 horizontal bar charts showing top 10 countries with highest co2 emission from each sources.
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
### Sort from highest value in 'Total' column
data = data[['Country', 'Solid Fuel','Liquid Fuel', 'Gas Fuel', 'Cement','Gas Flaring', 'Total']].groupby('Country').sum()

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

### Schema for pandas_schema validation
schema = Schema([
    Column('Total',null_validation+int_validation),
    Column('Solid Fuel',null_validation+int_validation),
    Column('Liquid Fuel',null_validation+int_validation),
    Column('Gas Fuel',null_validation+int_validation),
    Column('Cement',null_validation+int_validation),
    Column('Gas Flaring',null_validation+int_validation)
])


### Validate with pandas_schema
errors = schema.validate(data)
errors_index_rows = [e.row for e in errors]


#### Isolate validated data from invalid
data_cleaned = data.drop(index=errors_index_rows)


## Export validated data and errors to csv file
pd.DataFrame({'Errors':errors}).to_csv('errors.csv')
data_cleaned.to_csv('cleaned_data.csv')


### Isolating separate DF and sort them
### by Total
data_total = data_cleaned[['Total']].sort_values('Total', ascending=False)[:10]
### by Solid Fuel
data_solid = data_cleaned[['Solid Fuel']].sort_values('Solid Fuel', ascending=False)[:10]
### by Liquid Fuel
data_fluid = data_cleaned[['Liquid Fuel']].sort_values('Liquid Fuel', ascending=False)[:10]
### by Gas Fuel
data_gas = data_cleaned[['Gas Fuel']].sort_values('Gas Fuel', ascending=False)[:10]
### by Liquid Fuel
data_cement = data_cleaned[['Cement']].sort_values('Cement', ascending=False)[:10]
### by Gas Flaring
data_flaring = data_cleaned[['Gas Flaring']].sort_values('Gas Flaring', ascending=False)[:10]

### Creating list of isolated dataframes
data_list = [data_total, data_solid, data_fluid,data_gas, data_cement, data_flaring]

### Define number of rows and columns for subplots
nrow=3
ncol=2
fig, axes = plt.subplots(nrow, ncol, figsize=(35,15),constrained_layout=True)


### Plot counter
count=0
### Loop for each subplot
for r in range(nrow):
    for c in range(ncol):
        ### Plotting subplot
        data_list[count].plot(kind='barh', ax=axes[r,c])
        a = axes[r,c]
        ### Extracting string from ndarray of columns for each dataframe
        value = np.array2string(data_list[count].columns.values, formatter={'int':lambda x: chr(x).encode()}, separator='').strip("['']")
        ### Set title for subplot
        a.set_title(f'Total carbon emission by country by {value}')
        a.set_xticklabels(data_list[count][value])
        a.invert_yaxis()
        count+=1
plt.show()
