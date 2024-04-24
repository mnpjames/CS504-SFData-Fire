import pandas as pd
working_path = "/Users/michelle/Data/CS504/Project/"

# original file
original_file = 'Data/Fire_Department_Calls_for_Service_20240318.csv'
output_file = 'Data/FDCalls_2018_2023.csv'

full_file = working_path + original_file
full_output = working_path + output_file

# this gives a warning:
# <input>:1: DtypeWarning: Columns (19,20,25) have mixed types.
# #Specify dtype option on import or set low_memory=False.
table_df = pd.read_csv(full_file)

print(f'Current table shape ', table_df.shape)

# convert Call Date to a datetime
table_df['Call Date'] = pd.to_datetime(table_df['Call Date'], format='%m/%d/%Y')
my_year_df = table_df['Call Date'].dt.year

my_filter = ((table_df['Call Date'].dt.year > 2017) & (table_df['Call Date'].dt.year < 2024))
recent_df = table_df[my_filter]
print(f'Recent table shape ', recent_df.shape)

recent_df.to_csv(full_output, index=False)

# check negative calls from later analysis before setting datetime format
# just to make sure we didn't screw up the timedelta with datetime problems
"""
table_df.drop(columns=['Unit ID', 'Incident Number', 'Call Type', 'Call Date', 'Watch Date', 'Address', 'City',
       'Zipcode of Incident', 'Battalion', 'Station Area', 'Box',
       'Original Priority', 'Priority', 'Final Priority', 'ALS Unit',
       'Call Type Group', 'Number of Alarms', 'Unit Type',
       'Unit sequence in call dispatch', 'Fire Prevention District',
       'Supervisor District', 'Neighborhooods - Analysis Boundaries', 'RowID',
       'case_location', 'data_as_of', 'data_loaded_at'], inplace=True)
"""
# this shows that in fact some of the records do have an On Scene DtTm earlier than
# the received time
# my_filter = table_df['Call Number'] == 221871719


