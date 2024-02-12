import datetime

import numpy as np
import pandas as pd
import requests
from lets_plot import *

from strava.auth.authorize import PROFILE_HEADERS

LetsPlot.setup_html()

"""
Comparison of heart rate zones from my calculation, a Garmin watch, and Strava.
"""

ZONE_NAMES = ['Warm Up', 'Easy', 'Aerobic', 'Threshold', 'Maximum']

age = (datetime.date.today() - datetime.date.fromisoformat('1980-10-11')).days / 365
max_heart_rate = 220 - age


## heart rate calculation
def get_anne_heart_rate_zones() -> pd.DataFrame:
    """
    Calculation from https://health.clevelandclinic.org/exercise-heart-rate-zones-explained
    """
    resting_heart_rate = 49
    heart_rate_reserve = max_heart_rate - resting_heart_rate
    zone_max = np.round(np.arange(6, 11) / 10 * heart_rate_reserve + resting_heart_rate)
    zone_min = np.concatenate([np.array([0]), zone_max[:-1] - 1])
    return pd.DataFrame({'Anne_Min': zone_min, 'Anne_Max': zone_max, 'Position': range(1, 6)})


def get_strava_heart_rate_zones() -> pd.DataFrame:
    zones = requests.get("https://www.strava.com/api/v3/athlete/zones", headers=PROFILE_HEADERS)

    zones_df = pd.DataFrame(zones.json()['heart_rate']['zones'])
    zones_df['name'] = ZONE_NAMES
    zones_df['Position'] = range(1, 6)
    zones_df.rename(columns={'min': 'Strava_Min', 'max': 'Strava_Max'}, inplace=True)
    zones_df.at[4, 'Strava_Max'] = 190
    return zones_df


strava_df = get_strava_heart_rate_zones()
garmin_df = pd.DataFrame({'Garmin_Min': [0, 109, 127, 145, 162], 'Garmin_Max': [108, 126, 144, 162, max_heart_rate],
                          'Position': range(1, 6)})

zones_df = pd.merge(strava_df, garmin_df, on='Position')
zones_df = pd.merge(zones_df, get_anne_heart_rate_zones(), on='Position')

zones_df = zones_df[
    ['Position', 'name', 'Strava_Min', 'Garmin_Min', 'Anne_Min', 'Strava_Max', 'Garmin_Max', 'Anne_Max']]
melted_zones_df = pd.melt(zones_df, id_vars=['Position', 'name'], var_name='type_range', value_name='heart_rate')
melted_zones_df[['App', 'range_type']] = melted_zones_df['type_range'].str.split('_', expand=True)
melted_zones_df.drop(columns='type_range', inplace=True)

# separating out min/max
g = ggplot(melted_zones_df, aes(x='Position', y='heart_rate')) + theme_light() + \
    geom_line(aes(color='App'), size=3, tooltips=layer_tooltips().title('@App')) + facet_wrap(
    facets='range_type') + ylab("Heart Rate (bps)") + \
    scale_color_brewer(palette='Greens')

g.show()

g = ggplot(melted_zones_df[melted_zones_df.range_type == 'Max'], aes(x='Position', y='heart_rate')) + theme_light() + \
    geom_line(aes(color='App'), size=3, tooltips=layer_tooltips().title('@App')) + facet_wrap(
    facets='range_type') + ylab("Heart Rate (bps)") + \
    scale_color_brewer(palette='Greens')

g.show()

# ribbon plots
spread_zones_df = melted_zones_df.pivot_table(index=['Position', 'name', 'App'], columns='range_type',
                                              values='heart_rate').reset_index()

r = ggplot(spread_zones_df, aes(x='Position')) + theme_light() + \
    geom_ribbon(aes(fill='App', ymin='Min', ymax='Max'), alpha=0.3, tooltips=layer_tooltips().title('@App')) + \
    ylab("Heart Rate (bps)") + \
    scale_color_brewer(palette='Greens')

r.show()

# Removing Strava for clarity
r = ggplot(spread_zones_df[spread_zones_df.App != 'Strava'], aes(x='Position')) + theme_light() + \
    geom_ribbon(aes(fill='App', ymin='Min', ymax='Max'), alpha=0.3, tooltips=layer_tooltips().title('@App')) + \
    ylab("Heart Rate (bps)") + \
    scale_color_brewer(palette='Greens')

r.show()
