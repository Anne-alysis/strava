import matplotlib.pyplot as plt
import pandas as pd
import requests
from lets_plot import *

from strava.auth.authorize import ACTIVITY_HEADERS
# https://www.strava.com/settings/api

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
df.to_csv("./data/activities.csv", index=False)

g = ggplot(df, aes(x='suffer_score')) + theme_light() + geom_histogram(aes(fill='sport_type'))
g.show()

heart_rate_df = pd.melt(df[['id','sport_type', 'max_heartrate', 'average_heartrate']],
                        id_vars=['id','sport_type'], var_name='rate_type', value_name='heart_rate').reset_index()

df.max_heartrate.hist(bins=30)
plt.show()
df.average_heartrate.hist(bins=30)
plt.show()

g = ggplot(heart_rate_df, aes(x='heart_rate')) + geom_histogram(aes(fill='sport_type')) + \
        facet_wrap(facets='rate_type') + theme_light()
g.show()