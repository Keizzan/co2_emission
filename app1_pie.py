"""
##############################################################################
#######                 PROJECT NAME : CO2 EMISSIONS                   #######
##############################################################################
                                Synopsis:
Script which plots pie chart showing top 10 countries with highest total co2 emission.
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

#### Isolate validated data from invalid
data_cleaned = data_1.drop(index=errors_index_rows).sort_values('Total', ascending=False)[:10]


## Export validated data and errors to csv file
pd.DataFrame({'Errors':errors}).to_csv('errors.csv')
data_cleaned.to_csv('cleaned_data.csv')

plt.pie(data_cleaned['Total'],labels=data_cleaned.index, radius=1, textprops={'fontsize': 10}, autopct='%1.1f%%')


plt.show()
