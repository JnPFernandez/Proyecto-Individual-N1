<h1 align="center">**´MVP Movie Recommendation System´**</h1>

# ✏️ Project Description

This repository contains everything needed to run a movie recommendation system. I deployed it on Render. This system processes data from a large number of movies and, based on that data and the title of a movie entered by the user, it recommends 5 similar ones.
It also includes functions to:  <br>
- Get the number of movies released in a specific month.  <br>
- Get the number of movies released on a specific day.  <br>
- Get the score of a particular movie.  <br>
- Get the number of votes of a particular movie.  <br>

Demo: https://www.youtube.com/watch?v=_sTEYiiFzbs

# 🔎 Main Objectives

Build a graphical interface with a recommendation system that helps users find the movie they are looking for.

# 🗂️ Repository Structure

Proyecto-Individual-N1/

├── APIs.py # Python file with the functions

├── EDA.ipynb # Jupyter Notebook with the Exploratory Data Analysis

├── ETL.ipynb # Jupyter Notebook containing the Extract, Transform and Load process

├── README.md # Documentation (this file)

├── cast.csv # CSV file with cast information

├── crew.csv # CSV file with crew information (directors, VFX creators, animators, and backstage workers)

├── movies.csv # CSV file with movie information

└── requeriments.txt # Text file with function requirements

# ⚙️ Technologies and Tools

- **Render (for deployment)**

- **Jupyter Notebook (for EDA and ETL)**

- **Python 3.19 (libraries: FastAPI, APIRouter, pandas, JSONResponse, Response, json, cosine_similarity, TfidfVectorizer, MinMaxScaler, and numpy)**

# 🔁 Excel Transformations

For the "Credits" dataset, I split it into Cast and Crew for better data handling.

Cast: kept only the columns "movie_id", "cast_id", "cast_character", "actor_id", "cast_name".

Crew: kept only "movie_id", "crew_department", "crew_id", "crew_job", "crew_name".

Movies: used only "budget", "id", "popularity", "release_date", "revenue", "runtime", "title", "vote_average", "vote_count".

I limited each dataframe to the first 2,000 rows. Then, I filled missing values in revenue and budget with 0, removed nulls in release_date, created a new column "returncon" (revenue/budget), and extracted "release_year" from "release_date".

# 📥 Installation and Usage
```
git clone https://github.com/JnPFernandez/Proyecto-Individual-N1.git
cd Proyecto-Individual-2
```
- Deploy on Render

- Browse the different functions

# 👾 Function Descriptions

**Cantidad_filmaciones_mes**:
Created a dictionary mapping month names (string) to numbers. Used .lower() to avoid case sensitivity issues. If the input month was invalid, returned an error. Then filtered the movies dataframe to count how many movies were released in that month using .dt.month and .shape[0], stored the result in a new integer variable "cantidad", and returned it.

**Cantidad_filmaciones_dia**:
Similar process to the previous function, but used .dt.dayofweek instead of .dt.month.

**Score_titulo**:
Filtered the dataset by "title" to match the input movie title and stored it in a new dataframe "pelicula". With .iloc[0], selected only the first match in case of duplicates. Returned the title, release year, and score.

**Votos_titulo**:
Selected the first match by title with .iloc and extracted "title", "release_date", "vote_count", "vote_average". Stored it in "pelicula". Used an if to return only movies with more than 2,000 votes. Extracted only the year from "release_date" and returned the response as a dictionary.

**Get_actor**:
Filtered the Cast dataframe with .contains to find rows matching the given actor name (ignoring case and handling NaN with na=False). Stored results in "peliculas_actor". Merged with movies dataframe using "movie_id" and "id". Counted the number of movies with len() and stored as "cantidad_peliculas". Calculated total return with .sum() and average return by dividing total return by movie count. Returned these results.

**Get_director**:
Filtered the Crew dataframe to include only rows where "crew_job" = "Director". Retrieved all movies directed by that person. Calculated total return with .sum() on "returncon". Created the list "peliculas_info", iterated through the director’s movies with a for loop, and appended details ("title", "release_date", "returncon", "budget", "revenue") for each one. Returned the director’s name, total return, and detailed movie info.

# 📬 Contact

Email: juanpablofernandez132@gmail.com

LinkedIn: linkedin.com/in/juan-pablo-fernández-608a95217/

YouTube: https://www.youtube.com/@JuanPabloFern%C3%A1ndez-e6e
