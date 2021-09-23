﻿"""
 * Copyright 2020, Departamento de sistemas y Computación,
 * Universidad de Los Andes
 *
 *
 * Desarrolado para el curso ISIS1225 - Estructuras de Datos y Algoritmos
 *
 *
 * This program is free software: you can redistribute it and/or modify
 * it under the terms of the GNU General Public License as published by
 * the Free Software Foundation, either version 3 of the License, or
 * (at your option) any later version.
 *
 * This program is distributed in the hope that it will be useful,
 * but WITHOUT ANY WARRANTY; without even the implied warranty of
 * MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
 * GNU General Public License for more details.
 *
 * You should have received a copy of the GNU General Public License
 * along withthis program.  If not, see <http://www.gnu.org/licenses/>.
 *
 * Contribuciones:
 *
 * Dario Correal - Version inicial
 """


import copy
import time
from datetime import datetime
import config as cf

from DISClib.ADT import list as lt
from DISClib.Algorithms.Sorting import insertionsort as insertion
from DISClib.Algorithms.Sorting import mergesort as merge
from DISClib.Algorithms.Sorting import quicksort as quick
from DISClib.Algorithms.Sorting import shellsort as shell

assert cf

"""
Se define la estructura de un catálogo de videos. El catálogo tendrá dos listas, una para los videos, otra para las categorias de
los mismos.
"""

# Selectores

sort_algo = {1: insertion, 2: shell, 3: merge, 4: quick}

# Construccion de modelos

def newCatalog(implementation):
  """
  Inicializa el catálogo de artistas y obras (PENDIENTE)
  """
  catalog = {'artists': None,
             'artworks': None}

  if int(implementation) == 1:
    option = "ARRAY_LIST"
  elif int(implementation) == 2:
    option = "SINGLE_LINKED"

  catalog['artists'] = lt.newList(option, cmpfunction=compareartists)
  catalog['artworks'] = lt.newList(option, cmpfunction=cmpArtworkByDateAcquired)

  return catalog

def selectSample(catalog, sample):
  """
  Selecciona una muestra de los datos de la longitud que indique el parámetro sample
  """
  sample = int(sample)
  artworks_lenght = lt.size(catalog["artworks"])
  if sample not in range(artworks_lenght):
    lenght = artworks_lenght
  else:
    lenght = sample

  subsection = lt.subList(catalog["artworks"], 0, lenght)
  return subsection

# Funciones para agregar informacion al catalogo

def addArtwork(catalog, artwork):
    # Se adiciona la obra a la lista de obras
    lt.addLast(catalog['artworks'], artwork)
    # Se obtienen los artistas de la obra
    artists_ids = artwork['ConstituentID'].split(",")
    # Cada artista, se crea en la lista de artistas del catálogo, y se
    # crea una obraa en la lista de dicho artista (apuntador a la obra)
    for artist_id in artists_ids:
        addArtist(catalog, artist_id.strip(), artwork)

def addArtist(catalog, artist_id, artwork):
    """
    Adiciona un artista a lista de artistas, la cual guarda referencias
    a las obras de dicho artista
    """
    artists = catalog['artists']
    posartist = lt.isPresent(artists, artist_id)
    if posartist > 0:
        artist = lt.getElement(artists, posartist)
    else:
        artist = newArtist(artist_id)
        lt.addLast(artists, artist)

    lt.addLast(artist['Artworks'], artwork)

def addArtistInfo(catalog, artist_info):
  """
  Agrega la información de los artistas a la lista de artistas
  """
  artist_id = artist_info['ConstituentID']
  artists = catalog['artists']
  pos_artist = lt.isPresent(artists, artist_id)
  if pos_artist > 0:
    artist_info['Artworks'] = lt.getElement(artists, pos_artist)['Artworks']
    lt.changeInfo(artists, pos_artist, artist_info)
  else:
    artist_info['Artworks'] = lt.newList("ARRAY_LIST")
    lt.addLast(artists, artist_info)


# Funciones para creacion de datos
def newArtist(artist_id):
  """
  Crea una nueva estructura para modelar el perfil del artista (su información personal) y sus obras
  """
  artist = {"ConstituentID": None,
            "DisplayName": "",
            "BeginDate": None,
            "EndDate": None,
            "Nationality": "",
            "Gender": "",
            "ArtistBio": "",
            "Wiki QID": "",
            "ULAN": "",
            "Artworks": None}

  artist["ConstituentID"] = artist_id
  artist["Artworks"] = lt.newList('ARRAY_LIST')

  return artist

