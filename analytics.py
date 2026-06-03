import pandas as pd
import plotly.express as px

def rating_chart(df):

    fig = px.histogram(
        df,
        x="vote_average",
        title="Movie Rating Distribution"
    )

    return fig


def popularity_chart(df):

    top = df.sort_values(
        by="popularity",
        ascending=False
    ).head(10)

    fig = px.bar(
        top,
        x="title",
        y="popularity",
        title="Top 10 Popular Movies"
    )

    return fig