from fastapi import FastAPI, HTTPException, Query
from fastapi.middleware.cors import CORSMiddleware
from recommender import AnimeRecommender
import uvicorn

app = FastAPI(
    title="Anime Recommendation System API",
    description="REST API powered by TF-IDF & Cosine Similarity for anime recommendations using pickled model.",
    version="1.0.0"
)

# Enable CORS for web frontend access
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize recommender engine
recommender = AnimeRecommender()


@app.get("/", summary="API Root / Health Check")
def root():
    """Returns API overview, dataset metrics, and available endpoints."""
    titles = recommender.get_all_titles()
    genres = recommender.get_genres()
    return {
        "message": "Welcome to the Anime Recommendation System API!",
        "status": "online",
        "total_anime": len(titles),
        "total_genres": len(genres),
        "docs_url": "/docs",
        "endpoints": {
            "get_all_titles": "/titles?q={search_term}",
            "get_recommendations": "/recommend?title={anime_title}&top_n={count}",
            "get_anime_details": "/anime/{anime_title}",
            "get_genres": "/genres"
        }
    }


@app.get("/titles", summary="Get or Search Anime Titles")
def get_titles(q: str = Query(None, description="Optional search query to filter anime titles")):
    """Returns a list of all anime titles or filters them by search query."""
    matching_titles = recommender.get_all_titles(query=q if q else "")
    return {
        "query": q,
        "count": len(matching_titles),
        "titles": matching_titles
    }


@app.get("/recommend", summary="Get Anime Recommendations")
def get_recommendations(
    title: str = Query(..., description="Anime title to base recommendations on"),
    top_n: int = Query(10, ge=1, le=50, description="Number of recommendations to return (1-50)")
):
    """
    Generates recommendations for a specified anime title based on genre cosine similarity.
    """
    results = recommender.recommend(title=title, top_n=top_n)
    if results is None:
        raise HTTPException(
            status_code=404,
            detail=f"Anime '{title}' not found in dataset. Use /titles to search valid titles."
        )

    target_details = recommender.get_anime_details(title)
    return {
        "query_title": title,
        "target_anime": target_details,
        "requested_count": top_n,
        "returned_count": len(results),
        "recommendations": results
    }


@app.get("/anime/{title}", summary="Get Anime Metadata")
def get_anime_details(title: str):
    """Returns metadata (id, title, genres, episodes, rating, year) for a specific anime."""
    details = recommender.get_anime_details(title)
    if details is None:
        raise HTTPException(status_code=404, detail=f"Anime '{title}' not found.")
    return details


@app.get("/genres", summary="Get Unique Genres")
def get_genres():
    """Returns a list of all unique anime genres in the dataset."""
    genres = recommender.get_genres()
    return {
        "count": len(genres),
        "genres": genres
    }


if __name__ == "__main__":
    uvicorn.run("api:app", host="127.0.0.1", port=8000, reload=True)
