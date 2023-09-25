#writen by jake on 2023-09-23 for Iowa Spaceflight at HackUIowa

from taipy.gui import Gui
import datetime
import celestrak
import plot
import pandas as pd

content = './UI_instruments_in_space.jpg' #

my_theme = {
  "palette": {
    "background": {"default": "#000000"},
    "primary": {"main": "#FFCD00"},
    "secondary": {"main": "#00664F"},
  }
}

planet_coords = plot.getPlanetData()
data = planet_coords.to_dict(orient='list')
print(data)
#planet_coords = [{'x': data['x'], 'y': data['y'], 'z': data['z'], 'name': planet_coords.index.values.tolist()}]
planet_coords = [{'x': data['x'], 'y': data['y']}]
# Add two nan values to the end of each list
for i in range(len(planet_coords)):
    planet_coords[i]['x'].append(float('nan'))
    planet_coords[i]['y'].append(float('nan'))
    planet_coords[i]['x'].append(float('nan'))
    planet_coords[i]['y'].append(float('nan'))

voyager_coords = plot.getVoyagerData()
data = voyager_coords.to_dict(orient='list')
#voyager_coords = [{'x': data['x'], 'y': data['y'], 'z': data['z'], 'name': voyager_coords.index.values.tolist()}]
voyager_coords = [{'x': data['x'], 'y': data['y']}]
for j in range(9):
    for i in range(len(voyager_coords)):
        voyager_coords[i]['x'].insert(0, float('nan'))
        voyager_coords[i]['y'].insert(0, float('nan'))
        #voyager_coords[i]['z'].append(float('nan'))

#Add voyager data to planet data by concatenating the lists
object_coords = planet_coords + voyager_coords

markers = [
    # First data set is represented by increasingly large
    # disks, getting more and more opaque
    {
        "color": "#636efa"
    },
    # Second data set is represented with a different symbol
    # for each data point
    {
        "color": "#FFCD00"
    }
]


layout = {
    "width": 700,
    "height": 700,
    "title": "Iowa Spaceflight",
    "titlefont": {"size": 20, "color": "#FFCD00"},
    "hovermode": "closest",
    "xaxis": {
        "title": "X (AU)",
        "range": [-40, 40],
    },
    "yaxis": {
        "title": "Y (AU)",
        "range": [-40, 40],
    },
    "annotations": [
        # Annotation for local maximum (x = -1)
        {
            "text": "Earth",
            "font": {
                "size": 20
            },
            "x": planet_coords[0]['x'][2],
            "y": planet_coords[0]['y'][2],
        },
    ]
}

stylekit = {
  "color_primary": "#FFCD00",
  "color_secondary": "#00664F",
  "color_background_dark": "#000000",
  "color_paper_dark": "#222222",
}

text = "Original text"
dt = datetime.datetime.now()
active_sc_dictionary = celestrak.generate_active_dict() ##TODO connect to celestrak.py
# Remove NORAD_CAT_ID column
active_sc_dictionary.pop('NORAD_CAT_ID')
# Clean up dictionary column names for display
active_sc_dictionary = {k.replace('_', ' '): v for k, v in active_sc_dictionary.items()}
# Set to capitalize first letter of each word
active_sc_dictionary = {k.title(): v for k, v in active_sc_dictionary.items()}

#make a copy of the dictionary with only dates in the future
#active_sc_dictionary_for_display = {k: v for k, v in active_sc_dictionary.items() if v > dt}

page = """

# **Iowa Spaceflight**{: .color-primary}

<|{dt}|date|>

## **Spacecraft with UIowa instruments currently in space**{: .color-primary}

<|{active_sc_dictionary}|table|>

<|{object_coords}|chart|mode=markers|marker={markers}|layout={layout}|>

Find more information at [Iowa Spaceflight](https://physics.uiowa.edu/history/spaceflight-instruments)

<|{content}|image|width=700px|hover_text=UIowa Instruments in Space|>

"""
Gui(page).run(title="Iowa Spaceflight", use_reloader=True, theme=my_theme, stylekit=stylekit)
