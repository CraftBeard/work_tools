import pandas as pd
import numpy as np
import lightgbm as lgb
import datetime
from dateutil.relativedelta import relativedelta
from sklearn.metrics import mean_squared_error


'''
All functions
'''
def time_params(cnt=13):
    dt = datetime.datetime.now()
    print('Run datetime: {}'.format(dt.strftime('%Y-%m-%d %H:%M:%S')))

    params = {}
    for i in range(cnt):
        params['{}_day_ago'.format(i)] = dt - relativedelta(days=i)
        params['{}_mth_ago'.format(i)] = dt - relativedelta(months=i)
        params['{}_mth_ago_st'.format(i)] = (dt - relativedelta(months=i)).replace(day=1)
        params['{}_mth_ago_ed'.format(i)] = (dt - relativedelta(months=i-1)).replace(day=1) - relativedelta(days=1)
        params['{}_wk_ago'.format(i)] = dt - relativedelta(days=i*7)

    return params


'''
Main Procedure
'''
# get time parameters
time_params = time_params()

# construct datasets
col_x = []
col_y = []
lgb_train = lgb.Dataset(train[col_x], label=train[col_y])
lgb_test = lgb.Dataset(test[col_x], label=test[col_y], reference=lgb_train)

# set lightgbm parameters
params = {
    'task': 'train',
    'boosting_type': 'gbdt',  # 设置提升类型
    'objective': 'regression_l2', # 目标函数
    'metric': ['mape', 'rmse'],  # 评估函数
    'num_leaves': 31,   # 叶子节点数
    'learning_rate': 0.05,  # 学习速率
    'feature_fraction': 0.9, # 建树的特征选择比例
    'bagging_fraction': 0.8, # 建树的样本采样比例
    'bagging_freq': 5,  # k 意味着每 k 次迭代执行bagging
    'verbose': 1 # <0 显示致命的, =0 显示错误 (警告), >0 显示信息
}

# train model
print('Start training...')
gbm = lgb.train(params,lgb_train,num_boost_round=20,valid_sets=lgb_test,early_stopping_rounds=50)

# save model
#print('Save model...')
#gbm.save_model('model.txt')

# predict labels
print('Start predicting...')
y_pred = gbm.predict(test[col_x], num_iteration=gbm.best_iteration)

# validate model
print('The rmse of prediction is:', mean_squared_error(test[col_y], y_pred) ** 0.5)

'''
Parameter Tuning
'''
best_params = {}

# Tuning Accuracy
print('Tuning Accuracy')
for num_leaves in range(20,200,5):
    for max_depth in range(3,8,1):
        params['num_leaves'] = num_leaves
        params['max_depth'] = max_depth

        cv_results = lgb.cv(
                            params,
                            lgb_train,
                            seed=233,
                            nfold=5,
                            metrics=['mape', 'rmse'],
                            early_stopping_rounds=10,
                            verbose_eval=True
                            )

        mean_merror = pd.Series(cv_results['mape-mean']).min()
        boost_rounds = pd.Series(cv_results['mape-mean']).argmin()

        if mean_merror < min_merror:
            min_merror = mean_merror
            best_params['num_leaves'] = num_leaves
            best_params['max_depth'] = max_depth

params['num_leaves'] = best_params['num_leaves']
params['max_depth'] = best_params['max_depth']

# Tunning Overfitting
print('Tunning Overfitting')
for max_bin in range(1,255,5):
    for min_data_in_leaf in range(10,200,5):
            params['max_bin'] = max_bin
            params['min_data_in_leaf'] = min_data_in_leaf

            cv_results = lgb.cv(
                                params,
                                lgb_train,
                                seed=42,
                                nfold=3,
                                metrics=['binary_error'],
                                early_stopping_rounds=3,
                                verbose_eval=True
                                )

            mean_merror = pd.Series(cv_results['binary_error-mean']).min()
            boost_rounds = pd.Series(cv_results['binary_error-mean']).argmin()

            if mean_merror < min_merror:
                min_merror = mean_merror
                best_params['max_bin']= max_bin
                best_params['min_data_in_leaf'] = min_data_in_leaf

params['min_data_in_leaf'] = best_params['min_data_in_leaf']
params['max_bin'] = best_params['max_bin']

# Tunning Overfitting
print('Tunning Overfitting')
for feature_fraction in [0.0,0.1,0.2,0.3,0.4,0.5,0.6,0.7,0.8,0.9,1.0]:
    for bagging_fraction in [0.0,0.1,0.2,0.3,0.4,0.5,0.6,0.7,0.8,0.9,1.0]:
        for bagging_freq in range(0,50,5):
            params['feature_fraction'] = feature_fraction
            params['bagging_fraction'] = bagging_fraction
            params['bagging_freq'] = bagging_freq

            cv_results = lgb.cv(
                                params,
                                lgb_train,
                                seed=42,
                                nfold=3,
                                metrics=['binary_error'],
                                early_stopping_rounds=3,
                                verbose_eval=True
                                )

            mean_merror = pd.Series(cv_results['binary_error-mean']).min()
            boost_rounds = pd.Series(cv_results['binary_error-mean']).argmin()

            if mean_merror < min_merror:
                min_merror = mean_merror
                best_params['feature_fraction'] = feature_fraction
                best_params['bagging_fraction'] = bagging_fraction
                best_params['bagging_freq'] = bagging_freq

params['feature_fraction'] = best_params['feature_fraction']
params['bagging_fraction'] = best_params['bagging_fraction']
params['bagging_freq'] = best_params['bagging_freq']

# Tunning Overfitting
print('Tunning Overfitting')
for lambda_l1 in [0.0,0.1,0.2,0.3,0.4,0.5,0.6,0.7,0.8,0.9,1.0]:
    for lambda_l2 in [0.0,0.1,0.2,0.3,0.4,0.5,0.6,0.7,0.8,0.9,1.0]:
        for min_split_gain in [0.0,0.1,0.2,0.3,0.4,0.5,0.6,0.7,0.8,0.9,1.0]:
            params['lambda_l1'] = lambda_l1
            params['lambda_l2'] = lambda_l2
            params['min_split_gain'] = min_split_gain

            cv_results = lgb.cv(
                                params,
                                lgb_train,
                                seed=42,
                                nfold=3,
                                metrics=['binary_error'],
                                early_stopping_rounds=3,
                                verbose_eval=True
                                )

            mean_merror = pd.Series(cv_results['binary_error-mean']).min()
            boost_rounds = pd.Series(cv_results['binary_error-mean']).argmin()

            if mean_merror < min_merror:
                min_merror = mean_merror
                best_params['lambda_l1'] = lambda_l1
                best_params['lambda_l2'] = lambda_l2
                best_params['min_split_gain'] = min_split_gain

params['lambda_l1'] = best_params['lambda_l1']
params['lambda_l2'] = best_params['lambda_l2']
params['min_split_gain'] = best_params['min_split_gain']