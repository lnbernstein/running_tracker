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

st.sidebar.markdown("[![Github](data:image/png;base64,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)](https://github.com/lnbernstein/running_tracker)")




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






