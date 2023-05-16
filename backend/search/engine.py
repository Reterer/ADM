import data_setup
import gc
from sklearn.metrics.pairwise import cosine_similarity


# Функция для нахождения топ n рекомендаций для заданного соискателя
def get_top_n_recommendations(
    seeker_id,
    n,
    data_useful=data_setup.data_useful,
    seekers_df=data_setup.seekers_df,
):
    features = list(data_useful.columns)[3:4] + list(data_useful.columns)[6:-1]
    print("фичи")
    approp_city = seekers_df[seekers_df.SeekerIdHashed == seeker_id].iloc[0].City
    print("города")
    data_useful = data_useful[data_useful.City == approp_city]
    print("дата")
    seeker_data = data_useful[data_useful["SeekerIdHashed"] == seeker_id]
    print("просмотры")
    seeker_features = seeker_data[features].values
    print("просмотры фичи")
    vacancy_data = data_useful[data_useful["SeekerIdHashed"] != seeker_id]
    print("Вакансии дата")
    vacancy_features = vacancy_data[features].values
    print("До косинусов")
    similarity_scores = cosine_similarity(seeker_features, vacancy_features)
    print("После косинусов")
    top_n_indices = similarity_scores.argsort()[0][-n:]
    print("После обрезки")
    top_n_recommendations = vacancy_data.iloc[top_n_indices]["VacancyIdHashed"]
    print("Топ н рекомендаций")
    return top_n_recommendations.tolist()
