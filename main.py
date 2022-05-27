from sklearn.metrics.pairwise import cosine_similarity
from sklearn.feature_extraction.text import TfidfVectorizer
import pandas as pd
import json

f = open('./dataset/data_en.json', 'r', encoding='utf-8')
data = json.load(f)
# for i in df['modalHotspots']:
# print(i["title"])
f.close()

#df = pd.read_csv("./dataset/valsteam_products.csv", sep=';', low_memory=False)

#df = df[['title', 'description']]

df = pd.DataFrame.from_dict(data["modalHotspots"])
df = df[['title', 'description']]

tfidf = TfidfVectorizer(stop_words='english')
df['description'] = df['description'].fillna('')

tfidf_matrix = tfidf.fit_transform(df['description'])

cosine_sim = cosine_similarity(tfidf_matrix, tfidf_matrix)

df = df[~df['title'].isna()]

indices = pd.Series(df.index, index=df['title'])
indices = indices[~indices.index.duplicated(keep='last')]

target_movie_index = indices['BKR2']

similarity_scores = pd.DataFrame(
    cosine_sim[target_movie_index], columns=["score"])

movie_indices = similarity_scores.sort_values(
    "score", ascending=False)[0:11].index

print(df['title'].iloc[movie_indices])
