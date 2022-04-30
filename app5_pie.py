"""
##############################################################################
#######                 PROJECT NAME : CO2 EMISSIONS                   #######
##############################################################################
                                Synopsis:
Script plots pie chart comparing top 20% contribiutors of co2 emission vs rest of the world
"""
### Import necessary libraries
import pandas as pd
import numpy as np
from pandas_schema import Column, Schema
from pandas_schema.validation import CustomElementValidation
import matplotlib.pyplot as plt

### Create data frame from 'fossil-fuel-co2-emissions-by-nation_csv' data
### Isolate two columns ('Country' and 'Total') and group data by Country
data_1 = pd.read_csv('fossil-fuel-co2-emissions-by-nation_csv.csv')
data_1 = data_1[['Country','Total']].groupby('Country').sum()

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
    Column('Total',null_validation+int_validation)
])

### Validate with pandas_schema
errors = schema.validate(data_1)
errors_index_rows = [e.row for e in errors]

#### Isolate validated data from invalid, return dataframe sorted by column Total from max
data_cleaned = data_1.drop(index=errors_index_rows).sort_values('Total', ascending=False)


## Export validated data and errors to csv file
pd.DataFrame({'Errors':errors}).to_csv('errors.csv')
data_cleaned.to_csv('cleaned_data.csv')

### Find numbers 80/20 ratio of records
total = data_cleaned.shape[0]
first_20 = int(total * 0.2)
### Sum of total columns
top = data_cleaned[:first_20]['Total'].sum()
bot = data_cleaned[first_20:]['Total'].sum()

###Plotting a pie char
plt.style.use('ggplot')
plt.figure(figsize=(35,15))
plt.pie([top, bot],labels=['Top 20','Rest of the world'], startangle=90, explode=[0.2,0], radius=1.1, textprops={'fontsize': 10}, autopct='%1.1f%%',shadow=True)

plt.title('Comparison of 20% major contribiutors of CO2 emission \n vs rest of the world')

plt.show()