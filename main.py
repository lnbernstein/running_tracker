import datetime
import streamlit as st
import numpy as np
import pandas as pd
import streamlit.components.v1 as components
import api_strava

df = api_strava.get_data()
pd.options.display.float_format = "{:,.2f}".format

print(df.shape)

# df.to_csv('strava_data.csv')


# weekly_mileage = 10
runs_completed = 1
runs_of_week = 4
bpm = 172
bpm_change = 4

df.start_date = pd.to_datetime(df.start_date)
df['week'] = df.start_date.dt.isocalendar().week
df['year'] = df.start_date.dt.isocalendar().year
df['distance_miles'] = df.distance / 1609

def weekly_mileage():
    year, week_num, day_of_week = datetime.date.today().isocalendar()
    this_week = df[df['week'] == week_num]
    return this_week['distance_miles'].sum()

# def generate_run(weekly_mileage, runs_completed, runs_of_week):
#     miles_per_run = weekly_mileage/runs_of_week
#     if(runs_completed != runs_of_week-1):
#         return miles_per_run
#     else:
#         return miles_per_run*1.75


# chart_data = pd.DataFrame(
#      np.random.randn(20, 3),
#      columns=['a', 'b', 'c'])





st.markdown("<h1 style='text-align: left;'>Becoming a Better Athlete</h1>", unsafe_allow_html=True)
st.markdown("<p style='text-align: left;'>Following the 10% rule, this application will automatically generate a run based on prior training</p>", unsafe_allow_html=True)


col1, col2, col3 = st.columns(3)

with col1:
    st.write(' ')

with col2:
    # st.metric("    Today's Mileage", generate_run(weekly_mileage, runs_completed, runs_of_week))
    st.write('hi')

with col3:
    st.write(' ')


col1, col2, col3 = st.columns(3)

with col1:
    st.metric('Weekly Mileage', round(weekly_mileage(),2), 2)

with col2:
    st.metric('Average Heart Rate', int(df.average_heartrate.mean()), int(df.average_heartrate.diff()[1]))

with col3:
    st.metric('Average Pace', round(df.average_speed.mean(),2), int(df.average_speed.diff()[1]))


# st.line_chart(chart_data)
# components.iframe("https://calendar.google.com/calendar/embed?src=c_mst8mkd08jsbukco439oht7gr8%40group.calendar.google.com&ctz=America%2FNew_York",
#                     width=800, height=500, scrolling=True)






