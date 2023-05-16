import pandas as pd

data_dir = "data"

print("Загрузка данных")
data_useful = pd.read_pickle(f"{data_dir}/data_final.pkl")
seekers_df = pd.read_csv(f"{data_dir}/subsample_seekers.csv")
print("Загрузка данных завершена")
