import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import geopandas as gpd
import folium
from streamlit_folium import folium_static 
import warnings
warnings.filterwarnings('ignore')

import streamlit.components.v1 as components

## Modular pages
import page_test
page_test.hello()

hide_streamlit_style = """
            <style>
            #MainMenu {visibility: hidden;}
            footer {visibility: hidden;}
            </style>
            """
st.markdown(hide_streamlit_style, unsafe_allow_html=True) 

# pip install pillow
from PIL import Image
image = Image.open('./images/sunrise.jpg.jpg')
st.image(image, caption='Sunrise by the mountains', use_column_width=False, width=350)


###### DATA Loading
# Create the 6 data frames per csv file (Upload the CSV files first!)
rooms = pd.read_csv("./education_analysis/work/Rooms data.csv")
schools_loc = pd.read_csv("./education_analysis/work/Schools Location Data.csv")
teachers = pd.read_csv("./education_analysis/work/Teachers data.csv")
mooe = pd.read_csv("./education_analysis/work/MOOE data.csv")
masterlist= pd.read_csv("./education_analysis/work/Masterlist of Schools.csv")
enrol_e = pd.read_csv("./education_analysis/work/Enrollment Master Data_2015_E.csv")
enrol_s = pd.read_csv("./education_analysis/work/Enrollment Master Data_2015_S.csv")

region_stats = pd.read_csv("./education_analysis/work/regional_stats.csv")

df = pd.read_csv("schools_combined.csv")
######  End DATA Loading


## Side bars
st.sidebar.title("Group 1 - Sprint 01")
st.sidebar.header("Student Enrollment Retention Situation In the Philippines")

## Always present
st.header("Student Enrollment Retention Situation In the Philippines")

### Sprint Codes
page_nav = st.sidebar.radio('Navigation', ['Overview', 'Data', 'page 3', 'page 4', 'page 5'])

## Page codes now for the sprint
def page_Overview():
    st.title('Overview')
    st.markdown("Lorem ipsum")

def page_Data():
    st.title('Data')
    st.markdown("")

## Page switch
if page_nav == 'Overview':
    page_Overview()
elif page_nav == 'Data':
    page_Data()

    
# ()*)(*)(*)(*)(*)(*)(*)(*)(*)(*)(*)(*)(*)(*)(*)(*)(*)(*)
### GUIDE Code to be removed
my_page = st.sidebar.radio('EDA Navigation', ['None','page 1', 'page 2', 'page 3', 'page 4', 'page 5'])


## Pages code
# ''' Format to use: Page_NAME'''
def page_1():
    st.title("Data")
    # Add section header
    st.header("Public School Data in the Philippines")
    data_load_state = st.text('Loading data...')
    st.write(df.head(20))
    data_load_state.text('Loading data...done!')
    
    with st.beta_expander("About the data:"):
        st.write("2015 data is from the Department of Education.")
def page_2():
    option = st.sidebar.selectbox(
        'Which Region do you like best?',
         df['region'].unique())
    'You selected: ', option

    grade_level = df[df["region"]==option].groupby("year_level")["enrollment"].sum()

    # store figure in fig variable
    fig = plt.figure(figsize=(8,6)) 

    plt.bar(grade_level.index, grade_level.values) 

    plt.title("Students in Public Schools", fontsize=16)
    plt.ylabel("Number of Enrollees", fontsize=12)
    plt.xlabel("Year Level", fontsize=12)
    year = ["grade 1","grade 2", "grade 3", "grade 4", "grade 5", "grade 6",
            "first year", "second year", "third year", "fourth year"]
    plt.xticks(range(len(grade_level.index)), year, rotation=45)

    # display graph
    st.pyplot(fig)
    
def page_3():
    st.title("Geospatial Analysis of Schools : Folium")
    schools = gpd.read_file('./phl_schp_deped/phl_schp_deped.shp')
    schools["x"] = schools.geometry.centroid.x
    schools["y"] = schools.geometry.centroid.y
    #st.write(schools.head(20))
    # Coordinates to show
    map_center = [14.583197, 121.051538]

    # Styling the map
    mymap = folium.Map(location=map_center, height=700, width=1000, tiles="OpenStreetMap", zoom_start=14)
    option_city = st.sidebar.selectbox(
        'Which city',
        schools["Division"].unique())
    'You selected: ', option_city
    city = option_city

    df_city = schools[schools["Division"]==city]

    for i in np.arange(len(df_city)):
        lat = df_city["y"].values[i]
        lon = df_city["x"].values[i]
        name = df_city["School"].values[i]
        folium.Marker([lat, lon], popup=name).add_to(mymap)
    folium_static(mymap)

def page_4():
    st.title("Geospatial Analysis of Schools : st.map()")
    schools = gpd.read_file('./phl_schp_deped/phl_schp_deped.shp')
    schools["lon"] = schools.geometry.centroid.x
    schools["lat"] = schools.geometry.centroid.y
    st.map(schools)
    
def page_5():
    st.title("Geospatial Analysis of Schools : Geopandas")
    # To plot easier, a new shapefile was created with the cleaned data
    merged_data = gpd.read_file("./map_data_clean/map_data_clean.shp")
   
    # Copied from Mapping exercise
    variable = 'Total_Enro'
    vmin, vmax = merged_data["Total_Enro"].min(), merged_data["Total_Enro"].max()

    fig, ax = plt.subplots(1, figsize=(15, 10))
    merged_data.plot(column=variable, cmap='Oranges', linewidth=0.8, ax=ax, edgecolor='0.8', vmin=vmin, vmax=vmax)
    sm = plt.cm.ScalarMappable(cmap='Oranges', norm=plt.Normalize(vmin=vmin, vmax=vmax))
    cbar = fig.colorbar(sm)
    st.pyplot(fig)


if my_page == 'page 1':
    page_1()
    
elif my_page == 'page 2':
    page_2()
    
elif my_page == 'page 3':
    page_3()
    
elif my_page == 'page 4':
    page_4()
    
elif my_page == 'page 5':
    page_5()
else:
    print("")