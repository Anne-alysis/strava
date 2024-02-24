import matplotlib.pyplot as plt
import pandas as pd
import requests
from lets_plot import *
import numpy as np
import pandas as pd

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
df['date'] = pd.to_datetime(pd.to_datetime(df['start_date_local']).dt.date)

g = ggplot(df, aes(x='suffer_score')) + theme_light() + geom_histogram(aes(fill='sport_type'))
g.show()

heart_rate_df = pd.melt(df[['id', 'sport_type', 'max_heartrate', 'average_heartrate']],
                        id_vars=['id', 'sport_type'], var_name='rate_type', value_name='heart_rate').reset_index()

df.max_heartrate.hist(bins=30)
plt.show()
df.average_heartrate.hist(bins=30)
plt.show()

g = ggplot(heart_rate_df, aes(x='heart_rate')) + geom_histogram(aes(fill='sport_type')) + \
    facet_wrap(facets='rate_type') + theme_light()
g.show()

#### ELLIPTICAL FOCUS 

elliptical_df = df[(df.type == 'Elliptical') & (df.name != 'Warmup')]
elliptical_df['flavor'] = np.where(elliptical_df.name.isin(['Tempo', 'Intervals']), elliptical_df.name, 'Recovery')

elliptical_df = elliptical_df[['id', 'date', 'flavor', 'average_heartrate', 'max_heartrate', 'suffer_score']]

melt_df = pd.melt(elliptical_df, ['id', 'date', 'flavor'], var_name = 'type')

g = ggplot(elliptical_df, aes(x='date', y='suffer_score')) + facet_wrap(facets='flavor') + \
        geom_point()+theme_light() + scale_x_datetime(format="%b %y")
g.show()

g = ggplot(melt_df, aes(x='date', y='value')) + facet_wrap(facets='flavor') + \
        geom_point(aes(color='type'))+theme_light() + scale_x_datetime(format="%b %y")
g.show()


# suffer score vs max and avg heartrate
partial_melt_df = pd.melt(elliptical_df, ['id', 'date', 'flavor', 'suffer_score'], var_name = 'type', value_name='heart_rate')

g = ggplot(partial_melt_df, aes(x='heart_rate', y='suffer_score')) + facet_wrap(facets=['flavor', 'type'], scales='free', ncol=2) + \
        geom_point(aes(color='type'))+theme_light()
g.show()


g = ggplot(partial_melt_df[(partial_melt_df.flavor != 'Recovery') & (partial_melt_df.type == 'average_heartrate')], aes(x='value', y='suffer_score')) +\
        geom_point(aes(color='flavor'))+theme_light()
g.show()