# Funciones de consulta

# Funciones utilizadas para comparar elementos dentro de una lista

def compareartists(artist_id, artist):
  if (artist_id in artist['ConstituentID']):
    return 0
  return -1

def cmpArtistsByBeginDate(artist1, artist2):
  """
  Devuelve verdadero (True) si el 'BeginDate' de artist1 es menores que el de artist2
    Args:
    artist1: informacion de la primera obra que incluye su valor 'BeginDate'
    artist2: informacion de la segunda obra que incluye su valor 'BeginDate'
  """
  if artist1['BeginDate'] < artist2['BeginDate']:
    return 1
  return 0

def cmpArtworkByDateAcquired(artwork1, artwork2):
  """
  Devuelve verdadero (True) si el 'DateAcquired' de artwork1 es menores que el de artwork2
    Args:
    artwork1: informacion de la primera obra que incluye su valor 'DateAcquired'
    artwork2: informacion de la segunda obra que incluye su valor 'DateAcquired'
  """
  if artwork1['DateAcquired'] < artwork2['DateAcquired']:
    return 1
  return 0

def cmpPrize(obra1, obra2):
  if(obra1["prize"] > obra2["prize"]):
    return 1
  return 0
# Funciones de ordenamiento

def cmpDate(obra1, obra2):
  if(obra1["Date"] > obra2["Date"]):
    return 1
  return 0

def sortArtistsByBeginDate(catalog, implementation, initial_date, end_date):
  """
  Ordena los artistas en el rango de fechas dispuesto
  """
  filterArtistsByBeginDate(catalog, initial_date, end_date)
  algorithm = sort_algo[int(implementation)]
  start_time = time.process_time()
  sorted_entries = algorithm.sort(catalog["artists"], cmpArtistsByBeginDate)
  stop_time = time.process_time()
  elapsed_time_mseg = round((stop_time - start_time) * 1000, 3)
  return elapsed_time_mseg, sorted_entries

def sortArtworksByDate(catalog, implementation, initial_year, end_year):
  """
  Ordena las obras en el rango de fechas dispuesto
  """
  filterArtworksByDate(catalog, initial_year, end_year)
  algorithm = sort_algo[int(implementation)]
  start_time = time.process_time()
  sorted_entries = algorithm.sort(catalog["artworks"], cmpArtworkByDateAcquired)
  stop_time = time.process_time()
  elapsed_time_mseg = (stop_time - start_time) * 1000
  return elapsed_time_mseg, sorted_entries
  
# Funciones auxiliares

def filterArtistsByBeginDate(catalog, initial_date, end_date):
  """
  Filtra los artistas que no se encuentren en el rango de años deseado
  (NO ESTÁ TERMINADA. FUNCIÓN ACTUALMENTE DEFECTUOSA)
  """
  iter_artists = enumerate(lt.iterator(catalog["artists"]))

  initial_date = datetime.strptime(initial_date, "%Y")
  end_date = datetime.strptime(end_date, "%Y")
  pos_to_delete = lt.newList()

  deleted_elements = 0
  for ix, artist in iter_artists:
    if type(artist["BeginDate"]) == None:
      print(f"TEMP: {type(artist['BeginDate'])}")
      lt.addLast(pos_to_delete, ix - deleted_elements)
      deleted_elements += 1
      continue
    elif artist["BeginDate"] == 0 or artist["BeginDate"] == "0":
      lt.addLast(pos_to_delete, ix - deleted_elements)
      deleted_elements += 1
      continue
    else:
      date = datetime.strptime(artist["BeginDate"], "%Y")
      if initial_date > date or end_date < date:
        lt.addLast(pos_to_delete, ix - deleted_elements)
        deleted_elements += 1
  
  for pos in lt.iterator(pos_to_delete):
    lt.deleteElement(catalog['artists'], pos)

def filterArtworksByDate(catalog, initial_date, end_date):
  """
  Filtra las obras que no se encuentren en el rango de años deseado
  """
  iter_artworks = lt.iterator(catalog["artworks"])

  initial_date = datetime.strptime(initial_date, "%Y-%m-%d")
  end_date = datetime.strptime(end_date, "%Y-%m-%d")
  pos_to_delete = lt.newList()

  deleted_elements = 0
  for ix, artwork in enumerate(iter_artworks):
    if artwork["DateAcquired"] == '':
      lt.addLast(pos_to_delete, ix - deleted_elements)
      deleted_elements += 1
      continue
    art_dates = datetime.strptime(artwork["DateAcquired"], "%Y-%m-%d")
    if initial_date > art_dates or end_date < art_dates:
      lt.addLast(pos_to_delete, ix - deleted_elements)
      deleted_elements += 1
  
  for pos in lt.iterator(pos_to_delete):
    lt.deleteElement(catalog['artworks'], pos)

