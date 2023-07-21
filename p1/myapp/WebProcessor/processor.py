import numpy as np

from .primary_processing import primary_processing
from .next_processing import process
import pickle


def processing(url):
    df = primary_processing(url)
    df = process(df)

    with open("myapp/training/model.pickle", 'rb') as file:
        model = pickle.load(file)
    with open("myapp/training/scaler.pickle", 'rb') as file:
        sc = pickle.load(file)

    text = np.array(df['text'])
    x_test = df.drop(columns=['text'])
    x_test = sc.transform(x_test)
    y_pred = model.predict(x_test)

    n = len(y_pred)
    basic_information = []
    ignored_information = []
    deleted_information = []
    for i in range(n):
        if y_pred[i] == 1:
            basic_information.append(text[i])
        elif y_pred[i] == 0:
            ignored_information.append(text[i])
        else:
            deleted_information.append(text[i])
    basic = "\n".join(basic_information)
    ignored = "\n".join(ignored_information)
    deleted = "\n".join(deleted_information)

    return basic, ignored, deleted
