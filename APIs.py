from fastapi import FastAPI, APIRouter
import pandas as pd
from fastapi.responses import Response
import json
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.preprocessing import MinMaxScaler
import numpy as np

# Cargamos los dataset
movies = pd.read_csv("movies.csv")
cast = pd.read_csv("cast.csv")
crew= pd.read_csv("crew.csv")

# Aseguramos que las fechas estén en formato datetime
movies["release_date"] = pd.to_datetime(movies["release_date"], errors="coerce")

app = FastAPI()

@app.get("/cantidad_filmaciones_mes/{mes}")
def cantidad_filmaciones_mes(mes: str):
    meses = {
        "enero": 1, "febrero": 2, "marzo": 3, "abril": 4, "mayo": 5, "junio": 6,
        "julio": 7, "agosto": 8, "septiembre": 9, "octubre": 10, "noviembre": 11, "diciembre": 12
    }
    mes = mes.lower()
    if mes not in meses:
        return {"error": "Mes inválido"}

    cantidad = movies[movies["release_date"].dt.month == meses[mes]].shape[0]
    return {f"{cantidad} películas fueron estrenadas en el mes de {mes}"}

@app.get("/cantidad_filmaciones_dia/{dia}")
def cantidad_filmaciones_dia(dia: str):
    dias = {
        "lunes": 0, "martes": 1, "miércoles": 2, "jueves": 3,
        "viernes": 4, "sábado": 5, "domingo": 6
    }
    dia = dia.lower()
    if dia not in dias:
        return {"error": "Día inválido"}

    cantidad = movies[movies["release_date"].dt.dayofweek == dias[dia]].shape[0]
    return {f"{cantidad} películas fueron estrenadas en los días {dia}"}

@app.get("/score_titulo/{titulo}")
def score_titulo(titulo: str):
    pelicula = movies[movies["title"].str.lower() == titulo.lower()]
    if pelicula.empty:
        return {"error": "Película no encontrada"}

    pelicula = pelicula.iloc[0]
    return {
        "titulo": pelicula["title"],
        "año": pelicula["release_date"].year,
        "score": pelicula["popularity"]
    }

@app.get("/votos_titulo/{titulo}")
def votos_titulo(titulo: str):
    pelicula = movies[movies["title"].str.lower().str.strip() == titulo.lower().strip()]
    
    if pelicula.empty:
        return {"error": "Película no encontrada"}
    
    # Seleccionar solo las columnas deseadas
    pelicula = pelicula.iloc[0][["title", "release_date", "vote_count", "vote_average"]]
    if pelicula["vote_count"]<2000:
        return("La pelicula cuenta con menos de 2.000 votaciones, por lo cual no se devuelve información")
    
    # Convertir release_date a solo el año
    pelicula_dict = pelicula.to_dict()
    pelicula_dict["release_date"] = pelicula["release_date"].year  # Obtener solo el año

    return ("La pelicula", pelicula_dict["title"], "fue estrenada en el año ", pelicula_dict["release_date"],
            ". La misma cuenta con un total de ",pelicula_dict["vote_count"],"valoraciones, con un promedio de"
            ,pelicula_dict["vote_average"])

@app.get("/get_actor/{nombre}")
def get_actor(nombre: str):
    peliculas_actor = cast[cast["cast_name"].str.contains(nombre, case=False, na=False)]
    if peliculas_actor.empty:
        return {"error": "Actor no encontrado"}
    peliculas = peliculas_actor.merge(movies, left_on="movie_id", right_on="id")
    cantidad_peliculas = len(peliculas)
    retorno_total = peliculas["returncon"].sum()
    retorno_promedio = retorno_total / cantidad_peliculas if cantidad_peliculas > 0 else 0
    return {("El actor", nombre,"ha participado de", cantidad_peliculas, 
            "filmaciones, el mismo ha obtenido un retorno de", retorno_total,
            "con un promedio por filmación de", round(retorno_promedio, 2))
    }

@app.get("/get_director/{nombre}")
def get_director(nombre: str):
    directores = crew[(crew["crew_job"].str.lower() == "director") & (crew["crew_name"].str.contains(nombre, case=False, na=False))]
    
    if directores.empty: return{"error":"No se ha encontrado el nombre del director"}

    peliculas_director = movies[movies["id"].isin(directores["movie_id"])]
    
    if peliculas_director.empty: return {"error": "No se han encontrado películas de este director"}

    retorno_total = peliculas_director["returncon"].sum()

    peliculas_info = []
    for _, row in peliculas_director.iterrows():
        peliculas_info.append({
            "Titulo": row["title"],
            "Fecha de lanzamiento": row["release_date"],
            "Retorno individual": round(row["returncon"], 2),
            "Costo": row["budget"],
            "Ganancia": row["revenue"] - row["budget"]
        })
    
    return {
        "Director": nombre,
        "Retorno total": retorno_total,
        "Información sobre sus peliculas": peliculas_info
    }

@app.get("/recomendacion/{titulo}")
def recomendacion(titulo: str):
    movies["title"] = movies["title"].str.lower().str.strip()

    pelicula = movies[movies["title"] == titulo.lower().strip()]
    
    if pelicula.empty:
        return {"error": "Película no encontrada"}
    
    puntaje = pelicula["vote_average"].values[0]

    # Filtramos las películas con puntaje dentro de un rango cercano
    peliculas_similares = movies[(movies["vote_average"] >= puntaje - 0.1) & (movies["vote_average"] <= puntaje + 0.1)]
    peliculas_similares = peliculas_similares[peliculas_similares["title"] != titulo.lower().strip()]

    # Si hay más de 5 películas, aplicamos similitud de título con TF-IDF
    if len(peliculas_similares) > 5:
        vectorizer = TfidfVectorizer(stop_words="english")
        tfidf_matrix = vectorizer.fit_transform(peliculas_similares["title"])

        # Calculamos la similitud de coseno
        similitudes = cosine_similarity(tfidf_matrix)

        # Sumamos la similitud total para cada película
        peliculas_similares["similaridad_titulo"] = similitudes.sum(axis=1)

        # Ordenamos por vote_average (descendente) y luego por similaridad_titulo (descendente)
        peliculas_similares = peliculas_similares.sort_values(by=["vote_average", "similaridad_titulo"], ascending=[False, False])
    else:
        # Si hay 5 o menos, simplemente ordenamos por vote_average de mayor a menor
        peliculas_similares = peliculas_similares.sort_values(by="vote_average", ascending=False)

    return peliculas_similares[["title"]].head(5).to_dict(orient="records")

