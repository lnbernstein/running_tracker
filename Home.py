import datetime
import this
import streamlit as st
import numpy as np
import pandas as pd
import streamlit.components.v1 as components
import api_strava
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.express as px
sns.set(style="whitegrid", palette="pastel")
st.set_page_config(page_title="Running Tracker", page_icon="📈", layout='centered')


# pandas section
@st.experimental_memo
def get_data() -> pd.DataFrame():
    return api_strava.get_data()


df = get_data()
pd.options.display.float_format = "{:,.2f}".format

BASE_MILEAGE = 10
START_NUM_RUNS = 5

# df.to_csv('strava_data.csv')

runs_rec = 5
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


def create_week_df():
    year, week_num, day_of_week = datetime.date.today().isocalendar()
    return df[(df['week'] == week_num) & (df['year'] == year)]

#  correct because  year query used, not checked yet
def weekly_mileage():
    this_week = create_week_df()
    return this_week['distance_miles'].sum()

def runs_completed():
    this_week = create_week_df()
    return this_week.name.count()


def generate_run():
    base_mileage = 10
    less_long_mileage = base_mileage*.7
    base_run = less_long_mileage/(START_NUM_RUNS-1)
    this_week = create_week_df()
    num_runs_completed = this_week.shape[0] + 1
    if(num_runs_completed <= START_NUM_RUNS-1):
        return base_run
    else:
        return base_run*1.25
    


# def generate_run(runs_rec):
#     long_run = BASE_MILEAGE*.25
#     weekly_mileage = 2
#     mileage_left = BASE_MILEAGE - weekly_mileage
#     runs_left = START_NUM_RUNS - runs_completed() 
#     # miles_per_run = weekly_mileage() /runs_completed()

#     if(runs_left >= 2):
#         return mileage_left/runs_left
    
#     if(runs_completed() != START_NUM_RUNS):
        
#     else:
#         return miles_per_run*1.75


# streamlit section



# st.set_page_config(layout='wide')

# with st.sidebar:
#     add_radio = st.radio(
#         "Choose a shipping method",
#         ("Standard (5-15 days)", "Express (2-5 days)")
#     )

st.sidebar.success("Running Tracker")


st.markdown("<h1 style='text-align: left;'>Becoming a Better Athlete</h1>", unsafe_allow_html=True)
st.markdown("<p style='text-align: left;'>Following the 10% rule, this application will automatically generate a run based on prior training</p>", unsafe_allow_html=True)



col1, col2, col3 = st.columns(3)

with col1:
    st.write(' ')

with col2:
    st.metric("    Today's Mileage", generate_run())
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

st.subheader('Performance Metrics:')

week_grouper = df.groupby(pd.Grouper(key='start_date', freq='1W')).mean()
week_grouper.average_heartrate = week_grouper.average_heartrate.fillna(method='ffill')

fig4 = px.line(week_grouper, x=week_grouper.index, y='average_heartrate', title='Average Heartrate over Time')
fig4.update_xaxes(nticks=20, tick0="2020-03-22")
fig4.update_traces(line_color='#FF9F33')

st.plotly_chart(figure_or_data=fig4)


fig2 = px.histogram(df, x='length_cut', color='length_cut', 
                        category_orders={'length_cut':['short (<= 20 minutes)', 'medium (21 to 40 minutes)', 'long (> 40 minutes)']})
fig2.update_layout(title='Run Lengths Histogram', title_x=0.5, xaxis_title='Distribution of Run Lengths', )
st.plotly_chart(figure_or_data=fig2)

fig3 = px.histogram(df, x='moving_time_minutes', color_discrete_sequence=['#FF9F33'])
st.plotly_chart(figure_or_data=fig3)



# components.iframe("https://calendar.google.com/calendar/embed?src=c_mst8mkd08jsbukco439oht7gr8%40group.calendar.google.com&ctz=America%2FNew_York",
#                     width=800, height=500, scrolling=True)






