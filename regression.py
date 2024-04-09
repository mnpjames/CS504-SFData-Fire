from datetime import datetime
import pandas as pd
from sklearn.linear_model import LinearRegression
import sklearn.metrics

# Unit sequence in call dispatch (already numeric)
# Battalion: one hot encoded into 17 columns
# Unit Type: one hot encoded into 12 columns
# later: Add Received DtTm but needs to be turned into a numeric time of day
columns_for_trial = ['Unit sequence in call dispatch', 'Battalion', 'Unit Type', 'Response Time']
drop_negative_response_times = False  # need to code this

def show_mean_squared_error(y_actual, y_predicted):
    mse_metric = sklearn.metrics.mean_squared_error(y_actual, y_predicted)
    status_string = f'Mean Squared Error: {mse_metric}'
    print(status_string)
    results.append(status_string)
    metric_r_squared = sklearn.metrics.r2_score(y_actual, y_predicted)
    status_string = f'R-sqared: {metric_r_squared}'
    print(status_string)
    results.append(status_string)


def fit_model_for_intercept_type(intercept_type, x_items, y_items):

    model = LinearRegression(fit_intercept=intercept_type)
    clf = model.fit(x_items, y_items)
    status_string = f'Coefficient: {clf.coef_}'
    print(status_string)
    results.append(status_string)
    status_string = f'Intercept: {clf.intercept_}'
    print(status_string)
    results.append(status_string)

    predictions = model.predict(x_items)
    show_mean_squared_error(y, predictions)

column_processing = {
    'Unit sequence in call dispatch': None,
    'Battalion': 'one-hot-encoding',
    'Unit Type': 'one-hot-encoding',
    'Response Time': None
}
# set the columns we are using for this trial

results = []
status_string = f'\nSetting up trials for this column list: {columns_for_trial}'
print(status_string)
results.append(status_string)

# read in the columns we want from the three datasets
print(f'Read in three datasets for 2018-2023')
working_path = "/Users/michelle/Data/CS504/Project/"
set_prefixes = ['pre', 'in', 'post']
dfs = { }

for set_prefix in set_prefixes:
    stored_dataset_path = working_path + 'Data/' + set_prefix + '_lock_2018_2023.csv'
    status_string = f'Reading columns for {stored_dataset_path}'
    print(status_string)
    results.append(status_string)
    dfs[set_prefix] = pd.read_csv(stored_dataset_path, usecols=columns_for_trial)

for set_prefix in set_prefixes:
    # one hot encoding for PRE

    for column in columns_for_trial:
        if column_processing[column] == 'one-hot-encoding':
            column_prefix = column[0:4]

            status_string = f'Setting up one-hot encoding for {column} in {set_prefix} with prefix {column_prefix}'
            print(status_string)
            results.append(status_string)

            one_hot_temp_df = pd.get_dummies(dfs[set_prefix][column], prefix=column_prefix)
            dfs[set_prefix].drop(column, axis='columns', inplace=True)
            dfs[set_prefix] = dfs[set_prefix].join(one_hot_temp_df)

# set up response time as a timedelta
# and drop original column that is no longer needed
for set_prefix in set_prefixes:
    status_string = f'Changing dependent variable timedelta to number of seconds for {set_prefix}'
    print(status_string)
    results.append(status_string)
    dfs[set_prefix]['Response Time'] = pd.to_timedelta(dfs[set_prefix]['Response Time']) / pd.to_timedelta(1, unit='s')

# There seem to be 74 records with a negative response time, which seems weird.
# my_filter = dfs['pre']['Response Unit'] < 0
# negatives = dfs['pre'][my_filter]
# Handle here by dropping them if true
if not drop_negative_response_times:
    status_string = f'Keeping negative response times'
else:
    status_string = f'Need to code the dropping of negative response times'
print(status_string)
results.append(status_string)

for set_prefix in set_prefixes:
    status_string = f'Setting up variables for {set_prefix}'
    print(status_string)
    results.append(status_string)
    column_list = dfs[set_prefix].columns.to_list()
    column_list.remove('Response Time')
    X = dfs[set_prefix][column_list]
    # y is always Response Time
    y = dfs[set_prefix]['Response Time']

    for fit_intercept in [True, False]:
        if fit_intercept:
            status_string = f'Setting up regression for {set_prefix} with intercept fitting'
        else:
            status_string = f'Setting up regression for {set_prefix} without intercept fitting'
        print(status_string)
        results.append(status_string)
        fit_model_for_intercept_type(fit_intercept, X, y)

current_time = datetime.now().strftime("%m_%d_%H_%M_%S")
outfile = working_path + '/Data/latest_output_' + current_time + '.txt'
with open(outfile, mode='w') as outfile:
    for line in results:
        outfile.write(line)
