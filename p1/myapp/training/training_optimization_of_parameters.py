import pandas as pd
from catboost import CatBoostClassifier
from sklearn.ensemble import RandomForestClassifier
import xgboost as xgb
from sklearn.model_selection import cross_val_score
import optuna
from .constants import *


def objective_lgbm_CatBoost(trial):
    max_depth = trial.suggest_int('max_depth', 2, 9)
    learning_rate = trial.suggest_float('learning_rate', 0.01, 0.1)
    n_estimators = trial.suggest_int('n_estimators', 50, 300)
    score = cross_val_score(
        CatBoostClassifier(max_depth=max_depth, learning_rate=learning_rate, n_estimators=n_estimators),
        x_train, y_train, cv=10, n_jobs=-1).mean()
    print(score)
    return score


def objective_lgbm_RandomForest(trial):
    max_depth = trial.suggest_int('max_depth', 2, 13)
    n_estimators = trial.suggest_int('n_estimators', 50, 300)
    score = cross_val_score(RandomForestClassifier(max_depth=max_depth, n_estimators=n_estimators),
                            x_train, y_train, cv=10, n_jobs=-1).mean()
    print(score)
    return score


def objective_lgbm_XGBoost(trial):
    max_depth = trial.suggest_int('max_depth', 2, 13)
    learning_rate = trial.suggest_float('learning_rate', 0.01, 0.1)
    n_estimators = trial.suggest_int('n_estimators', 50, 300)
    score = cross_val_score(
        xgb.XGBClassifier(max_depth=max_depth, learning_rate=learning_rate, n_estimators=n_estimators),
        x_train, y_train, cv=10, n_jobs=-1).mean()
    print(score)
    return score


train_df = pd.read_csv('/dataset/train_v14.csv')
test_df = pd.read_csv('/dataset/test_v14.csv')
frames = [train_df, test_df]
df = pd.concat(frames)

print('CatBoost')
print('Структурные признаки')
x_train = df[structure_features]
y_train = df['label']
study = optuna.create_study(direction='maximize')
study.optimize(objective_lgbm_CatBoost(), n_trials=5)

print('Структурные и семантические признаки')
x_train = df.drop(columns=['label', 'text'])
y_train = df['label']
study = optuna.create_study(direction='maximize')
study.optimize(objective_lgbm_CatBoost(), n_trials=5)

print('RandomForest')
print('Структурные признаки')
x_train = df[structure_features]
y_train = df['label']
study = optuna.create_study(direction='maximize')
study.optimize(objective_lgbm_RandomForest(), n_trials=5)

print('Структурные и семантические признаки')
x_train = df.drop(columns=['label', 'text'])
y_train = df['label']
study = optuna.create_study(direction='maximize')
study.optimize(objective_lgbm_RandomForest(), n_trials=5)

print('XGBoost')
df['label'] = df['label'].apply(lambda t: 2 if t == -1 else t)
print('Структурные признаки')
x_train = df[structure_features]
y_train = df['label']
study = optuna.create_study(direction='maximize')
study.optimize(objective_lgbm_XGBoost(), n_trials=5)

print('Структурные и семантические признаки')
x_train = df.drop(columns=['label', 'text'])
y_train = df['label']
study = optuna.create_study(direction='maximize')
study.optimize(objective_lgbm_XGBoost(), n_trials=5)
