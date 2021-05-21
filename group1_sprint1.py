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

## Extra configs
st.set_page_config(page_title="DSFC7 Group 1 - Sprint 01")
hide_streamlit_style = """
            <style>
            #MainMenu {visibility: hidden;}
            footer {visibility: hidden;}
            </style>
            """
st.markdown(hide_streamlit_style, unsafe_allow_html=True) 
## End of Extra configs

## Modular pages
#import page_test
#page_test.hello()


# Example how to load Images
# pip install pillow
from PIL import Image
#image = Image.open('./images/sunrise.jpg.jpg')
#st.image(image, caption='Sunrise by the mountains', use_column_width=False, width=350)
# end of Image load example

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

df_sped = pd.read_csv("./education_analysis/schools_combined_SPED.csv")
######  End DATA Loading


## Side bars
#st.sidebar.title("Group 1 - Sprint 01")
#st.sidebar.header("Student Enrollment Retention Situation In the Philippines")
st.sidebar.title("Resource Allocation of SPED Schools in the Philippines")

## Always present
#st.header("Student Enrollment Retention Situation In the Philippines")

### Sprint Codes
page_nav = st.sidebar.radio('Navigation', ['Introduction', 'Data Information', 'Methodology', 'Exploratory Data Analysis', 'Cluster Analysis', 'Other Cluster Insights', 'Conclusion and Recommendations'])

## Page codes now for the sprint
def page_Intro():
    #st.title('Introduction')
    #st.header("Resource Allocation of SPED Schools in the Philippines")
    st.header("Resource Allocation of SPED Schools ")
    st.header("in the Philippines")
    #st.markdown("Lorem ipsum")
    image1 = Image.open('./images/slide1_teacher.png')
    image2 = Image.open('./images/slide1_wheelchair.png')
    #st.image(image1, caption='', use_column_width=False, width=350)
    #st.image(image2, caption='', use_column_width=False, width=350)
    st.markdown("""
Education is one of the most important human rights. It serves as a capital investment and equalizer for everyone. The right to education is practiced starting from the formative years of a child all throughout their life. However, not all children will have the chance to exercise this opportunity. And this opportunity to avail education should not be as challenged as to whatever mental and physical status they may present in.

Inclusive education also called inclusion is an education that includes everyone. This covers non-disabled and disabled children with special educational needs and to be able to provide them with fair and safe learning environment.
    """)
    col1, col2 = st.beta_columns(2)
    col1.image(image1, use_column_width=True) # you can also use col1.header("Title")
    col2.image(image2, use_column_width=True) # you can also use col2.header("Title")
    st.markdown("""
The Philippine Constitution, the Child and Welfare  Code (PD 603), the Enhanced Basic Education Act (RA 105333), and the Magna Carta for Disabled Persons (RA 7277) mandated the adoption of IE (Inclusive Education) approach in the Philippine Education system.

Inclusive Education in the form of Special Education program is a good way to cater the diversity of needs for all learners and lessen the challenges in achieving education for every status.
    """)
    st.markdown("""
According to the Philippine Statistics Authority, 16 per thousand of the country’s population had disability. In the 2010 Census of Population and Housing, the recorded persons with disabilities was 935, 551 person, which was 1.23 percent of the total household population. 
    """)
    st.markdown("""
From the 2009 report Inclusive Education as Strategy for Increasing Participation Rate of Children done by the Department of Education, the Philippines has only served 2% of the targeted 2.2 million children with disabilities in the country who live without access to a basic human right: the right to education.
    """)
    
def page_Data():
    st.title('Data Information')
    st.text("lorem ipsum")
    st.markdown("")
    st.dataframe(df_sped.iloc[:,1:])

def page_Methodology():
    st.title('Methodology')
    st.markdown("""
We consolidated seven source data from the Department of Education. Then proceeded to cleaning the datasets including dropping the zero and missing values. To produce a certain result, we concatenated and merged some chosen datasets and filtered it to our target study.
In getting a good grip of our raw data for us to show an accurate model, we engineered 5 features in answering our target study about SPED. Ratios exclusive only to SPED (such as the student-teacher ratio, student per school room ratio, and MOOE per teacher ratio, MOOE per student ratio, and MOOE per room ratio). We then proceeded to prepare the dataset and scaled it to feed to our different models. 
    """)
    
def page_EDA():
    st.title('Exploratory Data Analysis')
    st.text("")
    
def page_Cluster01():
    st.title('Cluster Analysis')
    st.text("")
    
def page_Cluster02():
    st.title('Other Cluster Insights')
    st.text("")
    
def page_Conclusion():
    st.title("Conclusion")
    st.text("")
    
def page_Recommendation():
    st.title("Recommenation")
    st.text("")
    
    
## Page switching
if page_nav == 'Introduction':
    page_Intro()
elif page_nav == 'Data Information':
    page_Data()
elif page_nav == 'Methodology':
    page_Methodology()
elif page_nav == 'Exploratory Data Analysis':
    page_EDA()
elif page_nav == 'Cluster Analysis':
    page_Cluster01()
elif page_nav == 'Other Cluster Insights':
    page_Cluster02()
elif page_nav == 'Conclusion and Recommendations':
    page_Conclusion()
    page_Recommendation()

    
# ()*)(*)(*)(*)(*)(*)(*)(*)(*)(*)(*)(*)(*)(*)(*)(*)(*)(*)
### GUIDE Code to be removed
my_page = st.sidebar.radio('Data Navigation', ['None','page 1', 'page 2', 'page 3', 'page 4', 'page 5'])


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
    
## Credits
st.sidebar.markdown("""
# Group 1 - Sprint 01
## The Team
A data app created by:
- Marko
- Joshua Miguel Bernardino
- Matthew Chan
- Robby Jean J. Pombo
- Rowen Remis R. Iral

*Eskwelabs Data Science Fellows Cohort 7*

*Mentored by Patrick Juan*
""")