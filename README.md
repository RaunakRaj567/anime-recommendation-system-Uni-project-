# Anime Recommendation System

A content-based anime recommender that uses TF-IDF and cosine similarity on anime genre data. It includes a Tkinter desktop application and an optional FastAPI backend.

## Project Introduction

- Anime platforms provide a large number of titles, making it difficult for viewers to discover shows that match their interests.
- Manually searching through titles and genres can be time-consuming, especially for users who do not know what to watch next.
- This project addresses the problem by suggesting anime that are similar to a title selected by the viewer.
- Its purpose is to make finding the next anime to watch simple, quick, and convenient.
- The recommendations help viewers discover titles they may not have found through ordinary searches.
- It supports viewers who have a favorite anime and want to explore more shows with a similar style or theme.
- The project can save time by narrowing a large collection of anime into a more relevant list.
- It is useful for both regular anime viewers and people who are new to anime and need ideas to get started.
- The system demonstrates how a focused digital tool can improve entertainment and content discovery.
- Its design can support future improvements such as considering viewer ratings, watch history, and personal preferences.

## Objective and Scope

- To help viewers find anime that match their interests and viewing preferences.
- To provide useful suggestions based on an anime title selected by the viewer.
- To make the process of discovering new anime simple, quick, and convenient.
- To cover a collection of anime titles with information such as genres, ratings, episodes, and release years.
- To support both experienced anime viewers and people who are looking for anime recommendations for the first time.
- To provide a foundation for future improvements, including more personalized suggestions based on viewer feedback and watch history.

## Technology Stack Used

- **Programming Language:** Python
- **Development Environments:** PyCharm, Jupyter Notebook, and Visual Studio Code
- **Libraries and Packages:** NumPy, Pandas, Scikit-learn, Matplotlib, Seaborn, Tkinter, FastAPI, and Uvicorn
- **Data Processing and Analysis:** Pandas, NumPy, Matplotlib, and Seaborn
- **Recommendation and Prediction:** Scikit-learn
- **Desktop Application:** Tkinter
- **Web API:** FastAPI with Uvicorn
- **Version Control:** Git
- **Database:** No separate database is used; project data is stored in the provided dataset file

## Future Goals and Scope of Improvement

- Add viewer ratings and feedback so recommendations can become more relevant to each person.
- Include watch history and favorite titles to provide more personalized suggestions.
- Expand the collection with more anime, updated information, and additional details.
- Allow viewers to search and filter titles by genre, rating, release year, and number of episodes.
- Improve the recommendation results by considering story themes, characters, and viewer interests.
- Make the application easier to use and available on more devices in the future.

## Conclusion / Summary

This project provides a simple way for viewers to discover anime recommendations based on selected titles. It helps save time, explore similar shows,use of ML in solving rreal life problems and make viewing choices easier. The project also offers a strong foundation for future personalization and improvement.

## Acknowledgement

I would like to express my sincere gratitude to Aman Sir, my Python Project instructor, whose valuable guidance, encouragement, and support helped me throughout my project-building journey. His explanations, suggestions, and continuous motivation enabled me to improve my understanding, overcome challenges, and complete this project with greater confidence. I am truly thankful for the time and effort he devoted to guiding me at every stage of the project.

## Requirements

- Python 3.8 or newer
- Tkinter (usually included with Python; on Linux install your distribution's `python3-tk` package)
- The files `anime_recommender.pkl` and `anime_dataset_1.xls` in the project folder

## Installation

Open a terminal in the project directory and create a virtual environment:

```bash
python -m venv .venv
```

Activate it on Windows PowerShell:

```powershell
.venv\Scripts\Activate.ps1
```

Activate it on macOS or Linux:

```bash
source .venv/bin/activate
```

Install the required packages:

```bash
python -m pip install --upgrade pip
python -m pip install pandas scikit-learn fastapi uvicorn jupyter matplotlib seaborn
```

## Run the Desktop Application

Start the Tkinter GUI from the project directory:

```bash
python app.py
```

Select an anime title, choose the number of recommendations, and click **Get Recommendations**. The application loads `anime_recommender.pkl` automatically. If the pickle file is missing or invalid, the model is rebuilt from `anime_dataset_1.xls` and saved automatically.

## Run the API

Start the FastAPI server:

```bash
python api.py
```

The API is available at `http://127.0.0.1:8000`. Interactive API documentation is available at `http://127.0.0.1:8000/docs`.

Useful endpoints:

- `GET /titles` - list or search anime titles
- `GET /recommend?title=Anime%20Title&top_n=10` - get recommendations
- `GET /anime/{title}` - get anime details
- `GET /genres` - list available genres

## Run API and GUI Together

On macOS or Linux, use the provided script:

```bash
chmod +x start.sh
./start.sh
```

On Windows PowerShell, open two terminals in the project directory. Activate the virtual environment in both, then run:

```powershell
# Terminal 1
python api.py
```

```powershell
# Terminal 2
python app.py
```

## Optional Notebook

To open the model training and analysis notebook:

```bash
jupyter notebook Anime_recomendation_System.ipynb
```

## Project Files

- `app.py` - Tkinter desktop GUI
- `api.py` - FastAPI backend
- `recommender.py` - recommendation engine and model rebuilding logic
- `anime_recommender.pkl` - serialized recommendation model
- `anime_dataset_1.xls` - anime dataset
- `Anime_recomendation_System.ipynb` - analysis and model training notebook
