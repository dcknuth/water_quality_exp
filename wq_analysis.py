import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
#aq = pd.read_csv('daily_88101_2022.csv')
wq = pd.read_csv('Cowels_fecal_coliform.csv')

# There is some general water saftey info here
#  https://www.waterboards.ca.gov/water_issues/programs/swamp/docs/cwt/guidance/340.pdf
# It also contains the state and federal act names that mandate the data
#  collection

# See what we have
for col in wq.columns:
    print(col)
wq.head()
wq['SampleDate'].head()

# Quick output similar to the website
# Need to convert to dates
wq['Date'] = pd.to_datetime(wq.loc[:,'SampleDate'], format='%Y-%m-%d')
# Need to drop the dates that were improperly formated
cutoff_date = pd.to_datetime('2017-01-01')
wq.drop(wq[wq['Date'] < cutoff_date].index, inplace=True)
plt.ioff()
sns.set_theme(style='whitegrid')
sns.relplot(x=wq['Date'], y=wq['CalculatedResult'], label='Fecal Coliform')
plt.show()
# There's a 10x outlier. Also need to know what level is unsafe
# Central Valley Water Board E. Coli monitoring says that
# <100 MPN/100 mL is good and >320 is bad for e. coli
# EPA level for swimming says <200 colonies/100mL
# Let's redraw with some more information
g = sns.relplot(x=wq['Date'], y=wq['CalculatedResult'], label='Fecal Coliform')
#g.set(yscale='symlog') # not log or zeros will not show
g.set(yscale='log') # we don't seem to have any zeros
plt.axhline(y=200, color='g', label='OK to swim below this')
plt.legend()
plt.show()

# What's the lowest measured value
wq['CalculatedResult'].min()
# 2 it seems

wq['Program'].unique()
# There seem to be two collections of the same measure? Need a web search to
#  see what this means. Can't find anything. Does it make a difference?
df = wq[['Date', 'CalculatedResult', 'Program']]
g = sns.relplot(data=df, x='Date', y="CalculatedResult",
               hue="Program")
g.set(yscale='log')
plt.show()

# Is there a seasonal trend. Let's just plot 2022
start_date = pd.to_datetime('2022-01-01')
end_date = pd.to_datetime('2023-01-01')
df = wq.loc[(wq['Date'] >= start_date) & (wq['Date'] < end_date)]
g = sns.relplot(x=df['Date'], y=df['CalculatedResult'],
                label='Fecal Coliform')
g.set(yscale='log')
plt.legend()
plt.title("2022")
plt.show()
# 2021
start_date = pd.to_datetime('2021-01-01')
end_date = pd.to_datetime('2022-01-01')
df = wq.loc[(wq['Date'] >= start_date) & (wq['Date'] < end_date)]
g = sns.relplot(x=df['Date'], y=df['CalculatedResult'],
                label='Fecal Coliform')
g.set(yscale='log')
plt.legend()
plt.title("2021")
plt.show()

# What about e. coli?
wqe = pd.read_csv('Cowels_enterococcus.csv')
wqe['Date'] = pd.to_datetime(wqe.loc[:,'SampleDate'], format='%Y-%m-%d')
cutoff_date = pd.to_datetime('2017-01-01')
wqe.drop(wqe[wqe['Date'] < cutoff_date].index, inplace=True)
start_date = pd.to_datetime('2022-01-01')
end_date = pd.to_datetime('2023-01-01')
df = wqe.loc[(wqe['Date'] >= start_date) & (wqe['Date'] < end_date)]
g = sns.relplot(x=df['Date'], y=df['CalculatedResult'],
                label='E. Coli')
g.set(yscale='log')
plt.legend()
plt.title("2022")
plt.show()

# merge with fecal and show both in the same plot
wqb = pd.concat([wq, wqe])
df = wqb.loc[(wqb['Date'] >= start_date) & (wqb['Date'] < end_date)]
g = sns.relplot(data=df, x='Date', y="CalculatedResult",
               hue="Analyte")
g.set(yscale='log')
plt.xticks(rotation=45, ha='right')
plt.show()

# See if we can cooralate with rainfall
# Got rain data from another script, bring in here
with open('santa_cruz_rain_2022.csv') as f:
    ls = f.read().strip().split('\n')
rain = dict()
for l in ls[1:]:
    d, mmm = l.split(',')
    rain[d] = int(mmm)
df = wq.loc[(wq['Date'] >= start_date) & (wq['Date'] < end_date)]
# Need to add rain levels
def rain_amount(d):
    if rain[d] < 5:
        return('No Rain')
    elif rain[d] < 30:
        return('Light Rain')
    else:
        return('Rain')

df['Rain'] = df['SampleDate'].apply(rain_amount)
g = sns.relplot(data=df, x='Date', y="CalculatedResult", hue="Rain")
g.set(yscale='log')
plt.xticks(rotation=45, ha='right')
plt.show()

# Maybe we should plot all the rain data?
rain_df = pd.DataFrame(rain.items(), columns=['Day', 'Amount 0.1mm'])
rain_df['Date'] = pd.to_datetime(rain_df.loc[:,'Day'], format='%Y-%m-%d')
# Create a FacetGrid object
g = sns.relplot(x='Date', y='CalculatedResult', data=df, height=5, aspect=2,
                label='Fecal Coliform')
g.set(yscale='log')
# Plot the second column on a second y-axis
g.map(sns.scatterplot, data=rain_df, x='Date', y='Amount 0.1mm', color='red',
      label='Rainfall in tenths of a mm')
plt.legend()
plt.show()