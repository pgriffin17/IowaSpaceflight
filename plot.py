import astroquery.jplhorizons as jpl
import astropy.time as time
import astropy.units as u
import numpy as np
import pandas as pd
import urllib.request
import read_web
from datetime import datetime
import re


# Get single vector for a given object
def getSingleVector(object):
    # Get current date using astropy.time
    now = time.Time.now()
    # Get only date from now, not time
    now = now.iso.split(' ')[0]
    vector = jpl.Horizons(id=object, location='500@0', epochs={now})
    vector = vector.vectors()
    return vector

def getPlanetVectors():
    planets = [i for i in range(1, 10)]
    planetVectors = {}
    for planet in planets:
        planetVectors[planet] = getSingleVector(planet)
    return planetVectors

def getPlanetData():
    planets = ["Mercury", "Venus", "Earth", "Mars", "Jupiter", "Saturn", "Uranus", "Neptune", "Pluto"]
    planetVectors = getPlanetVectors()
    # Set up dictionary to hold planet data
    planetData = {}
    # Populate dictionary with planet names
    for planet in planets:
        planetData[planet] = []

    # Want format of planetData to be:
    # planetData = {planet: [x, y, z]}
    for i in range(9):
        x = planetVectors[i+1]['x'][0]
        y = planetVectors[i+1]['y'][0]
        z = planetVectors[i+1]['z'][0]
        planetData[planets[i]] = {'x': x, 'y': y, 'z':z}

    # Convert to pandas dataframe
    planetData = pd.DataFrame(planetData)
    planetData = planetData.transpose()
    return planetData

def getVoyagerData():
    spacecraft = ["Voyager 1", "Voyager 2"]
    spacecraftVectors = {}
    for craft in spacecraft:
        spacecraftVectors[craft] = getSingleVector(craft)
    
    # Set up dictionary to hold spacecraft data
    spacecraftData = {}
    # Populate dictionary with spacecraft names
    for craft in spacecraft:
        spacecraftData[craft] = []
    
    for craft in spacecraft:
        x = spacecraftVectors[craft]['x'][0]
        y = spacecraftVectors[craft]['y'][0]
        z = spacecraftVectors[craft]['z'][0]
        spacecraftData[craft] = {'x': x, 'y': y, 'z':z}
    # Convert to pandas dataframe
    spacecraftData = pd.DataFrame(spacecraftData)
    spacecraftData = spacecraftData.transpose()
    return spacecraftData
    