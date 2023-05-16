# !pip install transformers
import util
import data_setup
import engine.py

import pandas as pd
import re
import torch
import tensorflow as tf
import tensorflow_hub as hub
from transformers import AutoTokenizer, AutoModel
import pandas as pd
from sklearn.metrics.pairwise import cosine_similarity

# read data
data, seekers_df, vacancies_df = data_setup.read_data()

# recommendations

# Подготовка данных для использования в алгоритме cosine distance
# for feature in features:
#     data_useful[feature] = pd.Categorical(data_useful[feature]).codes


while 1:
    # read seeker_id_hash and n_vacancies
    engine.relevant_vacancies = get_top_n_recommendations(seeker_id_hash, n_vacancies)
    vacancies_df.set_index("VacancyIdHashed").loc[relevant_vacancies].reset_index()
