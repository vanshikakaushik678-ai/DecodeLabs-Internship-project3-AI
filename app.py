import streamlit as st
import json

from analytics import (
    rating_chart,
    popularity_chart
)

from recommendation_engine import (
    recommend,
    movies
)


# -------------------------
# Favorites Functions
# -------------------------

def load_favorites():

    try:
        with open(
            "user_data/favorites.json",
            "r"
        ) as f:

            return json.load(f)

    except:
        return []


def save_favorites(data):

    with open(
        "user_data/favorites.json",
        "w"
    ) as f:

        json.dump(
            data,
            f,
            indent=4
        )


# -------------------------
# History Functions
# -------------------------

def load_history():

    try:
        with open(
            "user_data/history.json",
            "r"
        ) as f:

            return json.load(f)

    except:
        return []


def save_history(movie):

    history = load_history()

    history.append(movie)

    with open(
        "user_data/history.json",
        "w"
    ) as f:

        json.dump(
            history,
            f,
            indent=4
        )


# -------------------------
# Page Config
# -------------------------

st.set_page_config(
    page_title="AI Movie Recommendation Engine",
    layout="wide"
)

# -------------------------
# Sidebar
# -------------------------

page = st.sidebar.radio(
    "Navigation",
    [
        "Home",
        "Recommendations",
        "Favorites",
        "History",
        "Analytics"
    ]
)

# -------------------------
# Logo & Title
# -------------------------

st.image(
    "assets/logo.png",
    width=120
)

st.title(
    "🎬 Smart AI Movie Recommendation System"
)

# ==================================================
# HOME PAGE
# ==================================================

if page == "Home":

    st.header("🏠 Home")

    st.write(
        """
Welcome to the AI Movie Recommendation System.

Features:

✅ AI Recommendations

✅ Similarity Score

✅ Favorites

✅ History Tracking

✅ Analytics Dashboard
"""
    )

# ==================================================
# RECOMMENDATIONS PAGE
# ==================================================

elif page == "Recommendations":

    st.header("🎯 Movie Recommendations")

    minimum_rating = st.sidebar.slider(
        "Minimum Rating",
        0.0,
        10.0,
        5.0
    )

    movie = st.selectbox(
        "Choose a Movie",
        sorted(
            movies["title"].unique()
        )
    )

    if st.button(
        "Get Recommendations"
    ):

        save_history(movie)

        recommendations = recommend(
            movie
        )

        st.subheader(
            "Recommended Movies"
        )

        for item in recommendations:

            if item["rating"] >= minimum_rating:

                st.markdown(
                    f"""
### 🎥 {item['title']}

Similarity Score:
{item['similarity']}%

⭐ Rating:
{item['rating']}

🔥 Popularity:
{round(item['popularity'],2)}

---
"""
                )

                if st.button(
                    f"❤️ Favorite {item['title']}"
                ):

                    favs = load_favorites()

                    if item["title"] not in favs:

                        favs.append(
                            item["title"]
                        )

                        save_favorites(
                            favs
                        )

                        st.success(
                            "Added to Favorites"
                        )

# ==================================================
# FAVORITES PAGE
# ==================================================

elif page == "Favorites":

    st.header(
        "❤️ Favorite Movies"
    )

    favs = load_favorites()

    if len(favs) == 0:

        st.warning(
            "No Favorite Movies Yet"
        )

    else:

        for movie in favs:

            st.write(
                f"🎬 {movie}"
            )

# ==================================================
# HISTORY PAGE
# ==================================================

elif page == "History":

    st.header(
        "📜 Recommendation History"
    )

    history = load_history()

    if len(history) == 0:

        st.warning(
            "No History Found"
        )

    else:

        for movie in reversed(history):

            st.write(
                f"🎥 {movie}"
            )

# ==================================================
# ANALYTICS PAGE
# ==================================================

elif page == "Analytics":

    st.header(
        "📊 Analytics Dashboard"
    )

    st.plotly_chart(
        rating_chart(movies),
        use_container_width=True
    )

    st.plotly_chart(
        popularity_chart(movies),
        use_container_width=True
    )