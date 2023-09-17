import pandas as pd
import numpy as np



""" df = pd.read_csv('./data_files/nba_salaries_sophomore.csv')

df.rename(columns={'other_player_name': 'player_id'}, inplace=True)
df.rename(columns={'Guaranteed': 'guaranteed'}, inplace=True)
df.rename(columns={'Tm': 'team'}, inplace=True)
df.rename(columns={'Player': 'player'}, inplace=True)

#making the money columns correct format
df['salary_23_24'] = df['salary_23_24'].replace('[\$,]', '', regex=True).astype(float)
df['salary_24_25'] = df['salary_24_25'].replace('[\$,]', '', regex=True).astype(float)
df['guaranteed'] = df['guaranteed'].replace('[\$,]', '', regex=True).astype(float)


#putting stuff that in NaN to their garunteed amount
df['salary_23_24'].fillna(df['guaranteed'], inplace=True)

#sorting values in descending order
df.sort_values('salary_23_24', ascending=False, inplace=True)



df.sort_values('guaranteed', ascending=False, inplace = True)
df.drop_duplicates(subset='player_id', inplace = True)
df.sort_values('salary_23_24', ascending=False, inplace=True)


#calculating the outliers - we will use this calculation for now
Q1 = df['salary_23_24'].quantile(0.25)
Q3 = df['salary_23_24'].quantile(0.75)
IQR = Q3 - Q1

threshold = 1.5 * IQR

outliers = df[(df['salary_23_24'] < Q1 - threshold) | (df['salary_23_24'] > Q3 + threshold)]

num_of_rows_outliers = outliers.shape[0] #there are 53 outliers, 42 outliers in new data

print(outliers)

df = df[42:] #getting rid of the outliers


#transformiing the salary data to be more of a normal distribution
df['salary_23_24_log'] = np.log(df['salary_23_24'])
df['salary_24_25_log'] = np.log(df['salary_24_25'])

#data is still not normal according to shapiro tests
#so z-scores should be taken with a grain of s

from scipy.stats import zscore
df['salary_23_24_log_zscores'] = zscore(df['salary_23_24_log'])



raptor_df = pd.read_csv('./data_files/raptor_23.csv')

#cleaning the data a bit 
raptor_df = raptor_df[raptor_df['mp'] >= 1400]
raptors_columns_to_remove = ['poss', 'mp']
raptor_df = raptor_df.drop(raptors_columns_to_remove, axis=1)


darko_df = pd.read_csv('./data_files/darko_23.csv')

#df dimensions
print("df Number of rows:", df.shape[0])
print("df Number of columns:", df.shape[1])
print(df.head(40))


#raptor dimensions - 273 rows 
print("raptor Number of rows:", raptor_df.shape[0]) 
print("raptor Number of columns:", raptor_df.shape[1])


#printing th number of rows in darko - 508
print("darko Number of rows:", darko_df.shape[0])
print("darko Number of columns:", darko_df.shape[1])


darko_df = darko_df.rename(columns={'Player': 'player'})


#joining the raptor and salary datasets
salary_raptor = pd.merge(df, raptor_df, on='player_id', how='inner')

#175 rows
print("salaries and raptor Number of rows:", salary_raptor.shape[0])
print("salaries and raptor Number of columns:", salary_raptor.shape[1])

salary_raptor = salary_raptor.drop('player_name', axis=1)

from unidecode import unidecode
salary_raptor['player'] = salary_raptor['player'].apply(lambda x: unidecode(x))
salaries_raptor_darko = pd.merge(salary_raptor, darko_df, on='player', how='inner')

#printing th number of rows in final 
print("final Number of rows:", salaries_raptor_darko.shape[0]) #176 final number of rows 
print("final Number of columns:", salaries_raptor_darko.shape[1])


print(salary_raptor.head(30))
print(salaries_raptor_darko.head(30))


#need to add import pickle

import pickle
with open('salaries_raptor_darko.pickle', 'wb') as file:
    pickle.dump(salaries_raptor_darko, file)
 """

import pickle
with open('salaries_raptor_darko.pickle', 'rb') as file:
    salaries_raptor_darko = pickle.load(file) 



salary_stats = salaries_raptor_darko['salary_23_24'].describe()
print(salary_stats)

raptor_stats = salaries_raptor_darko['raptor_total'].describe()
print(raptor_stats)

darko_stats = salaries_raptor_darko['DPM'].describe()
print(darko_stats)


#making them z scores and then standardizing them 
from scipy.stats import zscore
salaries_raptor_darko['raptor_zscore'] = zscore(salaries_raptor_darko['raptor_total'])
salaries_raptor_darko['darko_zscore'] = zscore(salaries_raptor_darko['DPM'])

raptor_std_dev = salaries_raptor_darko['raptor_zscore'].std() 
darko_std_dev = salaries_raptor_darko['darko_zscore'].std()


salaries_raptor_darko['raptor_zscore_standardized'] = salaries_raptor_darko['raptor_zscore'] * raptor_std_dev
salaries_raptor_darko['darko_zscore_standardized'] = salaries_raptor_darko['darko_zscore'] * darko_std_dev


raptor_stats = salaries_raptor_darko['raptor_zscore_standardized'].describe()
print(raptor_stats)

darko_stats = salaries_raptor_darko['darko_zscore_standardized'].describe()
print(darko_stats)


#getting the combined statistic
salaries_raptor_darko['raptor_plus_darko'] = salaries_raptor_darko['raptor_zscore_standardized'] + salaries_raptor_darko['darko_zscore_standardized']


combined_stats = salaries_raptor_darko['raptor_plus_darko'].describe()
print(combined_stats)

salaries_raptor_darko.sort_values('raptor_plus_darko', ascending=False, inplace=True)

salaries_raptor_darko['salary_23_24_log_zscores'] = zscore(salaries_raptor_darko['salary_23_24_log'])

combined_stats = salaries_raptor_darko['salary_23_24_log_zscores'].describe()
print(combined_stats)

salaries_raptor_darko['salary_23_24_log_zscores_transformed'] = (2.1 - salaries_raptor_darko['salary_23_24_log_zscores']) * 1.88

salaries_raptor_darko['raptor_plus_darko_transformed'] = salaries_raptor_darko['raptor_plus_darko'] + 5.5




salaries_raptor_darko['DARYL_SCORE'] = salaries_raptor_darko['salary_23_24_log_zscores_transformed'] * salaries_raptor_darko['raptor_plus_darko_transformed']

salaries_raptor_darko.sort_values('DARYL_SCORE', ascending=False, inplace=True)

#making the dataset ready for statmuse
salaries_raptor_darko['statmuse_player_names'] = salaries_raptor_darko['player'].str.lower(); 

salaries_raptor_darko['statmuse_player_names'] = salaries_raptor_darko['statmuse_player_names'].str.replace(" ", "-")

print(salaries_raptor_darko.head(50))



with open('ready_for_statmuse.pickle', 'wb') as file:
    pickle.dump(salaries_raptor_darko, file)


""" #visualizing the distribution of the salaries 
import matplotlib.pyplot as plt

#making a plot for the values to experiment with it
plt.hist(salaries_raptor_darko['CAT_SCORE'], bins = 20)

# Set labels and title
plt.xlabel('Values')
plt.ylabel('Frequency')
plt.title('Histogram of Values')

# Display the plot
plt.show() 
 """

