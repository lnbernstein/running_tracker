import datetime
from PIL import Image
import streamlit as st
import numpy as np
import pandas as pd
import streamlit.components.v1 as components
import api_strava
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

START_NUM_RUNS = 4 #constant
base_mileage = 13 # constant

df.start_date = pd.to_datetime(df.start_date)
df['week'] = df.start_date.dt.isocalendar().week
df['year'] = df.start_date.dt.isocalendar().year
df['distance_miles'] = df.distance / 1609
df['rank'] = df.start_date.rank()-1
df['moving_time_minutes'] = df.moving_time/60

conditions = [
    (df['moving_time_minutes'] <= 20),
    (df['moving_time_minutes'] > 20) & (df['moving_time_minutes'] <= 40),
]

choices = ['short (<= 20 minutes)', 'medium (21 to 40 minutes)']
df['length_cut'] = np.select(conditions, choices, default='long (> 40 minutes)')


def create_week_df():
    '''Generates dataframe of runs for current week'''
    year, week_num, day_of_week = datetime.date.today().isocalendar()
    return df[(df['week'] == week_num) & (df['year'] == year)]

def create_last_week_df():
    '''Generates dataframe of runs from one week in the past'''
    year, week_num, day_of_week = datetime.date.today().isocalendar()
    return df[(df['week'] == week_num-1) & (df['year'] == year)]

def weekly_mileage():
    '''Calculate mileage run this week'''
    this_week = create_week_df()
    return this_week['distance_miles'].sum()

def last_weeks_mileage():
    '''Calculate mileage run last week'''
    last_week = create_last_week_df()
    return last_week['distance_miles'].sum()

def runs_completed():
    '''Calculate number of runs this week'''
    this_week = create_week_df()
    return this_week.name.count()

def generate_run():
    '''Using a week one mileage of 13 miles, generates daily run. Long run is defined as 30% of weekly mileage'''
    less_long_mileage = base_mileage*.7
    base_run = less_long_mileage/(START_NUM_RUNS-1)
    this_week = create_week_df()
    num_runs_completed = this_week.shape[0] + 1
    if(num_runs_completed <= START_NUM_RUNS-1):
        return base_run
    else:
        return base_mileage*.3
    

# streamlit section


# sidebar section

st.sidebar.write('Hi! My name is Luke Bernstein and I am a Junior at NYU studying Finance and Computer Science.')

st.sidebar.write('Add me: www.linkedin.com/in/luke-bernstein')
st.sidebar.write('Email me @ lnb337@stern.nyu.edu')

image = Image.open('bernstein_headshot.jpeg')
st.sidebar.image(image)

st.sidebar.write('Check out my [resume!](https://drive.google.com/file/d/1VvNS4UlRF0X-LvJ3iG0wQHrq_CkIoHik/view?usp=sharing)')

st.sidebar.markdown("[![Github](GitHub-Mark-64px.png)](https://github.com/lnbernstein/running_tracker)")




# rest of page


st.markdown("<h1 style='text-align: left;'>Becoming a Better Runner</h1>", unsafe_allow_html=True)
st.markdown("<p style='text-align: left;'>Following the 10% rule, this application will automatically generate a run based on prior training</p>", unsafe_allow_html=True)


topcol1, topcol2 = st.columns(2)
with topcol1:
    st.write('Training Start Date: August 15, 2022')
with topcol2:
    st.write('Base Week Mileage: ', base_mileage,  'miles')



col1, col2, col3 = st.columns(3)

with col1:
    st.metric('Runs Completed this week', runs_completed())

with col2:
    st.metric("Today's Mileage", round(generate_run(), 2))

with col3:
    st.write(' ')


col1, col2, col3 = st.columns(3)

with col1:
    st.metric('Weekly Mileage', round(weekly_mileage(),2), round(last_weeks_mileage(), 2))

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


# upcoming calendar feature

# components.iframe("https://calendar.google.com/calendar/embed?src=c_mst8mkd08jsbukco439oht7gr8%40group.calendar.google.com&ctz=America%2FNew_York",
#                     width=800, height=500, scrolling=True)






