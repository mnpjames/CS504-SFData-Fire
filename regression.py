from datetime import datetime
import pandas as pd
from sklearn.linear_model import LinearRegression
import sklearn.metrics

# Unit sequence in call dispatch (already numeric)
# Battalion: one hot encoded into 17 columns
# Unit Type: one hot encoded into 12 columns
# later: Add Received DtTm but needs to be turned into a numeric time of day
columns_for_trial = ['Unit sequence in call dispatch', 'Battalion', 'Unit Type', 'Response Time']

def show_mean_squared_error(y_actual, y_predicted):
    mse_metric = sklearn.metrics.mean_squared_error(y_actual, y_predicted)
    status_string = f'Mean Squared Error: {mse_metric}\n'
    print(status_string)
    results.append(status_string)
    metric_r_squared = sklearn.metrics.r2_score(y_actual, y_predicted)
    status_string = f'R-sqared: {metric_r_squared}\n'
    print(status_string)
    results.append(status_string)


def fit_model_for_intercept_type(intercept_type, x_items, y_items):

    model = LinearRegression(fit_intercept=intercept_type)
    clf = model.fit(x_items, y_items)
    status_string = f'Coefficient: {clf.coef_}\n'
    print(status_string)
    results.append(status_string)
    status_string = f'Intercept: {clf.intercept_}\n'
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
status_string = f'\nSetting up trials for this column list: {columns_for_trial}\n'
print(status_string)
results.append(status_string)

# read in the columns we want from the three datasets
status_string = f'Read in three datasets for 2018-2023'
print(status_string)
results.append(status_string)

working_path = "/Users/michelle/Data/CS504/Project/"
set_prefixes = ['pre', 'in', 'post']
dfs = { }

for set_prefix in set_prefixes:
    stored_dataset_path = working_path + 'Data/' + set_prefix + '_lock_2018_2023.csv'
    status_string = f'Reading columns for {stored_dataset_path}\n'
    print(status_string)
    results.append(status_string)
    dfs[set_prefix] = pd.read_csv(stored_dataset_path, usecols=columns_for_trial)

# set up response time as a timedelta
for set_prefix in set_prefixes:
    status_string = f'Changing dependent variable timedelta to number of seconds for {set_prefix}\n'
    print(status_string)
    results.append(status_string)
    dfs[set_prefix]['Response Time'] = pd.to_timedelta(dfs[set_prefix]['Response Time']) / pd.to_timedelta(1, unit='s')
    status_string = f'Response Time stats for {set_prefix}\n'
    print(status_string)
    results.append(status_string)
    status_string = f'count, mean, std, min, 1Q, 2Q, 3Q, max\n'
    print(status_string)
    results.append(status_string)
    # status_string = " ".join(list(dfs[set_prefix]['Response Time'].describe()))
    status_string = ""
    describe_results = list(dfs[set_prefix]['Response Time'].describe())
    for item in describe_results:
        status_string += str(item) + ", "

    print(status_string)
    results.append(status_string)

# set up one hot encoding as necessary
for set_prefix in set_prefixes:
    for column in columns_for_trial:
        if column_processing[column] == 'one-hot-encoding':
            column_prefix = column[0:4]

            status_string = f'Setting up one-hot encoding for {column} in {set_prefix} with prefix {column_prefix}\n'
            print(status_string)
            results.append(status_string)

            one_hot_temp_df = pd.get_dummies(dfs[set_prefix][column], prefix=column_prefix)
            dfs[set_prefix].drop(column, axis='columns', inplace=True)
            dfs[set_prefix] = dfs[set_prefix].join(one_hot_temp_df)


for set_prefix in set_prefixes:
    status_string = f'Setting up variables for {set_prefix}\n'
    print(status_string)
    results.append(status_string)
    column_list = dfs[set_prefix].columns.to_list()
    column_list.remove('Response Time')
    X = dfs[set_prefix][column_list]
    # y is always Response Time
    y = dfs[set_prefix]['Response Time']

    for fit_intercept in [True, False]:
        if fit_intercept:
            status_string = f'Setting up regression for {set_prefix} with intercept fitting\n'
        else:
            status_string = f'Setting up regression for {set_prefix} without intercept fitting\n'
        print(status_string)
        results.append(status_string)
        fit_model_for_intercept_type(fit_intercept, X, y)

current_time = datetime.now().strftime("%m_%d_%H_%M_%S")
outfile = working_path + '/Data/latest_output_' + current_time + '.txt'
with open(outfile, mode='w') as outfile:
    for line in results:
        outfile.write(line)
