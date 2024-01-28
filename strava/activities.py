import pandas as pd
import requests
from lets_plot import *

from strava.auth.authorize import ACTIVITY_HEADERS

LetsPlot.setup_html()
URL = f"https://www.strava.com/api/v3/athlete/activities?per_page=200&page=1"

activities_response = requests.get(URL, headers=ACTIVITY_HEADERS)
activities = activities_response.json()

df = pd.DataFrame(activities)

cols = ['id', 'name',
        'type', 'sport_type',
        'start_date_local',
        'distance',  # meters
        'moving_time', 'elapsed_time',  # seconds
        'average_speed', 'max_speed',  # m/s
        'average_cadence',
        'average_heartrate', 'max_heartrate',  # bps
        'total_elevation_gain', 'elev_high', 'elev_low',  # m
        'suffer_score'
        # 'average_watts', 'max_watts', 'weighted_average_watts', 'kilojoules'
        ]

df = df[cols]

g = ggplot(df, aes(x='suffer_score')) + theme_light() + geom_histogram(aes(fill='sport_type'))
g.show()
