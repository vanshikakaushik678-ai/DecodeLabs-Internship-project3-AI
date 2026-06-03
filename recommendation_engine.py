import pandas as pd
import ast

from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity


movies = pd.read_csv("data/tmdb_5000_movies.csv")


def convert(obj):
    genres = []

    try:
        obj = ast.literal_eval(obj)

        for item in obj:
            genres.append(item["name"])

    except:
        pass

    return " ".join(genres)


movies["genres"] = movies["genres"].apply(convert)

movies["keywords"] = movies["keywords"].apply(convert)

movies["overview"] = movies["overview"].fillna("")

movies["tags"] = (
    movies["overview"]
    + " "
    + movies["genres"]
    + " "
    + movies["keywords"]
)

movies = movies[
    [
        "title",
        "tags",
        "vote_average",
        "popularity"
    ]
]

tfidf = TfidfVectorizer(stop_words="english")

vectors = tfidf.fit_transform(
    movies["tags"]
)

similarity = cosine_similarity(vectors)


def recommend(movie_name):

    movie_name = movie_name.strip()

    if movie_name not in movies["title"].values:
        return []

    idx = movies[
        movies["title"] == movie_name
    ].index[0]

    distances = list(
        enumerate(similarity[idx])
    )

    distances = sorted(
        distances,
        reverse=True,
        key=lambda x: x[1]
    )

    recommendations = []

    for i in distances[1:11]:

        recommendations.append(
            {
                "title":
                movies.iloc[i[0]].title,

                "similarity":
                round(i[1] * 100, 2),

                "rating":
                movies.iloc[i[0]].vote_average,

                "popularity":
                movies.iloc[i[0]].popularity
            }
        )

    return recommendations