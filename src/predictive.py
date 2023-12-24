# Загружаем библиотеки
import numpy as np # работа с векторами
import matplotlib.pyplot as plt # рисовать графики
import pandas as pd # для работы с таблицами

def get_food_advice():
  data = pd.read_csv("food.csv", sep=';')
  data['Score'] = data['Score'].str.replace(',', '.').astype(float)
  data['Meat'] = data['Meat'].str.replace(',', '.').astype(float)
  data['Cereals'] = data['Cereals'].str.replace(',', '.').astype(float)
  #обозначим целевую переменную
  y = data.Expert
  X = data.drop(columns=["Expert"])
  from sklearn.model_selection import train_test_split
  X_train, X_test, y_train, y_test = train_test_split(X, y, test_size = 1/3, random_state = 8)
  from sklearn.linear_model import LogisticRegression
  ignore_columns = ["Name"]
  X_train_subset = X_train.drop(columns=ignore_columns)
  X_test_subset = X_test.drop(columns=ignore_columns)
  logC = LogisticRegression()
  logC.fit(X_train_subset,y_train)
  logC.score(X_train_subset, y_train), logC.score(X_test_subset, y_test)
  p = pd.DataFrame(logC.predict_proba(X_test_subset), columns=logC.classes_)
  names = pd.DataFrame(X_test['Name'].values)
  eat_result = pd.concat([names, p[1]], axis=1)
  eat_result_sorted = eat_result.sort_values(by=1, ascending=False)
  top_three_names = eat_result_sorted.head(3)[0]
  return top_three_names