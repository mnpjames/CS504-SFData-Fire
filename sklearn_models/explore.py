from datetime import datetime, date, time
import pandas as pd
working_path = "/Users/michelle/Data/CS504/Project/"

print(f'Read in dataset for 2018-2023')
# here read in the smaller dataset
subset_file = 'Data/FDCalls_2018_2023.csv'
full_subset_name = working_path + subset_file

# this gives a warning:
# <input>:1: DtypeWarning: Columns (19,20,25) have mixed types.
# #Specify dtype option on import or set low_memory=False.
table_df = pd.read_csv(full_subset_name)
row_count = len(table_df.index)
columns = table_df.columns
print(f'Dataframe has {row_count} rows and {len(columns)} columns')

# build output dataframe of information about the dataset
# what information do we want to store for each column
info_index = columns
info_columns = ['Non-Null', 'Null', 'DType', 'Unique']

info_df = pd.DataFrame(0, index=info_index, columns=info_columns)
for index in info_df.index:
    info_df.at[index, 'DType'] = table_df[index].dtypes
    info_df.at[index, 'Null'] = table_df[index].isna().sum()
    info_df.at[index, 'Non-Null'] = table_df[index].notna().sum()
    info_df.at[index, 'Unique'] = table_df[index].nunique()

    # this_head = table_df[index].head()
    # head returns a series and you can't drop it into an array slot
    # info_df.at[index, 'Head'] = this_head

info_file = working_path + 'Data/Attribute_Info.csv'
info_df.to_csv(info_file)

# convert date times
table_df['Call Date'] = pd.to_datetime(table_df['Call Date'], format='%Y-%m-%d')
table_df['Watch Date'] = pd.to_datetime(table_df['Watch Date'], format='%m/%d/%Y')
table_df['Received DtTm'] = pd.to_datetime(table_df['Received DtTm'], format='%m/%d/%Y %I:%M:%S %p')
table_df['Entry DtTm'] = pd.to_datetime(table_df['Entry DtTm'], format='%m/%d/%Y %I:%M:%S %p')
table_df['Dispatch DtTm'] = pd.to_datetime(table_df['Dispatch DtTm'], format='%m/%d/%Y %I:%M:%S %p')
table_df['Response DtTm'] = pd.to_datetime(table_df['Response DtTm'], format='%m/%d/%Y %I:%M:%S %p')
table_df['On Scene DtTm'] = pd.to_datetime(table_df['On Scene DtTm'], format='%m/%d/%Y %I:%M:%S %p')
table_df['Transport DtTm'] = pd.to_datetime(table_df['Transport DtTm'], format='%m/%d/%Y %I:%M:%S %p')
table_df['Hospital DtTm'] = pd.to_datetime(table_df['Hospital DtTm'], format='%m/%d/%Y %I:%M:%S %p')
table_df['Available DtTm'] = pd.to_datetime(table_df['Available DtTm'], format='%m/%d/%Y %I:%M:%S %p')

# calculate response time
table_df['Response Time'] = table_df['On Scene DtTm'] - table_df['Received DtTm']
table_df['Response Time'] = pd.to_timedelta(table_df['Response Time']) / pd.to_timedelta(1, unit='s')

# can do these as is
table_df['Response Time'].corr(table_df['Call Number'])  # 0.06
table_df['Response Time'].corr(table_df['Incident Number'])  # 0.06
table_df['Response Time'].corr(table_df['Unit sequence in call dispatch'])  # 0.36

# this one not practical
# table_df['Response Time'].corr(table_df['RowID'])

# create a new dataframe with just information about the ReceivedDtTm and Response Time

# to turn Response Time into a number, I subtracted two datetime columns and normalized them

# now I want to turn Received Time into a number
# I can pull off just the time (no date) and I want to turn this into a number of seconds since the day started
times_df = pd.DataFrame(table_df['Response Time'])
times_df['Received DtTm'] = table_df['Received DtTm']
times_df['Received Time'] = times_df['Received DtTm'].dt.time
times_df['Received Count'] = (times_df['Received DtTm'].dt.hour * 3600) + (times_df['Received DtTm'].dt.minute * 60) + (times_df['Received DtTm'].dt.second)
times_df['Response Time'].corr(times_df['Received Count']) # -0.02

# try one-hot-encoding the case_location variable

times_df['Time of Day'] = pd.to_timedelta(table_df['Received DtTm'], unit='s') / pd.to_timedelta(1, unit='s')

# drop other columns
times_df.drop(columns=['Received DtTm', 'Received Time', 'Received Count'], inplace=True)
one_hot_temp_df = pd.get_dummies(table_df['case_location'])
times_df = times_df.join(one_hot_temp_df)
for column_name in times_df.columns:
    if (column_name != 'Response Time'):
        print(f'Correlation with {column_name} is {times_df["Response Time"].corr(times_df[column_name])}')

# need to do one-hot-encoding
table_df['Response Time'].corr(table_df['City'])

table_df['Response Time'].corr(table_df['Fire Prevention District'])

# check correlation of response time to other columns if possible