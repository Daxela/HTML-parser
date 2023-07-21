import pickle
from sklearn.preprocessing import StandardScaler
from catboost import CatBoostClassifier
from sklearn.metrics import accuracy_score
from sklearn.ensemble import RandomForestClassifier
import xgboost as xgb
from .constants import *
import pandas as pd

name_test = '/dataset/test_v14.csv'
test_df = pd.read_csv(name_test)
name_train = '/dataset/train_v14.csv'
train_df = pd.read_csv(name_train)

print('CatBoost. Структурные признаки')
x_train = train_df[structure_features]
y_train = train_df['label']
x_test = test_df[structure_features]
y_test = test_df['label']
sc = StandardScaler()
x_train = sc.fit_transform(x_train)
x_test = sc.transform(x_test)
model = CatBoostClassifier(learning_rate=0.031212905067033038, n_estimators=197, max_depth=4,
                           loss_function='MultiClass')
model.fit(x_train, y_train)
y_pred = model.predict(x_test)
y_pred[y_pred == -1] = 1
print(accuracy_score(y_test, y_pred))

print('CatBoost. Структурные и семантические признаки')
x_train = train_df.drop(columns=['label', 'text'])
y_train = train_df['label']
x_test = test_df.drop(columns=['label', 'text'])
y_test = test_df['label']
sc = StandardScaler()
x_train = sc.fit_transform(x_train)
x_test = sc.transform(x_test)
model = CatBoostClassifier(learning_rate=0.07784833581720688, n_estimators=231, max_depth=6,
                           loss_function='MultiClass')
model.fit(x_train, y_train)
y_pred = model.predict(x_test)
y_pred[y_pred == -1] = 1
print(accuracy_score(y_test, y_pred))

print('RandomForest. Структурные признаки')
x_train = train_df[structure_features]
y_train = train_df['label']
x_test = test_df[structure_features]
y_test = test_df['label']
sc = StandardScaler()
x_train = sc.fit_transform(x_train)
x_test = sc.transform(x_test)
model = RandomForestClassifier(max_depth=6, n_estimators=273)
model.fit(x_train, y_train)
y_pred = model.predict(x_test)
y_pred[y_pred == -1] = 1
print(accuracy_score(y_test, y_pred))

print('RandomForest. Структурные и семантические признаки')
x_train = train_df.drop(columns=['label', 'text'])
y_train = train_df['label']
x_test = test_df.drop(columns=['label', 'text'])
y_test = test_df['label']
sc = StandardScaler()
x_train = sc.fit_transform(x_train)
x_test = sc.transform(x_test)
model = RandomForestClassifier(max_depth=13, n_estimators=226)
model.fit(x_train, y_train)
y_pred = model.predict(x_test)
y_pred[y_pred == -1] = 1
print(accuracy_score(y_test, y_pred))

train_df['label'] = train_df['label'].apply(lambda t: 2 if t == -1 else t)
print('XGBoost. Структурные признаки')
x_train = train_df[structure_features]
y_train = train_df['label']
x_test = test_df[structure_features]
y_test = test_df['label']
sc = StandardScaler()
x_train = sc.fit_transform(x_train)
x_test = sc.transform(x_test)
model = xgb.XGBClassifier(objective='multi:softmax', learning_rate=0.08830793492862306, n_estimators=57, num_class=3,
                          max_depth=3)
model.fit(x_train, y_train)
y_pred = model.predict(x_test)
y_pred[y_pred == 2] = 1
print(accuracy_score(y_test, y_pred))

print('XGBoost. Структурные и семантические признаки')
x_train = train_df.drop(columns=['label', 'text'])
y_train = train_df['label']
x_test = test_df.drop(columns=['label', 'text'])
y_test = test_df['label']
sc = StandardScaler()
x_train = sc.fit_transform(x_train)
x_test = sc.transform(x_test)
model = xgb.XGBClassifier(objective='multi:softmax', learning_rate=0.07658355188008653, n_estimators=125, num_class=3,
                          max_depth=12)
model.fit(x_train, y_train)
y_pred = model.predict(x_test)
y_pred[y_pred == 2] = 1
print(accuracy_score(y_test, y_pred))

"""with open("scaler.pickle", 'wb') as file:
    pickle.dump(sc, file)
with open("model.pickle", 'wb') as file:
    pickle.dump(model, file)"""