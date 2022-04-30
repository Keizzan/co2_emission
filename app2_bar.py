"""
##############################################################################
#######                 PROJECT NAME : CO2 EMISSIONS                   #######
##############################################################################
                            Synopsis:
Script which plots bar chart showing top 50 countries with highest total co2 emission broken into separete sources.
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

### Prepare validation rules for Schema
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

### Validate with pandas_schema
errors = schema.validate(data)
errors_index_rows = [e.row for e in errors]


#### Isolate validated data from invalid
data_cleaned = data.drop(index=errors_index_rows)[:50]


## Export validated data and errors to csv file
pd.DataFrame({'Errors':errors}).to_csv('errors.csv')
data_cleaned.to_csv('cleaned_data.csv')



### Define style of plot
plt.style.use('fivethirtyeight')
### Plot horizontal bar plot and define size of plot
data_cleaned.plot(kind='bar', figsize=(30,10))
### Define title
plt.title('total carbon emission by country')
### Scale plot on x axis
plt.yscale('log')
### Print legend on plot
plt.legend()
### Fit plots within your figure cleanly
plt.tight_layout()
### Plot bar chart
plt.show()
