import os
import pickle
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity


class AnimeRecommender:
    """
    Anime Recommender Engine powered by TF-IDF genre similarity.
    Loads pre-computed objects from anime_recommender.pkl.
    """

    def __init__(self, pkl_path="anime_recommender.pkl", dataset_path="anime_dataset_1.xls"):
        self.pkl_path = pkl_path
        self.dataset_path = dataset_path
        self.df = None
        self.tfidf = None
        self.tfidf_matrix = None
        self.similarity_matrix = None
        self.indices = None

        self._load_model()

    def _load_model(self):
        """Loads model data from pickle file, or trains from dataset if missing."""
        if os.path.exists(self.pkl_path):
            try:
                with open(self.pkl_path, "rb") as f:
                    data = pickle.load(f)
                self.df = data["df"]
                self.tfidf = data["tfidf"]
                self.tfidf_matrix = data["tfidf_matrix"]
                self.similarity_matrix = data["similarity_matrix"]
                self.indices = data["indices"]
                print(f"Successfully loaded model from '{self.pkl_path}' ({len(self.df)} anime records).")
                return
            except Exception as e:
                print(f"Failed to load pickle file: {e}. Rebuilding model...")

        self.rebuild_model()

    def rebuild_model(self):
        """Rebuilds TF-IDF vectorizer and cosine similarity matrix from raw dataset."""
        if not os.path.exists(self.dataset_path):
            raise FileNotFoundError(f"Neither '{self.pkl_path}' nor '{self.dataset_path}' was found.")

        print(f"Loading dataset from '{self.dataset_path}'...")
        df = pd.read_csv(self.dataset_path)
        df["genres_clean"] = df["genres"].fillna("").str.replace("|", " ", regex=False)

        tfidf = TfidfVectorizer()
        tfidf_matrix = tfidf.fit_transform(df["genres_clean"])
        similarity_matrix = cosine_similarity(tfidf_matrix)
        indices = pd.Series(df.index, index=df["anime_title"]).drop_duplicates()

        self.df = df
        self.tfidf = tfidf
        self.tfidf_matrix = tfidf_matrix
        self.similarity_matrix = similarity_matrix
        self.indices = indices

        model_data = {
            "df": self.df,
            "tfidf": self.tfidf,
            "tfidf_matrix": self.tfidf_matrix,
            "similarity_matrix": self.similarity_matrix,
            "indices": self.indices
        }

        with open(self.pkl_path, "wb") as f:
            pickle.dump(model_data, f)
        print(f"Model rebuilt and saved to '{self.pkl_path}'.")

    def get_all_titles(self, query=""):
        """Returns list of anime titles matching optional search query."""
        if self.df is None:
            return []
        titles = self.df["anime_title"].dropna().unique().tolist()
        if query:
            q_lower = query.lower()
            return [t for t in titles if q_lower in t.lower()]
        return titles

    def get_anime_details(self, title):
        """Returns metadata dictionary for a specific anime title."""
        if title not in self.indices:
            return None

        idx = self.indices[title]
        if isinstance(idx, pd.Series):
            idx = idx.iloc[0]

        row = self.df.iloc[idx]
        return {
            "anime_id": int(row["anime_id"]),
            "anime_title": str(row["anime_title"]),
            "genres": str(row["genres"]),
            "type": str(row["type"]),
            "episodes": int(row["episodes"]),
            "rating": float(row["rating"]),
            "year_of_release": int(row["year_of_release"])
        }

    def recommend(self, title, top_n=10):
        """
        Generates top N recommendations for a given anime title based on genre similarity.
        Returns a list of dicts with anime info and similarity percentage score.
        """
        if title not in self.indices:
            return None

        idx = self.indices[title]
        if isinstance(idx, pd.Series):
            idx = idx.iloc[0]

        similarity_scores = list(enumerate(self.similarity_matrix[idx]))
        similarity_scores = sorted(similarity_scores, key=lambda x: x[1], reverse=True)

        # Exclude the anime itself (index 0)
        similarity_scores = similarity_scores[1:top_n + 1]

        results = []
        for rank, (i, score) in enumerate(similarity_scores, start=1):
            row = self.df.iloc[i]
            results.append({
                "rank": rank,
                "anime_id": int(row["anime_id"]),
                "anime_title": str(row["anime_title"]),
                "genres": str(row["genres"]),
                "type": str(row["type"]),
                "episodes": int(row["episodes"]),
                "rating": float(row["rating"]),
                "year_of_release": int(row["year_of_release"]),
                "similarity_score": round(float(score) * 100, 2)
            })

        return results

    def get_genres(self):
        """Returns unique list of all genre tags across the dataset."""
        if self.df is None:
            return []
        all_genres = set()
        for g in self.df["genres"].dropna():
            for item in g.split("|"):
                item_clean = item.strip()
                if item_clean:
                    all_genres.add(item_clean)
        return sorted(list(all_genres))
