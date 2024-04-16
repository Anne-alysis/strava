import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from lets_plot import *

from strava.data import get_data

# https://www.strava.com/settings/api

LetsPlot.setup_html()
df = get_data()

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

melt_df = pd.melt(elliptical_df, ['id', 'date', 'flavor'], var_name='type')

g = ggplot(elliptical_df, aes(x='date', y='suffer_score')) + facet_wrap(facets='flavor') + \
    geom_point() + theme_light() + scale_x_datetime(format="%b %y")
g.show()

g = ggplot(melt_df, aes(x='date', y='value')) + facet_wrap(facets='flavor') + \
    geom_point(aes(color='type')) + theme_light() + scale_x_datetime(format="%b %y")
g.show()

# suffer score vs max and avg heartrate
partial_melt_df = pd.melt(elliptical_df, ['id', 'date', 'flavor', 'suffer_score'], var_name='type',
                          value_name='heart_rate')

g = ggplot(partial_melt_df, aes(x='heart_rate', y='suffer_score')) + facet_wrap(facets=['flavor', 'type'],
                                                                                scales='free', ncol=2) + \
    geom_point(aes(color='type')) + theme_light()
g.show()

g = ggplot(partial_melt_df[(partial_melt_df.flavor != 'Recovery') & (partial_melt_df.type == 'average_heartrate')],
           aes(x='value', y='suffer_score')) + \
    geom_point(aes(color='flavor')) + theme_light()
g.show()

## runs
run_df = df[df.type == 'Run']

run_df['avg_min_mile'] = 1 / (run_df['average_speed'] * 0.0372823)
run_df['Location'] = run_df['name'].apply(lambda x: x.split(':')[0])
run_df['Distance (miles)'] = run_df['distance'] * 0.000621371
run_df = run_df[run_df.Location != 'Cool down']

g = (ggplot(run_df, aes(x='date', y='avg_min_mile')) +
     geom_point(aes(fill='Location', size='Distance (miles)'), col='black', shape=21) + \
     theme_light() + ylab('Pace (min / mile)'))
g.show()
