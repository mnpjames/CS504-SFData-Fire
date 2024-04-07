import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
working_path = "/Users/michelle/Data/CS504/Project/"

print(f'Read in dataset for 2018-2023')
# here read in the smaller dataset
subset_file = 'Data/FDCalls_2018_2023.csv'
full_subset_name = working_path + subset_file

# this gives a warning:
# <input>:1: DtypeWarning: Columns (19,20,25) have mixed types.
# #Specify dtype option on import or set low_memory=False.
table_df = pd.read_csv(full_subset_name)

print(f'Fix date formats from csv file')
table_df['Call Date'] = pd.to_datetime(table_df['Call Date'], format='%Y-%m-%d')
table_df['Watch Date'] = pd.to_datetime(table_df['Watch Date'], format='%m/%d/%Y')

# make a function for this format
table_df['Received DtTm'] = pd.to_datetime(table_df['Received DtTm'], format='%m/%d/%Y %I:%M:%S %p')
table_df['Entry DtTm'] = pd.to_datetime(table_df['Entry DtTm'], format='%m/%d/%Y %I:%M:%S %p')
table_df['Dispatch DtTm'] = pd.to_datetime(table_df['Dispatch DtTm'], format='%m/%d/%Y %I:%M:%S %p')
table_df['Response DtTm'] = pd.to_datetime(table_df['Response DtTm'], format='%m/%d/%Y %I:%M:%S %p')
table_df['On Scene DtTm'] = pd.to_datetime(table_df['On Scene DtTm'], format='%m/%d/%Y %I:%M:%S %p')
table_df['Transport DtTm'] = pd.to_datetime(table_df['Transport DtTm'], format='%m/%d/%Y %I:%M:%S %p')
table_df['Hospital DtTm'] = pd.to_datetime(table_df['Hospital DtTm'], format='%m/%d/%Y %I:%M:%S %p')
table_df['Available DtTm'] = pd.to_datetime(table_df['Available DtTm'], format='%m/%d/%Y %I:%M:%S %p')

# and plot call response times by month
# how will we calculate response time per unit?
# this_field='Entry DtTm'
# this_field='On Scene DtTm'

# check non-null count of date-time fields
print(f'Check null counts of date-time fields')
table_df['Call Date'].isnull().sum()
table_df['Watch Date'].isnull().sum()
table_df['Received DtTm'].isnull().sum()
table_df['Entry DtTm'].isnull().sum()
table_df['Dispatch DtTm'].isnull().sum()
table_df['Response DtTm'].isnull().sum()
table_df['On Scene DtTm'].isnull().sum()
table_df['Transport DtTm'].isnull().sum()
table_df['Hospital DtTm'].isnull().sum()
table_df['Available DtTm'].isnull().sum()

# pull off row where On Scene DtTm is Null
# The resulting shape is 375611, 37
print(f'Pull off null values')
null_filter = table_df['On Scene DtTm'].isnull()
null_df = pd.DataFrame(table_df[null_filter])
null_df.shape

null_file_path = working_path + 'Data/null_records.csv'
null_df.to_csv(null_file_path)


print(f'Plot the counts by time of the null values')
# plot the records with null OnSceneDtTm values to see whether they are concentrated
# call_year_sr = null_df['Call Year'].value_counts(sort=False, ascending=True)
# call_year_sr.sort_index(inplace=True)

null_df['Index Date'] = null_df['Call Date'].dt.year.map(str)+ '-' + null_df['Call Date'].dt.month.map(str)
null_df['Index Date'] = pd.to_datetime(null_df['Index Date'], format='%Y-%m').dt.strftime('%Y-%m')

null_df_sr = null_df['Index Date'].value_counts(sort=False, ascending=True)
null_df_sr.sort_index(inplace=True)

fig, ax = plt.subplots()
ax.plot(null_df_sr)
ax.set_title('Null Records by Month')
ax.set_xlabel('Month')
ax.set_ylabel('Record Count')
plt.xticks(rotation=90)
plt.tight_layout()
plt.savefig(working_path + 'Images/null_records_by_month.png')

# I should come back and plot the value counts of the null records
# against the value counts of the not-null records and show the
# trends are the same

# now get the dataset without any of the null values and
# plot the counts by month to determine where to do the
# cutoffs for the different models

table_df.dropna(axis='index', subset=['On Scene DtTm'], inplace=True)
table_df['Index Date'] = table_df['Call Date'].dt.year.map(str)+ '-' + table_df['Call Date'].dt.month.map(str)
table_df['Index Date'] = pd.to_datetime(table_df['Index Date'], format='%Y-%m').dt.strftime('%Y-%m')

table_df_sr = table_df['Index Date'].value_counts(sort=False, ascending=True)
table_df_sr.sort_index(inplace=True)

fig, ax = plt.subplots()
ax.plot(table_df_sr)
ax.set_title('Valid Records by Month')
ax.set_xlabel('Month')
ax.set_ylabel('Record Count')
plt.xticks(rotation=90)
plt.tight_layout()
plt.savefig(working_path + 'Images/valid_records_by_month.png')


ax.plot(null_df_sr)
plt.savefig(working_path + 'Images/both_records_by_month.png')

# calculate response time
table_df['Response Time'] = table_df['On Scene DtTm'] - table_df['Received DtTm']

# build three timestamp for comparison
# range 1 should be from 1/1/2018 to 3/16/2020
# range 2 should be from 3/17/2020 to 6/15/2021
# range 3 should be from 6/15/2021 to 12/31/2023
first_break_dtm = pd.to_datetime('2020-03-16', format='%Y-%m-%d')
second_break_dtm = pd.to_datetime('2021-06-15', format='%Y-%m-%d')

pre_lock_filter = (table_df['Call Date'] <= first_break_dtm)
in_lock_filter = ((table_df['Call Date'] > first_break_dtm) & (table_df['Call Date'] <= second_break_dtm))
post_lock_filter = (table_df['Call Date'] > second_break_dtm)

# make the tables
pre_lock_df = pd.DataFrame(table_df[pre_lock_filter])
# this one has 567361 records
in_lock_df = pd.DataFrame(table_df[in_lock_filter])
# this one has 280026 records
post_lock_df = pd.DataFrame(table_df[post_lock_filter])
# this one has 687645 records

# total records is 1535032
# all records accounted for

pre_lock_df.to_csv(working_path + 'Data/Pre_lock_2018_2023.csv')
in_lock_df.to_csv(working_path + 'Data/In_lock_2018_2023.csv')
post_lock_df.to_csv(working_path + 'Data/Post_lock_2018_2023.csv')
