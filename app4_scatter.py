"""
##############################################################################
#######                 PROJECT NAME : CO2 EMISSIONS                   #######
##############################################################################
                                Synopsis:
Script which create 6 scatter plots showing 6 countries (Poland, India, Japan, Sweden, Belgium, Germany) co2 emission vs population over years.
"""
### Import necessary libraries
import pandas as pd
import numpy as np
from pandas_schema import Column, Schema
from pandas_schema.validation import CustomElementValidation
import matplotlib.pyplot as plt

### Create two data frames from fossil-fuel-co2-emissions-by-nation_csv and population_csv files
data1 = pd.read_csv('fossil-fuel-co2-emissions-by-nation_csv.csv')
data2 = pd.read_csv('population_csv.csv')
### Create new column and apply capitalization to prepare for merging
data2['Country'] = data2['Country Name'].str.upper()
### Merge both data frames on matching values in columns Country and Year
data = data1.merge(data2, how='inner', on=['Country', 'Year'])
### Isolate 4 columns and sort it from maximum value of Total
data = data[['Country','Total','Value','Year']].sort_values('Total', ascending=False)

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
    Column('Country',null_validation),
    Column('Total',null_validation+int_validation),
    Column('Value',null_validation+int_validation),
    Column('Year',null_validation+int_validation)
])


### Validate with pandas_schema
errors = schema.validate(data)
errors_index_rows = [e.row for e in errors]


#### Isolate validated data from invalid
data_cleaned = data.drop(index=errors_index_rows)


## Export validated data and errors to csv file
pd.DataFrame({'Errors':errors}).to_csv('errors.csv')
data_cleaned.to_csv('cleaned_data.csv')

### Create groups for each country
data = data_cleaned.groupby(['Country'])
### Isolate 6 countries to plot results
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
fig, ax = plt.subplots(nrow, ncol, figsize=(35,15),constrained_layout=True, sharex=True)
plt.style.use('ggplot')

### First subplot
ax1=ax[0,0].scatter(poland['Year'], poland['Value'], c=poland['Total'], vmin=poland['Total'].min(), vmax=poland['Total'].max(), cmap='Greens', alpha=0.75, edgecolor='black', linewidth=1)
ax1_y = np.arange(poland['Value'].min(), poland['Value'].max(), step=1000000)
ax[0,0].set_title('Carbon emmision by population over the years in Poland')
ax[0,0].set_ylabel('Population in 10 millions')
ax[0,0].set_yticks(ax1_y)
fig.colorbar(ax1, ax=ax[0,0], label='Carbon Emission')
### Second subplot

ax2 = ax[0,1].scatter(india['Year'], india['Value'], c=india['Total'], cmap='Greens', vmin=india['Total'].min(), vmax=india['Total'].max(), alpha=0.75, edgecolor='black', linewidth=1)
ax2_y = np.arange(india['Value'].min(), india['Value'].max(), step=1000000)
ax[0,1].set_title('Carbon emmision by population over the years in India')
ax[0,1].set_ylabel('Population in 10 millions')
ax[0,1].set_yticks(ax2_y)
ax[0,1].set_yscale('log')
fig.colorbar(ax2, ax=ax[0,1], label='Carbon Emission')

### Third subplot
ax3 = ax[1,0].scatter(swe['Year'], swe['Value'], c=swe['Total'], cmap='Greens', vmin=swe['Total'].min(),vmax=swe['Total'].max(),alpha=0.75, edgecolor='black', linewidth=1)
ax3_y = np.arange(swe['Value'].min(), swe['Value'].max(), step=1000000)
ax[1,0].set_title('Carbon emmision by population over the years in Sweden')
ax[1,0].set_ylabel('Population in 10 millions')
ax[1,0].set_yticks(ax3_y)
fig.colorbar(ax3, ax=ax[1,0], label='Carbon Emission')
### Fourth subplot

ax4 = ax[1,1].scatter(jap['Year'], jap['Value'], c=jap['Total'], cmap='Greens',vmin=jap['Total'].min(),vmax=jap['Total'].max(), alpha=0.75, edgecolor='black', linewidth=1)
ax4_y = np.arange(jap['Value'].min(), jap['Value'].max(), step=1000000)
ax[1,1].set_title('Carbon emmision by population over the years in Japan')
ax[1,1].set_ylabel('Population in 10 millions')
ax[1,1].set_yticks(ax4_y)
ax[1,1].set_yscale('log')
fig.colorbar(ax4, ax=ax[1,1], label='Carbon Emission')

### Fifth subplot
ax5 = ax[2,0].scatter(ger['Year'], ger['Value'], c=ger['Total'], cmap='Greens',vmin=ger['Total'].min(),vmax=ger['Total'].max(), alpha=0.75, edgecolor='black', linewidth=1)
ax5_y = np.arange(ger['Value'].min(), ger['Value'].max(), step=1000000)
ax[2,0].set_title('Carbon emmision by population over the years in Germany')
ax[2,0].set_ylabel('Population in 10 millions')
ax[2,0].set_yticks(ax5_y)
fig.colorbar(ax5, ax=ax[2,0], label='Carbon Emission')

### Sixth subplot
ax6 = ax[2,1].scatter(bel['Year'], bel['Value'], c=bel['Total'], cmap='Greens',vmin=bel['Total'].min(), vmax=bel['Total'].max(), alpha=0.75, edgecolor='black', linewidth=1)
ax6_y = np.arange(bel['Value'].min(), bel['Value'].max(), step=1000000)
ax[2,1].set_title('Carbon emmision by population over the years in Belgium')
ax[2,1].set_ylabel('Population in 10 millions')
ax[2,1].set_yticks(ax6_y)
fig.colorbar(ax6, ax=ax[2,1], label='Carbon Emission')

plt.show()
