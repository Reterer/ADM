import pandas as pd

data_dir = "data"

print("Загрузка данных")
data_useful = pd.read_pickle(f"{data_dir}/data_final_small.pkl")
# data_useful = data_useful.sample(int(data_useful.shape[0] * 0.3))
# data_useful.to_pickle(f"{data_dir}/data_final_small.pkl")
seekers_df = pd.read_csv(f"{data_dir}/subsample_seekers.csv")
vacancies_df = pd.read_csv(f"{data_dir}/subsample_vacancies.csv")
print("Загрузка данных завершена")
