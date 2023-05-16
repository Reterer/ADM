%%writefile modules/data_setup.py
import os
import pandas as pd

# read data
def read_data():
    data = pd.read_csv('/content/drive/MyDrive/hack_mai_data/df_full.csv')
    seekers_df = pd.read_csv('/content/drive/MyDrive/hack_mai_data/subsample_seekers.csv')
    vacancies_df = pd.read_csv('/content/drive/MyDrive/hack_mai_data/subsample_vacancies.csv')
    return data, seekers_df, vacancies_df
