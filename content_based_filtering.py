from sklearn.metrics.pairwise import cosine_similarity
from sklearn.feature_extraction.text import TfidfVectorizer
import pandas as pd
import json


def content_based_filtering(list, item):
    df = prepare_data_frame(list)
    tfidf_matrix = vectorize_matrix(df)
    cosine_sim = calculate_cosine_similarity(tfidf_matrix)
    indices = get_indices(df)
    movie_indices = calculate_similarities(item, indices, cosine_sim)
    return df['title'].iloc[movie_indices]


def prepare_data_frame(list):
    df = pd.DataFrame(list)
    df = df[['title', 'description']]
    return df


def vectorize_matrix(df):
    tfidf = TfidfVectorizer(stop_words='english')
    df['description'] = df['description'].fillna('')
    tfidf_matrix = tfidf.fit_transform(df['description'])
    return tfidf_matrix


def calculate_cosine_similarity(tfidf_matrix):
    cosine_sim = cosine_similarity(tfidf_matrix, tfidf_matrix)
    return cosine_sim


def get_indices(df):
    df = df[~df['title'].isna()]
    indices = pd.Series(df.index, index=df['title'])
    indices = indices[~indices.index.duplicated(keep='last')]
    return indices


def calculate_similarities(item, indices, cosine_sim):
    target_movie_index = indices[item]
    similarity_scores = pd.DataFrame(
        cosine_sim[target_movie_index], columns=["score"])
    movie_indices = similarity_scores.sort_values(
        "score", ascending=False)[0:11].index
    return movie_indices


#f = open('./dataset/data_en.json', 'r', encoding='utf-8')
#data = json.load(f)
# f.close()
#print(content_based_filtering(data["modalHotspots"], "SRV6"))
