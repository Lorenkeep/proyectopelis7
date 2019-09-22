from app import app
from flask import render_template, request, redirect, url_for, flash
import csv, sqlite3
from os import remove, rename
import configparser
import requests
import json

config = configparser.ConfigParser()
config.read('config.ini')
url = config['OMDb']['SEARCH_API_PELI']
api_key = config['OMDb']['API_KEY']
buskeda_peli = config['OMDb']['SEARCH_API_PELI']
buskeda_peli_id = config['OMDb']['SEARCH_API_DETALLE']


@app.route('/')
def index():
        return render_template("index.html")


@app.route("/detalle", methods=["POST"])
def detalle():
        if request.method == "POST":
                imbdid = request.values.get(request.values.get("selection"))
                peli = APIdetalle(imbdid)
                buskeda = request.values.get("buskeda")
                internetmoviedb="no"
                try:
                        peli["Ratings"][0]["Value"]    
                except:
                        internetmoviedb= "N/A"
                if internetmoviedb == "no":
                        internetmoviedb= peli["Ratings"][0]["Value"]
                        
                ratings = "no"
                try:
                        peli["Ratings"][1]["Value"]
                except:
                        ratings = "N/A"
                if ratings == "no":
                        ratings= peli["Ratings"][1]["Value"]
                
                metacriticrating = "no"
                try:
                        peli["Ratings"][2]["Value"]
                except:
                        metacriticrating = "N/A"
                if metacriticrating == "no":
                        metacriticrating= peli["Ratings"][2]["Value"]
                
                return render_template("detalle.html",internetmoviedb=internetmoviedb, metacriticrating=metacriticrating, buskeda=buskeda, peli=peli, ratings=ratings)
                

        







@app.route('/peliculas', methods=["POST"])
def buskeda():
        if request.method == "POST":
                buskeda = request.values.get("buskeda")
                if request.values.get('sig') or request.values.get("prev"):
                        if request.values.get("prev"):
                                page= int(request.values.get("prev")) -1
                        if request.values.get("sig"):
                                page= int(request.values.get("sig")) +1
                        resultadoBusqueda, pageactual = APIpelis (buskeda, page)
                else:
                        
                        resultadoBusqueda, pageactual= APIpelis(buskeda)
                pageactual=int(pageactual) 

                if resultadoBusqueda["Response"] == "False":
                        nosepuedebuscar="No hay resultados para la(s) palabra(s) introducidas"
                        return render_template("index.html", nosepuedebuscar=nosepuedebuscar)
                
                else:
                        nosepuedebuscar=""
                        buskedapelis = resultadoBusqueda["Search"]
                        totalpeliculas = int(resultadoBusqueda["totalResults"])
                        numeropaginas= totalpeliculas
                        #print("Se  encontrado {} peliculas".format(totalpeliculas))
                        if totalpeliculas % 10 ==0:
                                numeropaginas=totalpeliculas //10
                        else:
                                numeropaginas=(totalpeliculas //10) +1
                                #print (totalpeliculas)
                                #print (numeropaginas)
                
                        return render_template("peliculas.html",nosepuedebuscar=nosepuedebuscar, buskedapelis=buskedapelis,buskeda=buskeda, pageactual= pageactual, totalpeliculas=totalpeliculas, numeropaginas=numeropaginas, resultadoBusqueda=resultadoBusqueda)


def APIpelis(buskeda, page='1'):
    url = buskeda_peli.format(api_key, buskeda, page)
    response = requests.get(url)

    if response.status_code == 200:
        resultadoBusqueda = json.loads(response.text)
        print(resultadoBusqueda["Response"])
        return resultadoBusqueda, page
    else:
        print('Se ha producido un error en la petición: ', response.status_code)

def APIdetalle(imbdid):
    url = buskeda_peli_id.format(api_key, imbdid)
    response = requests.get(url)

    if response.status_code == 200:
        resultadodetalle = json.loads(response.text)
        return resultadodetalle
    else:
        print('Se ha producido un error en la petición: ', response.status_code)







