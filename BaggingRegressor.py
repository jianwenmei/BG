# 时间：2024年6月6日  Date： June 6, 2024
# 文件名称 Filename： BaggingRegressor.py
# 编码实现 Coding by：Xu QiPing, Jian Wenmei  
# 所属单位：中国 成都，西南民族大学（Southwest University of Nationality，or Southwest Minzu University）, 计算机科学与工程学院.
# 指导老师：周伟老师

# coding=utf-8
# 训练模型并预测测试集中数据，计算测试集与真实之间的误差

import pandas as pd
import numpy as np
from sklearn.ensemble import BaggingRegressor
from sklearn.tree import DecisionTreeRegressor
from sklearn.metrics import mean_squared_error

# 加载数据集
train_dataSet = pd.read_csv('modified_数据集Time_Series448_detail.dat')
test_dataSet = pd.read_csv('modified_数据集Time_Series660_detail.dat')

# columns表示原始列，noise_columns表示添加噪声的列
columns = ['T_SONIC', 'CO2_density', 'CO2_density_fast_tmpr', 'H2O_density', 'H2O_sig_strgth', 'CO2_sig_strgth', 'RECORD']
noise_columns = ['Error_T_SONIC', 'Error_CO2_density', 'Error_CO2_density_fast_tmpr', 'Error_H2O_density', 'Error_H2O_sig_strgth', 'Error_CO2_sig_strgth', 'Error_RECORD']

# 划分训练集中X_Train和y_Train
X_train = train_dataSet[noise_columns]
y_train = train_dataSet[columns]

# 定义训练模型（修改部分）
models = {}
for column in columns:
    model = BaggingRegressor(base_estimator=DecisionTreeRegressor())
    model.fit(X_train, y_train[column])  # 为每个目标变量训练一个模型
    models[column] = model

# 划分测试集中X_test和y_test
X_test = test_dataSet[noise_columns]
y_test = test_dataSet[columns]

# 预测值
y_predict = pd.DataFrame()
for column in columns:
    y_predict[column] = models[column].predict(X_test)

results = []
# 遍历y_test和y_predict，并且计算误差
for true_values, predicted_values in zip(y_test.values, y_predict.values):
    error = np.abs(true_values - predicted_values)

    # 格式化True_Value和Predicted_Value为原始数据格式
    formatted_true_value = ' '.join(map(str, true_values))
    formatted_predicted_value = ' '.join(map(str, predicted_values))
    formatted_error = ' '.join(map(str, error))  # 修改ERROR数据格式
    results.append([formatted_true_value, formatted_predicted_value, formatted_error]) # 保存结果

# 结果写入CSV文件当中
result_df = pd.DataFrame(results, columns=['True_Value', 'Predicted_Value', 'Error'])
result_df.to_csv("result-BaggingRegressor.csv", index=False)
