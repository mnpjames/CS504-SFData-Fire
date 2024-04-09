import pandas as pd

# original file
original_file = 'Data/Fire_Department_Calls_for_Service_20240318.csv'
working_path = "/Users/michelle/Data/CS504/Project/"

full_file = working_path + original_file
table_df = pd.read_csv(full_file)

# check negative calls from later analysis before setting datetime format
# just to make sure we didn't screw up the timedelta with datetime problems
table_df.drop(columns=['Unit ID', 'Incident Number', 'Call Type', 'Call Date', 'Watch Date', 'Address', 'City',
       'Zipcode of Incident', 'Battalion', 'Station Area', 'Box',
       'Original Priority', 'Priority', 'Final Priority', 'ALS Unit',
       'Call Type Group', 'Number of Alarms', 'Unit Type',
       'Unit sequence in call dispatch', 'Fire Prevention District',
       'Supervisor District', 'Neighborhooods - Analysis Boundaries', 'RowID',
       'case_location', 'data_as_of', 'data_loaded_at'], inplace=True)
# this shows that in fact some of the records do have an On Scene DtTm earlier than
# the received time

my_filter = table_df['Call Number'] == 221871719
