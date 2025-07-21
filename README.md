# <h1 align="center">**`MVP Sistema de recomendación de peliculas`**</h1>

# ✏️ Descripción del proyecto
Este repositorio contiene todo lo necesario para hacer correr un sistema de recomendación. Yo lo corrí en Render. Este sistema toma datos de una gran cantidad de peliculas, y en base a eso, y al titulo de una pelicula ingresado por el usuariote recomienda 5. Por otro lado también tiene funciones para:  <br>
- Saber que cantidad de peliculas que fueron estrenadas en un mes en particular.  <br>
- Saber que cantidad de peliculas que fueron estrenadas en un dia en particular.  <br>
- Saber el score de una pelicula en particular.  <br>
- Saber la cantidad de votos de una pelicula en particular.  <br>

Demostración: https://www.youtube.com/watch?v=_sTEYiiFzbs

# 🔎 Objetivos principales:
Crear una interfaz gráfica con un sistema de recomendación que ayude a los usuarios a encontrar la película que están buscando.

# 🗂️ Estructura del repositorio

Proyecto-Individual-N1/

├── APIs.py                   # Archivo con las funciones en python

├── EDA.ipynb                 # Archivo con el informe EDA (Análisis Exploratorio de los Datos)

├── ETL.ipynb                 # Archivo de Jupiter Notebook que contiene la Extracción, Transformación y Carga (Load) de los datos

├── README.md                 # Documentación (este archivo)

├── cast.csv                  # Archivo csv con la información de los elencos

├── crew.csv                  # Archivo csv con la información de la "crew", tripulación en español literal, se refiere a los directores, creadores de efectos visuales, animadores, y demás personas que trabajaron en el detrás de escena

├── movies.csv                # Archivo csv con la información de las películas

└── requeriments.txt          # Archivo de texto con los requerimientos de las funciones

# ⚙️ Tecnologías y Herramientas

- **Render** (para deployar las funciones)

- **Jupyter Notebook** (para el EDA y el ETL)
  
- **Python 3.19** (librerías: FastAPI, APIRouter, pandas, JSONResponse, Response, json, cosine_similarity, TfidfVectorizer, MinMaxScaler y numpy)

# 🔁 Tranformaciones del Excel:

Para el dataset "Credits" lo dividi en 2, en Cast y Crew para un mejor manejo de la información. Solamente dejé las columnas de: "movie_id", "cast_id","cast_character","actor_id","cast_name" en el caso de Cast  <br>
Y en el caso de Crew solamente: "movie_id", "crew_department", "crew_id", "crew_job" y "crew_name". Por otro lado del dataset Movies solamente use las columnas: "budget", "id", "popularity", "release_date", "revenue", "runtime", "title", "vote_average" y "vote_count". <br>
De cada Dataframe solamente dejé las primeras 2.000 filas. Luego rellene los campos de revenue y budget con 0, eliminé nulos de release_date y cree la nueva columna de return ("returncon"). Y cree la columna "release_year" con el año de "release_date".

# 📥 Instalación y Uso
```
git clone https://github.com/JnPFernandez/Proyecto-Individual-N1.git
cd Proyecto-Individual-2
```
- Deployar en Render

- Navegar las diferentes funciones

# 👾 Descripción de las funciones

- En **cantidad_filmaciones_mes**, cree un diccionario relacionando los meses str con un numero. Use lower para pasar a minuscula y evitar problemas con mayusculas y minusculas. Si el mes ingresado no era valido, use if para devolver un error en ese caso.
Luego filtré el df de movies para contar cuántas peliculas fueron estrenadas en el mismo mes que se ingreso con las funciones .dt.month y .shape[0], y lo asigne en una variable de tipo entero nueva llamada "cantidad".
Y luego retorne el resultado.

- En **cantidad_filmaciones_dia**, hice basicamente el mismo proceso que en la función anterior con la diferencia que en vez de la función dt.month, use la función dt.dayofweek.

- En **score_titulo**, filtre el dataset en "title" buscando la fila que coincida con el titulo insertado, y los valores los guarde en un nuevo df llamado "pelicula". Con .iloc[0] solamente toma los valores de la primera pelicula, por si hay valores repetidos, que es improbable pero bueno,por las dudas.
Y por último la función retorna el titulo, el año y el score.

- En **votos_titulo**, seleccionamos la primera coincidencia con el titulo con .iloc y extraemos las columnas necesarias para la respuesta: "title", "release_date", "vote_count" y "vote_average". Todo esto lo guardamos en una serie llamada "pelicula". Usamos un if para devolver unicamente las peliculas con más de 2.000 votos. Luego pasamos pelicula a diccionario. De "release_date" sacamos unicamente el año con la función .year. Y por último retornamos la respuesta.

- En **get_actor**, primero filtramos el df Cast buscando cuál coincide con el nombre dado usando la función .contains, ignoramos mayusculas y minnusculas con "case=fasle" y por otro lado usamos "na=false" para que los valores Nan sean tomados como Falsos para evitar errores, osea que son detectados por contains como una no coincidencia con el titulo dado, todo esto lo guardamos en un nuevo df llamado "peliculas_actor". Luego hice un merge entre este nuevo df y el df de movies, trayendo toda la información de movies usando como conector "movie_id"(cast) e "id"(movies). Esto lo almacene en un nuevo df llamado "peliculas". Luego use len para contar la cantidad de peliculas que tenía el actor y lo guarde en un int "cantidad_peliculas". Después calcule una nueva variable float "retorno_total" sumando los retornos de las peliculas con la función .sum. Y retorno_promedio, diviendo retorno total por cantidad de peliculas. Y por último el retorno.

- En **get_director**, primero, del df de crew, filtramos unicamente donde indique que el trabajo es de director en la columna "crew_job" y buscamos que peliculas contienen al director. Luego calculamos el retorno total del director con returncon y la función .sum y la guardamos en la nueva variable float "retorno_total". Después un paso muy importante, cree la lista "peliculas_info" que luego la vamos a retornar. Use un for iterando sobre las peliculas del director, agregando con la función .append la información de cada pelicula a la lista "peliculas_info", información sería especificamente las columnas "title", "release_date", "returncon", "budget" y "revenue". Y por ultimo retornamos el nombre del director, su retorno total y la información sobre sus peliculas.

# 📬 Contacto

Correo: juanpablofernandez132@gmail.com

LinkedIn: linkedin.com/in/juan-pablo-fernández-608a95217/
