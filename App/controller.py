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
 """

from model import addArtWork
import config as cf
import model
import csv


"""
El controlador se encarga de mediar entre la vista y el modelo.
"""

# Inicialización del Catálogo de libros
def initCatalog():
    catalog = model.newCatalog()
    return catalog

def artistsInfo():
    artists_info = model.artistsInfo()
    return artists_info

# Funciones para la carga de datos
def loadData(catalog, artists_info):
    loadArtistsinfo(artists_info)
    loadArtWorks(catalog)
   

def loadArtWorks(catalog):
    artworksfile = cf.data_dir + 'MoMA/Artworks-utf8-large.csv'
    input_file = csv.DictReader(open(artworksfile, encoding = 'utf-8'))
    for artwork in input_file:
        model.addArtWork(catalog, artwork)

def loadArtistsinfo(artists_info):
    artistsfile = cf.data_dir + 'MoMA/Artists-utf8-large.csv'
    input_file =  csv.DictReader(open(artistsfile, encoding= 'utf-8'))
    
    for info in input_file:
        model.addArtistsInfo(artists_info, info)
    


# Funciones de ordenamiento

# Funciones de consulta sobre el catálogo
