from p1.myapp.WebProcessor.next_processing import process
import pandas as pd

def concat_df(df_main, df_new):
    return pd.concat([df_main, df_new])

def create_dataset(names):
    start_df = process(pd.read_csv(names[0]))
    for name in names[1:]:
        df = process(pd.read_csv(name))
        start_df = concat_df(start_df, df)
    return start_df

train_names = [str(x)+'.csv' for x in [1, 2, 3, 4, 6, 7, 8, 9, 11, 12, 13, 14, 16, 17, 18, 19, 21, 22, 23, 24, 26, 27, 28, 29, 30, 31, 32, 33, 34, 35, 36, 37, 38, 39, 40, 41, 42, 43, 44, 45, 46, 47, 48, 49, 50]]
test_names = [str(x)+'.csv' for x in [5, 10, 15, 20, 25]]

train_df = create_dataset(train_names)
test_df = create_dataset(test_names)

str_file = "train_v1.csv"
train_df.to_csv(str_file, index=False)
str_file1 = "test_v1.csv"
test_df.to_csv(str_file1, index=False)