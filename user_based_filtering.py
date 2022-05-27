import math
import operator
import pandas as pd
import numpy as np
from sklearn.neighbors import NearestNeighbors

from sqlite import list_all


def user_based_fitering(conn, user):
    recommendations = []
    pt = prepare_matrix(conn)
    if pt.empty:
        return []
    else:
        items = get_list_of_items(pt)
        user_idx = pt.index.values.tolist().index(user)
        k = len(pt.index.values) - 1
        if k > 10:
            k = 10
        for i in range(0, len(items)):
            if(math.isnan(pt.values[user_idx][i])):
                pred = predict_rating_item(user_id=user_idx, ratings=pd.DataFrame(
                    pt.values), item_id=i, k=k)
                recommendations.append(
                    {"item": pt.columns.values[i], "prediction": pred})
    return sorted(recommendations, key=operator.itemgetter(
        "prediction"), reverse=True)


def prepare_matrix(conn):
    list = list_all(conn)
    df = pd.DataFrame(list)
    if(df.empty):
        return df
    pt = pd.pivot_table(data=df, values="rate", index="user",
                        columns="item")
    return pt


def get_list_of_items(pt):
    return pt.columns.values


def find_k_similar_users(user_id, ratings, metric='cosine', k=4):
    ratings = ratings.loc[:, ~ratings.iloc[user_id].isna()]
    ratings = ratings.fillna(0)
    model = NearestNeighbors(metric=metric, algorithm='brute')
    model.fit(ratings)

    distances, indices = model.kneighbors(
        ratings.iloc[user_id-1, :].values.reshape(1, -1), n_neighbors=k+1)
    similarities = 1-distances.flatten()

    return similarities, indices


def predict_rating_item(user_id, item_id, ratings, metric='cosine', k=4):
    prediction = 0
    similarities, indices = find_k_similar_users(user_id, ratings, metric, k)
    ratings = ratings.fillna(0)
    mean_rating = ratings.loc[user_id-1, :].mean()
    sum_wt = np.sum(similarities)-1
    product = 1
    wtd_sum = 0

    for i in range(0, len(indices.flatten())):
        if indices.flatten()[i] == user_id:
            continue
        else:
            ratings_diff = ratings.iloc[indices.flatten(
            )[i], item_id-1]-np.mean(ratings.iloc[indices.flatten()[i], :])
            product = ratings_diff * (similarities[i])
            wtd_sum = wtd_sum + product
    prediction = int(round(mean_rating + (wtd_sum/sum_wt)))
    return prediction
