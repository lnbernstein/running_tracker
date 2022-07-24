import datetime
import streamlit as st
import numpy as np
import pandas as pd
import streamlit.components.v1 as components
import api_strava
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.express as px
sns.set(style="whitegrid", palette="pastel")

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
df['rank'] = df.start_date.rank()-1
df['moving_time_minutes'] = df.moving_time/60

conditions = [
    (df['moving_time_minutes'] <= 20),
    (df['moving_time_minutes'] > 20) & (df['moving_time_minutes'] <= 40),
    # (df['moving_time_minutes'] > 40) & (df['moving_time_minutes'] <= 60)
]

choices = ['short (<= 20 minutes)', 'medium (21 to 40 minutes)']
df['length_cut'] = np.select(conditions, choices, default='long (> 40 minutes)')

#  correct because  year query used, not checked yet
def weekly_mileage():
    year, week_num, day_of_week = datetime.date.today().isocalendar()
    this_week = df[(df['week'] == week_num) & (df['year'] == year)]
    return this_week['distance_miles'].sum()

def generate_run(weekly_mileage, runs_completed, runs_of_week):
    miles_per_run = weekly_mileage()/runs_of_week
    if(runs_completed != runs_of_week-1):
        return miles_per_run
    else:
        return miles_per_run*1.75



st.markdown("<h1 style='text-align: left;'>Becoming a Better Athlete</h1>", unsafe_allow_html=True)
st.markdown("<p style='text-align: left;'>Following the 10% rule, this application will automatically generate a run based on prior training</p>", unsafe_allow_html=True)


col1, col2, col3 = st.columns(3)

with col1:
    st.write(' ')

with col2:
    st.metric("    Today's Mileage", generate_run(weekly_mileage, runs_completed, runs_of_week))
    # st.write('hi')

with col3:
    st.write(' ')


col1, col2, col3 = st.columns(3)

with col1:
    st.metric('Weekly Mileage', round(weekly_mileage(),2), 2)

with col2:
    st.metric('Average Heart Rate', int(df.average_heartrate.mean()), int(df.average_heartrate.diff()[1]))

with col3:
    st.metric('Average Pace', round(df.average_speed.mean(),2), int(df.average_speed.diff()[1]))


fig = plt.figure(figsize=(10,4))
sns.lineplot(x='rank', y='average_heartrate', data=df).set(title='Average Heartrate over Time', xlabel='Time')
st.pyplot(fig=fig)

fig1 = px.line(df, x='rank', y='average_heartrate', width=800, height=400, title='Average Heartrate over Time')
fig1.update_layout(title_x=0.5, xaxis_title="Time")
st.plotly_chart(figure_or_data=fig1)

fig2 = px.histogram(df, x='length_cut', color='length_cut', width=800, height=400, 
                        category_orders={'length_cut':['short (<= 20 minutes)', 'medium (21 to 40 minutes)', 'long (> 40 minutes)']})
fig2.update_layout(title='Run Lengths Histogram', title_x=0.5, xaxis_title='Distribution of Run Lengths', )
st.plotly_chart(figure_or_data=fig2)

fig3 = px.histogram(df, x='moving_time_minutes')
st.plotly_chart(figure_or_data=fig3)



# components.iframe("https://calendar.google.com/calendar/embed?src=c_mst8mkd08jsbukco439oht7gr8%40group.calendar.google.com&ctz=America%2FNew_York",
#                     width=800, height=500, scrolling=True)






