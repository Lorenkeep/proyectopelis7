

# Busca Pelis

Este es el proyecto final del bootcamp cero de keepcoding.
## Como procedemos
Éste proyecto hace uso de la **API** de **# OMDb** que conseguiremos de [aquí.](http://www.omdbapi.com/apikey.aspx)


## Dependencias

> pip install -r requirements.txt
>



## Config.ini

Creamos el fichero **config.ini** con lo siguiente:

> [OMDb]
API_KEY=[AquíTuApiKey]
SEARCH_API_DETALLE=http://www.omdbapi.com/?apikey={}&i={}&plot=full
SEARCH_API_PELI= http://www.omdbapi.com/?apikey={}&s={}&page={}

## Arrancando

     - export FLASK_APP=run.py
     - flask run


