# <h1 align="center">**`MVP Sistema de recomendación de peliculas`**</h1>

# ✏️ Descripción del proyecto+
Este repositorio contiene todo lo necesario para hacer correr un sistema de recomendación. Yo lo corrí en Render. Este sistema toma datos de una gran cantidad de peliculas, y en base a eso, y al titulo de una pelicula ingresado por el usuariote recomienda 5. Por otro lado también tiene funciones para 
Este repositorio contiene un archivo .py con la codificación de las API´s para el funcionamiento del sistema de recomendación, un archivo jupyter notebook con el Análisis Exploratorio de los Datos, otro con el proceso de Extracción, Transformación y Carga de los datos. Los 3 archivos fuente en .csv. Y un archivo .txt con los requerimientos de las funciones. 

# 🔎 Objetivos principales:

- Analizar la evolución de los accesos por tecnología (ADSL, Cablemodem, Fibra Óptica) a través del tiempo.

- Medir el KPI obligatorio: crecimiento mínimo de 2% de accesos por cada 100 hogares por provincia en el próximo trimestre.

- Proponer y visualizar tres KPIs adicionales: participación de Fibra Óptica en el AMBA, cuota de mercado de Fibra óptica y cuota de mercado de Cablemodem por provincia.

- Identificar oportunidades de despliegue y mejora en provincias menos saturadas.

- 
**"TRANSFORMACIONES"**: Para el dataset "Credits" lo dividi en 2, en Cast y Crew para un mejor manejo de la información. Solamente dejé las columnas de: "movie_id", "cast_id","cast_character","actor_id","cast_name" en el caso de Cast. 
Y en el caso de Crew solamente: "movie_id", "crew_department", "crew_id", "crew_job" y "crew_name". Por otro lado del dataset Movies solamente use las columnas: "budget", "id", "popularity", "release_date", "revenue", "runtime", "title", "vote_average" y "vote_count"
De cada Dataframe solamente dejé las primeras 2.000 filas. Luego rellene los campos de revenue y budget con 0, eliminé nulos de release_date y cree la nueva columna de return ("returncon"). Y cree la columna "release_year" con el año de "release_date".


**"DESARROLLO API"**: Genere las 6 funciones APIs. Importe las librerías de FastAPI, APIRouter, pandas, JSONResponse, Response, json, cosine_similarity, TfidfVectorizer, MinMaxScaler y numpy.
Luego cargue los datasets. 

En **cantidad_filmaciones_mes**, cree un diccionario relacionando los meses str con un numero. Use lower para pasar a minuscula y evitar problemas con mayusculas y minusculas. Si el mes ingresado no era valido, use if para devolver un error en ese caso.
Luego filtré el df de movies para contar cuántas peliculas fueron estrenadas en el mismo mes que se ingreso con las funciones .dt.month y .shape[0], y lo asigne en una variable de tipo entero nueva llamada "cantidad".
Y luego retorne el resultado.

En **cantidad_filmaciones_dia**, hice basicamente el mismo proceso que en la función anterior con la diferencia que en vez de la función dt.month, use la función dt.dayofweek.

En **score_titulo**, filtre el dataset en "title" buscando la fila que coincida con el titulo insertado, y los valores los guarde en un nuevo df llamado "pelicula". Con .iloc[0] solamente toma los valores de la primera pelicula, por si hay valores repetidos, que es improbable pero bueno,por las dudas.
Y por último la función retorna el titulo, el año y el score.

En **votos_titulo**, seleccionamos la primera coincidencia con el titulo con .iloc y extraemos las columnas necesarias para la respuesta: "title", "release_date", "vote_count" y "vote_average". Todo esto lo guardamos en una serie llamada "pelicula". Usamos un if para devolver unicamente las peliculas con más de 2.000 votos. Luego pasamos pelicula a diccionario. De "release_date" sacamos unicamente el año con la función .year. Y por último retornamos la respuesta.

En **get_actor**, primero filtramos el df Cast buscando cuál coincide con el nombre dado usando la función .contains, ignoramos mayusculas y minnusculas con "case=fasle" y por otro lado usamos "na=false" para que los valores Nan sean tomados como Falsos para evitar errores, osea que son detectados por contains como una no coincidencia con el titulo dado, todo esto lo guardamos en un nuevo df llamado "peliculas_actor". Luego hice un merge entre este nuevo df y el df de movies, trayendo toda la información de movies usando como conector "movie_id"(cast) e "id"(movies). Esto lo almacene en un nuevo df llamado "peliculas". Luego use len para contar la cantidad de peliculas que tenía el actor y lo guarde en un int "cantidad_peliculas". Después calcule una nueva variable float "retorno_total" sumando los retornos de las peliculas con la función .sum. Y retorno_promedio, diviendo retorno total por cantidad de peliculas. Y por último el retorno.

En **get_director**, primero, del df de crew, filtramos unicamente donde indique que el trabajo es de director en la columna "crew_job" y buscamos que peliculas contienen al director. Luego calculamos el retorno total del director con returncon y la función .sum y la guardamos en la nueva variable float "retorno_total". Después un paso muy importante, cree la lista "peliculas_info" que luego la vamos a retornar. Use un for iterando sobre las peliculas del director, agregando con la función .append la información de cada pelicula a la lista "peliculas_info", información sería especificamente las columnas "title", "release_date", "returncon", "budget" y "revenue". Y por ultimo retornamos el nombre del director, su retorno total y la información sobre sus peliculas.


**"DEPLOYMENT"**: Use render para deployar mis APIs a traves de FastAPI.


**"EDA"**: Importe las librerías necesarias, leí los archivos csv guardados después del ETL. Use la función .info y .describe con cada df. Luego las funciones .isnull y .duplicated para revisar nulos y duplicados.  Grafique la relación entre budget y revenue. Hice un boxplot de revenue y luego un histograma donde se puede ver la frecuencia de los valores 0s en la columna. Y por último realize una nube de palabras con los titulos de las peliculas.


**"SISTEMA DE RECOMENDACIÓN"**: Use las funciones lower y strip para no generar fallos entre mayusculas y minusculas, y para eliminar los espacios antes y después, para evitar también fallos. Luego cree un df "peliculas" con los datos del df movies que coincidian con el titulo insertado por el usuario. Luego cree el float "puntaje" con el "vote_average" de la pelicula ingresada. Después busque en el df movies peliculas con puntajes similadres (entre -0.1 y +0.1) guardandolas en un nuevo df llamado "peliculas_similares". Excluí la pelicula ingresada porque sino iba a aparecer en la respuesta al ser identica. Use un if por si el df "peliculas_similares" tenía más de 5 valores, lo cuál no debía de suceder, y en caso de que sea verdad use la función tf idf para convertir a vector los titulos asi se podía usar similitud de coseno.  En una nueva columna del df peliculas_similares, llamada "similaridad_titulo" inserte la suma de "similitudes"(que fue la calculada con similaridad de coseno). Después ordene este df "peliculas_similares" de mayor a menor con la función .sort_values según los valores "vote_average" y "similaridad_titulo". Y use el else por si habían pocas peliculas directamente se ordenaban por Vote_average. Luego retorne el df peliculas_similares en ["title] usando la función .head con los primeros 5 datos y convirtiendolo en diccionario con la función .to_dict
