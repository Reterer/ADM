%%writefile modules/engine.py
"""
Contains functions for training and testing a PyTorch model.
"""
from tqdm.auto import tqdm
import pandas as pd
from sklearn.metrics.pairwise import cosine_similarity

# Функция для нахождения топ n рекомендаций для заданного соискателя

def get_top_n_recommendations(seeker_id, n, data_useful=data_useful, seekers_df=seekers_df, vacancies_df=vacancies_df):
    features = list(data_useful.columns)[3:4] + list(data_useful.columns)[6:10] + list(data_useful.columns)[11:]
    approp_city = seekers_df[seekers_df.SeekerIdHashed == seeker_id].iloc[0].City
    print(approp_city)
    data_useful = data_useful[data_useful.City == approp_city]
    seeker_data = data_useful[data_useful['SeekerIdHashed'] == seeker_id]
    seeker_features = seeker_data[features].values
    vacancy_data = data_useful[data_useful['SeekerIdHashed'] != seeker_id]
    vacancy_features = vacancy_data[features].values
    similarity_scores = cosine_similarity(seeker_features, vacancy_features)
    top_n_indices = similarity_scores.argsort()[0][-n:]
    print(similarity_scores)
    top_n_recommendations = vacancy_data.iloc[top_n_indices]['VacancyIdHashed']
    return top_n_recommendations.tolist()