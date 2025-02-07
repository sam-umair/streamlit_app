#import libraries
import streamlit as st
import plotly.express as px
import pandas as pd

#import dateset
st.title('Plotly and streamlit to make an app')
df = px.data.gapminder()
st.write(df)
st.write(df.head())
st.write(df.columns)

#summary stats
st.write(df.describe())

#data management
year_option = df['year'].unique().tolist()
year = st.selectbox('Select year', year_option,0)
#df = df[df['year'] == year]

#plotting
fig = px.scatter(df, x='gdpPercap', y='lifeExp', size='pop', color='continent', hover_name='country', log_x=True, 
                 size_max=55, range_x=[100,100000], range_y=[20,90],
                 animation_frame='year', animation_group='country')
fig.update_layout(width=1000, height=600)
st.write(fig) 
