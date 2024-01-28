import requests

from strava.auth.env_handler import env_variables

AUTH_ENDPOINT = "https://www.strava.com/oauth/token"


def get_access_token_via_refresh():
    # these params needs to be passed to get access
    # token used for retrieveing actual data
    payload = {
        'client_id': env_variables['CLIENT_ID'],
        'client_secret': env_variables['CLIENT_SECRET'],
        'refresh_token': env_variables['REFRESH_TOKEN'],
        'grant_type': "refresh_token",
        'f': 'json'
    }
    res = requests.post(AUTH_ENDPOINT, data=payload, verify=False)
    access_token = res.json()['access_token']
    return access_token


def get_access_token_via_code():
    # these params needs to be passed to get access
    # token used for retrieveing actual data
    payload = {
        'client_id': env_variables['CLIENT_ID'],
        'client_secret': env_variables['CLIENT_SECRET'],
        'code': env_variables['CODE'],
        'grant_type': "authorization_code",
        'f': 'json'
    }
    res = requests.post(AUTH_ENDPOINT, data=payload, verify=False)
    access_token = res.json()['access_token']
    return access_token


ACCESS_TOKEN = env_variables['ACCESS_TOKEN']  # get_access_token_via_code()
ACTIVITY_HEADERS = {'Authorization': f'Authorization: Bearer {ACCESS_TOKEN}'}
PROFILE_HEADERS = {'Authorization': f'Authorization: Bearer {env_variables["PROFILE_CODE"]}'}