def getArtist(catalog, artistname):
  """
  Devuelve una lista con el número de obras de un artista, un diccionario con las técnicas utilizadas y el número de veces fueron utilizadas,
  la técnica que fue más utilizada y una lista que contiene una muestra de tres obras con la técnica más utilizada.
  """

  for x in lt.iterator(catalog["artists"]):
    if artistname == x["DisplayName"]:
      y= x["Artworks"]

  n_obras= len(y["elements"])
  diccionario= {}

  for x in y["elements"]:      
    diccionario[x["Classification"]]= 0

  for x in y["elements"]:        
    diccionario[x["Classification"]]+=1

  max_key = max(diccionario, key= diccionario.get)    
  obras_mas_utilizadas= lt.newList(datastructure='SINGLE_LINKED')
  n=0
  muestra= 0

  while (n < n_obras) and (muestra < 3):
    if(y["elements"][n]["Classification"] == max_key):
      lt.addLast(obras_mas_utilizadas, y["elements"][n])
      muestra +=1
    n+=1

  respuestas= lt.newList(datastructure="ARRAY_LIST")
  lt.addLast(respuestas, n_obras)
  lt.addLast(respuestas, diccionario)
  lt.addLast(respuestas, max_key)
  lt.addLast(respuestas, obras_mas_utilizadas)

  return respuestas

def transportar_obras(departamento, catalog):

  obras_dept= lt.newList(datastructure="ARRAY_LIST")
  obras_dept2= lt.newList(datastructure="ARRAY_LIST")
  for x in lt.iterator(catalog["artworks"]):
    if(x["Department"] == departamento):
      lt.addLast(obras_dept, x)
      lt.addLast(obras_dept2, x)
  total_obras= lt.size(obras_dept)
  lista= lt.newList(datastructure= "ARRAY_LIST")
  precio_total= 0
  obras_caras= lt.newList(datastructure="ARRAY_LIST")
  obras_viejas= lt.newList(datastructure= "ARRAY_LIST")
  peso_total= 0
  diccionario= {}
  for x in lt.iterator(obras_dept):
    precio= 0
    peso= 0
    if(x["Circumference (cm)"] != '') and (x["Circumference (cm)"] != '0.0'):
      lt.addLast(lista, x["Circumference (cm)   "])
    if(x["Depth (cm)"] != '') and (x["Depth (cm)"] != '0.0'):
      lt.addLast(lista, x["Depth (cm)"])
    if(x["Diameter (cm)"] != '') and (x["Diameter (cm)"] != '0.0'):
      lt.addLast(lista, x["Diameter (cm)"])
    if(x["Height (cm)"] != '') and (x["Height (cm)"] != '0.0'):
      lt.addLast(lista, x["Height (cm)"])
    if(x["Length (cm)"] != '') and (x["Length (cm)"] != '0.0'):
      lt.addLast(lista, x["Length (cm)"])
    if(x["Width (cm)"] != '') and (x["Width (cm)"] != '0.0'):
      lt.addLast(lista, x["Width (cm)"])
    if(x["Weight (kg)"] != '') and (x["Weight (kg)"] != '0.0'):
      peso= x["Weight (kg)"]
    n= lt.size(lista)

    if(n == 3):
      precio= ((float(lt.getElement(lista, 1)) * float(lt.getElement(lista, 2)) * float(lt.getElement(lista, 3)) + peso)/1000000)*72
    elif(n == 2):
      precio= ((float(lt.getElement(lista, 1)) * float(lt.getElement(lista, 2)) + peso)/10000)*72
    elif(n == 0) or (n==1):
      precio= 48

    diccionario[x["Title"]]= x["Date"]
    x["prize"]= precio

    while n > 0:
      lt.deleteElement(lista, n)
      n-=1
    precio_total += precio
    peso_total += peso
  obras_caras= shell.sort(obras_dept, cmpPrize)
  obras_viejas= shell.sort(obras_dept2, cmpDate)
  respuesta= lt.newList(datastructure="ARRAY_LIST")
  lt.addLast(respuesta, total_obras)
  lt.addLast(respuesta, precio_total)
  lt.addLast(respuesta, peso_total)
  lt.addLast(respuesta, obras_viejas)
  lt.addLast(respuesta, obras_caras)
  return respuesta