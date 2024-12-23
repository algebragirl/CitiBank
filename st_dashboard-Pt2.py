############################################################### CITIBIKE DASHBOARD
###########################################################################

import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
from plotly.subplots import make_subplots
import plotly.graph_objects as go
from streamlit_keplergl import keplergl_static
from keplergl import KeplerGl
from datetime import datetime as dt
from numerizer import numerize
from PIL import Image


############################################################### Initial settings for the dashboard
###################################################################################################

st.set_page_config(page_title ='CitiBike Strategy Dashboard', layout='wide')
st.title("CitiBike Strategy Dashboard")

# Define side bar
st.sidebar.title("Variable/Section?")
page = st.sidebar.selectbox('Select any variable/section of the analysis',
                            ['Intro page','Temperature and bike usage',
                             'Most popular start stations',
                             'Interactive map with aggregated bike trips','Recommendations'])

          
####################################################### Import data
################################################################################################
######

df=pd.read_csv('reduced_data_to_plot_7.csv', index_col = 0)
df_dual_axis = pd.read_csv("dual_axis.csv", index_col = 0)
top20 = pd.read_csv('top20.csv',index_col=0)


#####################################################  DEFINE THE PAGES
######################################################################################

### Intro page

if page == "Intro page":
    st.markdown("### This dashboard provides helpful insights about the obstacles that CitiBike currently faces as it is considering expanding its bike supply in New York.")
    st.markdown("#### CitiBike has customers complaining about not being able to obtain bikes at certain times, and this analysis looks at the possible reasons behind this bike shortage. This dashboard contains an introduction page, an insights & analysis section where I analyze 3 variables that affect bike demand, and lastly a recommendations page. I dedicated 1 page for each of the variables that I analyzed and each has an accompanying visualization.")
    st.markdown("##### -Introduction page")
    st.markdown("##### -Insights and Analysis")
    st.markdown("- Most popular start stations")
    st.markdown("- Temperature and bike usage")
    st.markdown("- Interactive map with aggregated bike trips")
    st.markdown("##### -Conclusions and Recommendations")
    st.markdown("#### The dropdown menu in the upper left-hand side of the page will allow you to select the different sections of our analysis.")

###
    myimage = st.image("OIP.jfif", width=400)
 

### Create the dual axis line chart page ###

elif page == 'Temperature and bike usage':

    fig_2 = make_subplots(specs = [[{"secondary_y": True}]])


    fig_2.add_trace(
    go.Scatter(x = df_dual_axis['date'], y = df_dual_axis['bike_rides_daily'], name = 'Daily bike rides',    
    marker={'color':df_dual_axis['bike_rides_daily'],'color':'blue'}),
    secondary_y = False
    )

    fig_2.add_trace(

    go.Scatter(x=df_dual_axis['date'], y = df_dual_axis['avgTemp'], name = 'Daily temperature', 
    marker={'color':df_dual_axis['avgTemp'],'color':'red'}),
    secondary_y=True
    )


    fig_2.update_layout(
        title = 'Daily bike trips and temperatures in 2022',
         height = 400
    )


    st.plotly_chart(fig_2, use_container_width=True)

    st.markdown("There is an obvious correlation between the temperature and the frequency of the daily bike trips. As the temperature increases, so does the bike usage. This insight indicates that the bike shortage problem may only occur in the the warmer months, which is approximately from May to October.")


  ### Most popular stations page

  # Create the season variable

elif page == 'Most popular start stations':
    # Create the filter on the side bar
    with st.sidebar:
        season_filter = st.multiselect(label= 'Select the season', options=df['season'].unique(), default=df['season'].unique())
    df1 = df.query('season == @season_filter')

    #define the total rides
    total_rides = int(df1['ride_id'].count())
    st.markdown(f"#### total bike rides: {total_rides}")

################################################################# DEFINE THE CHARTS
##############################################################################################



## Bar chart

    df1['value'] = 1
    df_groupby_bar = df1.groupby('start_station_name', as_index = False).agg({'value':'sum'})
    top20 = df_groupby_bar.nlargest(20,'value')
    fig = go.Figure(go.Bar(x = top20['start_station_name'], y = top20['value'], marker={'color':top20['value'],'colorscale':'Blues'}))
    fig.update_layout(
        title = 'Top 20 most popular bike stations in New York',
        xaxis_title = 'Start stations',
        yaxis_title = 'Sum of trips',
        width = 900, height = 600
    )
    st.plotly_chart(fig, use_container_width=True)
    st.markdown("From the bar chart we can see that some start stations are more popular than others. The top 3 are W 21st Street/6th Avenue, West Street/Chambers Street and 1st Ave/E 62nd Street. In terms of the total number of bike trips, the station ranked #20 is about 38% less than the most popular station. We can cross reference these findings with the interactive map - which is another option in the dropdown filter.")


elif page == 'Interactive map with aggregated bike trips':

    ### Create the map ###

    st.write("Interactive map showing aggregated bike trips over New York")
                      
    ### Add the map ###

    path_to_html = "CitiBike Bike Trips Aggregated.html"

    # Read file and keep in variable
    with open(path_to_html,'r') as f:
        html_data = f.read()

    ## Show in webpage
    st.header("Aggregated Bike Trips in New York")
    st.components.v1.html(html_data,height=1000)
    st.markdown("#### Using the filter on the left-hand side of the map we can check whether the most popular start stations also appear in the most popular trips.")
    st.markdown("The 3 most popular start stations are W 21st Street/6th Avenue, West Street/Chambers Street and 1st Ave/E 68th Street.")
    st.markdown("With the aggregated bike trips filter enabled, we can see that even though West Street/Chambers Street is a popular start station, it doesn't account for the top 4 most commonly taken trips.")
    st.markdown("The most common routes (>900) are between W 21 St/6th Ave and W 22 St/10th Ave (933, Chelsea); Norfolk St/Broome St and Henry St/Grand St (989, Lower East Side); 1st Ave/E 62 St and 1st Ave/E 68 St (1200, Lenox Hill); and W 21 St/6th Ave and 9th Ave/W 22 St (1261, Chelsea).")
    st.markdown("When you look at the routes with more than 700 daily bike rides, a lot of those routes are along the Hudson River and one route starts at Central Park S/6 Ave.")

                
else:

    st.header("Conclusions and Recommendations")
  
    myimage_2=st.image("Citibike_NYC_render_01.jpg", width=400)
    st.markdown("### Our analysis has shown that CitiBike may consider the following recommendations when expanding their bike supply:")
    st.markdown("- Add more bikes to the stations whose start/end destinations are in high-volume tourist areas - namely Lenox Hill, Chelsea (in Upper East Side) and Lower East Side. These stations include: W 21 St/6th Ave; W 22 St/10th Ave; Norfolk St/Broome St; Henry St/Grand St; 1st Ave/E 62 St; 1st Ave/E 68 St; and W 21 St/6th Ave and 9th Ave/W 22 St.") 
    st.markdown("- If we look at rides>750, then we see that there are a lot of bike riders along the Hudson River. So places along the Hudson River that need to be stocked up include: Little West St/1 Pl; West St/Chambers St; Pier 40-Hudson River Park; 10th Ave/W 40 St. The station at Central Park S/6 Ave.")
    
    st.markdown("- Ensure that bikes are fully stocked in all these stations during the warmer months (May to October) in order to meet the higher demand, but provide a lower supply in winter and late autumn to reduce costs.")
    st.markdown("- Limitations of this analysis: We don't know how many bikes are stocked at each station at the beginning of the day. Also, we don't have any records of bike thefts or bike malfunctions.")
                      




    
