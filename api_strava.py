import requests
import streamlit as st
import urllib3
import pandas as pd
from pandas import json_normalize


urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

auth_url = "https://www.strava.com/oauth/token"
activites_url = "https://www.strava.com/api/v3/athlete/activities"

client_id = st.secrets['client_id']
client_secret = st.secrets['client_secret']
refresh_token = st.secrets['refresh_token']

payload = {
    'client_id': client_id,
    'client_secret': client_secret,
    # 'refresh_token': '782dbf689a067a29c8c0b71806e36b230767bbc8',
    'refresh_token': refresh_token,
    'grant_type': "refresh_token",
    'f': 'json'
}

# print("Requesting Token...\n")
# res = requests.post(auth_url, data=payload, verify=False)
# print(res.json())
# access_token = res.json()['access_token']
# print("Access Token = {}\n".format(access_token))



# print(my_dataset)

def get_auth_token(payload, auth_url):
    res = requests.post(auth_url, data=payload, verify=False)
    return res.json()['access_token']


def get_data():
    header = {'Authorization': 'Bearer ' + get_auth_token(payload, auth_url)}
    param = {'per_page': 200, 'page': 1}
    dataset = requests.get(activites_url, headers=header, params=param).json()
    return json_normalize(dataset)


frame = get_data()
print(frame.shape)
print(frame.head())

# data = json_normalize(my_dataset)
# print(data.columns)
# print(data.shape)

# print(data.head())
# print(type(data))