import pandas as pd
from sklearn.linear_model import LinearRegression
import sklearn.metrics


def show_mean_squared_error(y_actual, y_predicted):
    mse_metric = sklearn.metrics.mean_squared_error(y_actual, y_predicted)
    print('Mean Squared Error: ', mse_metric)
    metric_r_squared = sklearn.metrics.r2_score(y_actual, y_predicted)
    print('R-squared: ', metric_r_squared)
    return mse_metric, metric_r_squared


def fit_model_for_intercept_type(intercept_type, x_items, y_items):
    print(f'Fit Intercept is {intercept_type}')
    model = LinearRegression(fit_intercept=intercept_type)
    clf = model.fit(x_items, y_items)
    print('Coefficient: ', clf.coef_)
    print('Intercept: ', clf.intercept_)
    predictions = model.predict(x_items)
    model_mse, model_rsquared = show_mean_squared_error(y, predictions)
    return model_mse, model_rsquared


# read in three datasets
print(f'Read in three datasets for 2018-2023')
working_path = "/Users/michelle/Data/CS504/Project/"
pre_lock_df = pd.read_csv(working_path + 'Data/Pre_lock_2018_2023.csv')
in_lock_df = pd.read_csv(working_path + 'Data/In_lock_2018_2023.csv')
post_lock_df = pd.read_csv(working_path + 'Data/Post_lock_2018_2023.csv')

# What I want to use for regression
# Unit sequence in call dispatch (already numeric)
# Battalion: one hot encoded into 17 columns
# Unit Type: one hot encoded into 12 columns
# later: Add Received DtTm but needs to be turned into a numberic time of day
print(f'Set up relevant columns')
pre_lock_reg = pre_lock_df[['Unit sequence in call dispatch', 'Battalion', 'Unit Type', 'Response Time']].copy()
in_lock_reg = in_lock_df[['Unit sequence in call dispatch', 'Battalion', 'Unit Type', 'Response Time']].copy()
post_lock_reg = post_lock_df[['Unit sequence in call dispatch', 'Battalion', 'Unit Type', 'Response Time']].copy()

# one hot encoding for PRE
print(f'One hot encoding for pre')
one_hot_bat = pd.get_dummies(pre_lock_reg['Battalion'], prefix='Bat')
pre_lock_reg = pre_lock_reg.drop('Battalion', axis='columns')
pre_lock_reg = pre_lock_reg.join(one_hot_bat)

one_hot_unit = pd.get_dummies(pre_lock_reg['Unit Type'], prefix='Unit')
pre_lock_reg = pre_lock_reg.drop('Unit Type', axis='columns')
pre_lock_reg = pre_lock_reg.join(one_hot_unit)

# one hot encoding for IN
print(f'One hot encoding for in')
one_hot_bat = pd.get_dummies(in_lock_reg['Battalion'], prefix='Bat')
in_lock_reg = in_lock_reg.drop('Battalion', axis='columns')
in_lock_reg = in_lock_reg.join(one_hot_bat)

one_hot_unit = pd.get_dummies(in_lock_reg['Unit Type'], prefix='Unit')
in_lock_reg = in_lock_reg.drop('Unit Type', axis='columns')
in_lock_reg = in_lock_reg.join(one_hot_unit)

# one hot encoding for POST
print(f'One hot encoding for post')
one_hot_bat = pd.get_dummies(post_lock_reg['Battalion'], prefix='Bat')
post_lock_reg = post_lock_reg.drop('Battalion', axis='columns')
post_lock_reg = post_lock_reg.join(one_hot_bat)

one_hot_unit = pd.get_dummies(post_lock_reg['Unit Type'], prefix='Unit')
post_lock_reg = post_lock_reg.drop('Unit Type', axis='columns')
post_lock_reg = post_lock_reg.join(one_hot_unit)

# set up column lists
print(f'Set up column lists')
pre_column_list = pre_lock_reg.columns.to_list()
pre_column_list.remove('Response Time')
in_column_list = in_lock_reg.columns.to_list()
in_column_list.remove('Response Time')
post_column_list = post_lock_reg.columns.to_list()
post_column_list.remove('Response Time')

#column_list = ['Unit sequence in call dispatch', 'Bat_3E', 'Bat_AMB',
       #'Bat_B01', 'Bat_B02', 'Bat_B03', 'Bat_B04', 'Bat_B05', 'Bat_B06',
       #'Bat_B07', 'Bat_B08', 'Bat_B09', 'Bat_B10', 'Bat_B99', 'Unit_AIRPORT',
       #'Unit_CHIEF', 'Unit_ENGINE', 'Unit_INVESTIGATION', 'Unit_MEDIC',
       #'Unit_PRIVATE', 'Unit_RESCUE CAPTAIN', 'Unit_RESCUE SQUAD',
       #'Unit_SUPPORT', 'Unit_TRUCK']

# in future combine these two lines
# pre_lock_reg['Response Time'] = pd.to_timedelta(pre_lock_reg['Response Time'])
# pre_lock_reg['Response Time']  = pre_lock_reg['Response Time'] / pd.to_timedelta(1, unit='s')
print(f'Set up Response Time as a float from a timedelta')
pre_lock_reg['Response Time'] = pd.to_timedelta(pre_lock_reg['Response Time']) / pd.to_timedelta(1, unit='s')
in_lock_reg['Response Time'] = pd.to_timedelta(in_lock_reg['Response Time']) / pd.to_timedelta(1, unit='s')
post_lock_reg['Response Time'] = pd.to_timedelta(post_lock_reg['Response Time']) / pd.to_timedelta(1, unit='s')


results = []

print(f'Setting up models for pre-lock')
X = pre_lock_reg[pre_column_list]
y = pre_lock_reg['Response Time']

for fit_intercept in [True, False]:
    print(f'Fitting model with fit_intercept {fit_intercept}')
    mse, r2 = fit_model_for_intercept_type(fit_intercept, X, y)
    record = [len(pre_column_list), fit_intercept, mse, r2]
    results.append(record)

print(f'Setting up models for in-lock')
X = in_lock_reg[in_column_list]
y = in_lock_reg['Response Time']

for fit_intercept in [True, False]:
    print(f'Fitting model with fit_intercept {fit_intercept}')
    mse, r2 = fit_model_for_intercept_type(fit_intercept, X, y)
    record = [len(in_column_list), fit_intercept, mse, r2]
    results.append(record)

print(f'Setting up models for post-lock')
X = post_lock_reg[post_column_list]
y = post_lock_reg['Response Time']

for fit_intercept in [True, False]:
    print(f'Fitting model with fit_intercept {fit_intercept}')
    mse, r2 = fit_model_for_intercept_type(fit_intercept, X, y)
    record = [len(post_column_list), fit_intercept, mse, r2]
    results.append(record)

for line in results:
    print(line)
