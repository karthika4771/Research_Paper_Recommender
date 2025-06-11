import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import streamlit as st

# Load Data
@st.cache_data
def load_data():
    return pd.read_csv("papers.csv")

df = load_data()

# Preprocessing
tfidf = TfidfVectorizer(stop_words='english')
tfidf_matrix = tfidf.fit_transform(df['Title'])

cosine_sim = cosine_similarity(tfidf_matrix, tfidf_matrix)

# Recommendation Function
def recommend(title, df, cosine_sim):
    indices = pd.Series(df.index, index=df['Title']).drop_duplicates()
    idx = indices.get(title)
    if idx is None:
        return ["Title not found in database."]
    sim_scores = list(enumerate(cosine_sim[idx]))
    sim_scores = sorted(sim_scores, key=lambda x: x[1], reverse=True)[1:6]
    paper_indices = [i[0] for i in sim_scores]
    return df['Title'].iloc[paper_indices]

# Streamlit UI
st.title("🔍 Smart Research Paper Recommender")
st.write("Enter a research paper title to get similar papers.")

user_input = st.text_input("Enter Title:")

if user_input:
    recommendations = recommend(user_input, df, cosine_sim)
    st.write("### Recommended Papers:")
    for rec in recommendations:
        st.write("- " + rec)
