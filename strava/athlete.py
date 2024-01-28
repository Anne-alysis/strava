import requests
from lets_plot import *

from strava.auth.authorize import PROFILE_HEADERS

LetsPlot.setup_html()

athlete_response = requests.get("https://www.strava.com/api/v3/athlete", headers=PROFILE_HEADERS)
athlete = athlete_response.json()
