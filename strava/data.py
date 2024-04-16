import pandas as pd
import requests

from strava.auth.authorize import ACTIVITY_HEADERS

# https://www.strava.com/settings/api

URL = f"https://www.strava.com/api/v3/athlete/activities?per_page=200&page"


def get_data() -> pd.DataFrame:
    activities_data = []
    for page in range(1, 1000):
        print(f"Page: {page}")
        activities_response = requests.get(f"{URL}={page}", headers=ACTIVITY_HEADERS)
        activities_list = activities_response.json()

        if activities_response.status_code != 200:
            raise Exception(f"Bad response: {activities_response.status_code}")
        if len(activities_list) == 0:
            break
        activities_data.append(pd.DataFrame(activities_list))

    df = pd.concat(activities_data)

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

    return df
