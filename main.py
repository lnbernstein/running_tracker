from requests import api
import streamlit as st
import numpy as np
import pandas as pd
import streamlit.components.v1 as components
import api_strava

df = api_strava.get_data()
print(df.shape)

df.to_csv('strava_data.csv')


# weekly_mileage = 10
# runs_completed = 1
# runs_of_week = 4

# def generate_run(weekly_mileage, runs_completed, runs_of_week):
#     miles_per_run = weekly_mileage/runs_of_week
#     if(runs_completed != runs_of_week-1):
#         return miles_per_run
#     else:
#         return miles_per_run*1.75


# chart_data = pd.DataFrame(
#      np.random.randn(20, 3),
#      columns=['a', 'b', 'c'])

# bpm = 172
# bpm_change = 4



# st.markdown("<h1 style='text-align: left;'>Becoming a Better Athlete</h1>", unsafe_allow_html=True)
# st.markdown("<p style='text-align: left;'>Following the 10% rule, this application will automatically generate a run based on prior training</p>", unsafe_allow_html=True)


# col1, col2, col3 = st.columns(3)

# with col1:
#     st.write(' ')

# with col2:
#     st.metric("    Today's Mileage", generate_run(weekly_mileage, runs_completed, runs_of_week))

# with col3:
#     st.write(' ')


# col1, col2, col3 = st.columns(3)

# with col1:
#     st.metric('Weekly Mileage', 42, 2)

# with col2:
#     st.metric('Average Heart Rate', bpm, bpm_change)

# with col3:
#     st.metric('Average Pace', bpm, bpm_change)


# st.line_chart(chart_data)
# components.iframe("https://calendar.google.com/calendar/embed?src=c_mst8mkd08jsbukco439oht7gr8%40group.calendar.google.com&ctz=America%2FNew_York",
#                     width=800, height=500, scrolling=True)