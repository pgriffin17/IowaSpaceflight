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

data = [
    { "x": [1, 2, 3, 4], "y": [10, 11, 12, 13] },
    { "x": [1, 2, 3, 4], "y": [11, 12, 13, 14] },
    { "x": [1, 2, 3, 4], "y": [12, 13, 14, 15] }
]

markers = [
]

stylekit = {
  "color_primary": "#FFCD00",
  "color_secondary": "#00664F",
  "color_background_dark": "#000000",
  "color_paper_dark": "#222222",
}

#make a copy of the dictionary with only dates in the future
#active_sc_dictionary_for_display = {k: v for k, v in active_sc_dictionary.items() if v > dt}

page = """

# **Iowa Spaceflight**{: .color-primary}

## **Spacecraft with UIowa instruments currently in space**{: .color-primary}

<|{data}|chart|mode=markers|marker={markers}|>

Find more information at [Iowa Spaceflight](https://physics.uiowa.edu/history/spaceflight-instruments)

<|{content}|image|width=700px|hover_text=UIowa Instruments in Space|>

"""
Gui(page).run(title="Iowa Spaceflight", use_reloader=True, theme=my_theme, stylekit=stylekit)
