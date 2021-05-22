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
st.set_page_config(page_title="Resource Allocation of SPED Schools in the Philippines")
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

###### Data Geopandas

#FOR GEOPANDAS
df_sped = pd.read_csv("schools_combined_SPED.csv")
provice_data = gpd.read_file('./Provinces/Provinces/Provinces.shp')

#FOR FOLIUM
geo_data= gpd.read_file('./phl_schp_deped/phl_schp_deped.shp')
geo_data["x"] = geo_data.geometry.centroid.x
geo_data["y"] = geo_data.geometry.centroid.y

province_dic = {'CITY OF COTABATO':'Maguindanao',
 'Manila, Ncr, First District':"Metropolitan Manila",
 'Ncr Fourth District':"Metropolitan Manila",
 'Ncr Second District':"Metropolitan Manila",
 'Ncr Third District':"Metropolitan Manila",
 'CITY OF ISABELA':"Basilan"}

df_sped["school.province"] = df_sped["school.province"].str.title().replace(province_dic).str.replace("Del", 'del')
sped_province = df_sped.groupby("school.province")["school.id"].nunique().reset_index()
merged_data = pd.merge(provice_data,sped_province,left_on="PROVINCE",right_on="school.province",how ="left").fillna(0)
sped_corr=df_sped.fillna("Urban")
sped_urban = sped_corr[sped_corr["school.urban"] =="Urban"]
sped_part_urban = sped_corr[sped_corr["school.urban"] =="Partially Urban"]
sped_rural = sped_corr[sped_corr["school.urban"] =="Rural"]
######


## Side bars
#st.sidebar.title("Group 1 - Sprint 01")
#st.sidebar.header("Student Enrollment Retention Situation In the Philippines")
st.sidebar.title("Resource Allocation of SPED Schools in the Philippines")

## Always present
#st.header("Student Enrollment Retention Situation In the Philippines")

### Sprint Codes
page_nav = st.sidebar.radio('Navigation', ['Introduction', 'Data Information', 'Methodology', 'Exploratory Data Analysis', 'Interactive Map', 'Heat Maps', 'Cluster Analysis', 'Other Cluster Insights', 'Conclusion and Recommendations'])

## Page codes now for the sprint
def page_Intro():
    #st.title('Introduction')
    st.header("Resource Allocation of SPED Schools in the Philippines")
    #st.header("Resource Allocation of SPED Schools ")
    #st.header("in the Philippines")
    #st.markdown("Lorem ipsum")
    image1 = Image.open('./images/slide1_teacher.png')
    image2 = Image.open('./images/slide1_wheelchair.png')
    #st.image(image1, caption='', use_column_width=False, width=350)
    #st.image(image2, caption='', use_column_width=False, width=350)
    st.markdown("""
Education is one of the most important human rights. It serves as a capital investment and equalizer for everyone. The right to education is practiced starting from the formative years of a child all throughout their life. However, not all children will have the chance to exercise this right. This opportunity  to avail education should not be as challenged as to whatever mental and physical status they may present in.

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
According to the Philippine Statistics Authority, **16 per thousand** of the country’s population had disability. In the 2010 Census of Population and Housing, the recorded persons with disabilities was 935, 551 person, which was 1.23 percent of the total household population. 
    """)
    st.markdown("""
From the 2009 report Inclusive Education as Strategy for Increasing Participation Rate of Children done by the Department of Education, the Philippines has only served **2% of the targeted 2.2 million children with disabilities** in the country who live without access to a basic human right: the right to education.
    """)
    
    st.markdown("""
## Objective

To use clustering to help assess how resource allocation for SPED schools should be prioritized in the country


    """)
def page_Data():
    st.title('Data Information')
    #st.text("lorem ipsum")
    st.markdown("")
    image1 = Image.open('./images/slide2_data_information.png')
    st.image(image1, caption='')
             #, use_column_width=False, width=350)
    #st.dataframe(df_sped.iloc[:,1:])
    st.markdown("""
Data sources: [Department of Education](https://www.deped.gov.ph/)
    """)

def page_Methodology():
    st.title('Methodology')
    st.text('')
    image1 = Image.open('./images/methodology.png')
    st.image(image1, caption='')
    st.text('')
    st.markdown("""
We consolidated seven source data from the Department of Education. Then proceeded to cleaning the datasets including dropping the zero and missing values. To produce a certain result, we concatenated and merged some chosen datasets and filtered it to our target study.
In getting a good grip of our raw data for us to show an accurate model, we engineered 5 features in answering our target study about SPED. Ratios exclusive only to SPED (such as the student-teacher ratio, student per school room ratio, and MOOE per teacher ratio, MOOE per student ratio, and MOOE per room ratio). We then proceeded to prepare the dataset and scaled it to feed to our different models. 
    """)
    
def page_EDA():
    st.title('Exploratory Data Analysis')
    st.text("")
    # Start EDA
    image1 = Image.open('./images/sped_vs_non-sped.png')
    st.image(image1, caption='', use_column_width=False, width=500)
    st.markdown("""
There are around 45,000 schools for non-SPED  which is comparatively high versus
SPED Schools which is around less than 1, 500.
    """)
    st.text("")
    st.text("")
    
    # Sped Schools
    st.markdown("""
## SPED schools location distribution:
    """)
    image1 = Image.open('./images/sped_based_on_urban_types.png')
    image2 = Image.open('./images/sped_school_heatmap.png')
    st.image(image2, caption='', use_column_width=False, width=350)
    st.image(image1, caption='', use_column_width=False, width=350)
    st.markdown("""
-Majority are located at areas that are urban or partially urban
-SPED schools are concentrated mainly at Luzon

**Top 5: NCR, Pangasinan, Batangas, Zamboanga del Sur, Quezon, and Cebu**
    """)
    st.text('')
    st.text('')
    
    # MOOE SPED 
    image1 = Image.open('./images/mooe_sped_02.png')
    st.image(image1, caption='', use_column_width=False, width=500)
    
    st.markdown("""
On average, SPED Schools have a much higher MOOE than non SPED Schools
    """)
    
    # MOOE SPED by Urban Type
    st.markdown("""
## MOOE and Number of Students grouped by School Urban Type
    """)
    image1 = Image.open('./images/mooe_urban.png')
    st.image(image1, caption='', use_column_width=False, width=700)
    
    st.markdown("""
    """)
    
    # MOOE SPED without Outliers by Urban Type
    st.markdown("""
### Zooming into SPED's MOOE without outlier by Urban Type
    """)
    image1 = Image.open('./images/boxplot_sped_grouped_by_urban_type_no_outlier.png')
    st.image(image1, caption='', use_column_width=False, width=700)
    
    st.markdown("""
MOOE is divided roughly equally, with urban schools getting the most MOOE by only a small amount
    """)
    
    # MOOE is distributed more or less evenly among city income groups with only a bit of discrepancy
    image1 = Image.open('./images/sped_no_outlier_grouped_by_city_income.png')
    st.image(image1, caption='', use_column_width=False, width=700)
    
    st.markdown("""
MOOE is distributed more or less evenly among city income groups with only a bit of discrepancy
    """)
    
    # MOOE SPED by Region
    image1 = Image.open('./images/sped_mooe_no_outlier_grouped_by_region.png')
    st.image(image1, caption='', use_column_width=False, width=700)
    
    st.markdown("""
MOOE is distributed more or less evenly among the regions with only a bit of discrepancy
    """)
    
def page_Cluster01():
    st.title('Cluster Analysis')
    st.text("")
        # Cluster Radar
    st.markdown("""
## Radar Charts of Cluster
    """)
    st.markdown("""
Majority of SPED schools are in cluster zero with low resources and financial support. It consists of 83% of SPED schools in the country. This illustrates an imbalance in allocating resources. 
    """)
    image1 = Image.open('./images/radarchar_clusters.png')
    st.image(image1, caption='', use_column_width=False, width=700)
    
    st.markdown("""
**Cluster 0** - Low demand, low resources, and low financial support

**Cluster 1** - Low demand, low resources but high financial support

**Cluster 2** - High demand, High financial support, but low resources
    """)
    
def page_Cluster02():
    st.title('Other Cluster Insights')
    st.text("")
    
    # MOOE vs Students
    image1 = Image.open('./images/sped_clusters_mooe_students.png')
    st.image(image1, caption='', use_column_width=False, width=700)
    
    st.markdown("""
**Cluster 1** has moderate MOOE allocation whilst having the most number of students. **Cluster 0** has the least MOOE allocated while **cluster 2** has the most MOOE allocated despite having the least number of students.
    """)
    
    # 
    image1 = Image.open('./images/sped_teachers_rooms.png')
    st.image(image1, caption='', use_column_width=False, width=700)
    
    st.markdown("""
For the teachers, there is no significant difference among them. Cluster 0 has the least rooms allocated for its student while cluster 2 enjoys having the most rooms provided. However...
    """)
    # SPED schools by Cluster
    image1 = Image.open('./images/sped_schools_cluster.png')
    st.image(image1, caption='', use_column_width=False, width=700)
    
    st.markdown("""
… cluster 0 has the most SPED schools with over 1000 schools while cluster 2 has the least, garnering less than 10 schools.
    """)
    
def page_Conclusion():
    st.title("Conclusion and Recommendations")
    st.markdown("""
## Conclusion

-Despite having more MOOE allocation than non SPED schools, there is an uneven distribution of resources for SPED. In particular, majority of SPED schools suffer from lack of resources while the minority has the most allocated resources. 

## Recommendation

-This study could serve as a benchmark since the data was dated on year 2015.

-There needs to be better assessment on how resources and budgeting should be allocated among SPED schools.

-Future studies may benefit in looking into other discrepancies in resources (school supplies, books, learning aids)
    """)
    
def page_folium_part():
    #FOLIUM PART
    fol_sped = pd.merge(df_sped,geo_data,left_on="School ID_y", right_on = "ID",how ="left")
    fol_filtered = fol_sped[fol_sped['geometry'].notnull()]

    # Coordinates to show
    map_center = [14.583197, 121.051538]
    # Styling the map
    mymap = folium.Map(location=map_center, height=700, width=1000, tiles="OpenStreetMap", zoom_start=14)

    from folium.plugins import MarkerCluster
    mymap_cluster = folium.Map(location=map_center, height=700, width=1000, tiles="OpenStreetMap", zoom_start=13)
    marker_cluster = MarkerCluster().add_to(mymap_cluster)

    #DISCLAIMER: 769 out of 1362 schools only has geo data available!!!

    st.title("Location of Schools offering SPED Education in the Philippines")
    st.text("DISCLAIMER: 769 out of 1212 schools only has geo data available")

    for i in np.arange(len(fol_filtered)):
        lat = fol_filtered["y"].values[i]
        lon = fol_filtered["x"].values[i]
        name = fol_filtered["school.name"].values[i]
        folium.Marker([lat,lon], popup=name).add_to(marker_cluster)

    folium_static(mymap_cluster)

def page_geopandas_part():
    #GEOPANDAS PART

    option = st.sidebar.selectbox('Which Urban Type do you like best?',['All', 'Urban', 'Partially Urban', 'Rural'])

    if option == "All":
        st.title("Geospatial Analysis of SPED Schools")
        ## OVERALL SPED

        # set a variable that will call whatever column we want to visualise on the map
        variable = 'school.id'
        # set the range for the choropleth
        vmin, vmax = merged_data["school.id"].min(), merged_data["school.id"].max()
        # create figure and axes for Matplotlib
        fig, ax = plt.subplots(1, figsize=(15, 10))

        # Complete the code
        merged_data.plot(column=variable, cmap='Oranges', linewidth=0.8, ax=ax, edgecolor='0.8', vmin=vmin, vmax=vmax)

        sm = plt.cm.ScalarMappable(cmap='Oranges', norm=plt.Normalize(vmin=vmin, vmax=vmax))
        cbar = fig.colorbar(sm)
        st.pyplot(fig)

    elif option == "Urban":
        st.title("Geospatial Analysis of Urban SPED Schools")
            #SPED URBAN
        sped_province_U = sped_urban.groupby("school.province")["school.id"].nunique().reset_index()
        merged_data_U = pd.merge(provice_data,sped_province_U,left_on="PROVINCE",right_on="school.province",how ="left").fillna(0)

        # set a variable that will call whatever column we want to visualise on the map
        variable = 'school.id'
        # set the range for the choropleth
        vmin, vmax = merged_data_U["school.id"].min(), merged_data_U["school.id"].max()
        # create figure and axes for Matplotlib
        fig, ax = plt.subplots(1, figsize=(15, 10))

        # Complete the code
        merged_data.plot(column=variable, cmap='Oranges', linewidth=0.8, ax=ax, edgecolor='0.8', vmin=vmin, vmax=vmax)

        sm = plt.cm.ScalarMappable(cmap='Oranges', norm=plt.Normalize(vmin=vmin, vmax=vmax))
        cbar = fig.colorbar(sm)
        st.pyplot(fig)

    elif option == "Partially Urban":
        st.title("Geospatial Analysis of Partially Urban SPED Schools")
        #SPED PARTIAL URBAN
        sped_province_PU = sped_part_urban.groupby("school.province")["school.id"].nunique().reset_index()
        merged_data_PU = pd.merge(provice_data,sped_province_PU,left_on="PROVINCE",right_on="school.province",how ="left").fillna(0)

        # set a variable that will call whatever column we want to visualise on the map
        variable = 'school.id'
        # set the range for the choropleth
        vmin, vmax = merged_data_PU["school.id"].min(), merged_data_PU["school.id"].max()
        # create figure and axes for Matplotlib
        fig, ax = plt.subplots(1, figsize=(15, 10))

        # Complete the code
        merged_data.plot(column=variable, cmap='Oranges', linewidth=0.8, ax=ax, edgecolor='0.8', vmin=vmin, vmax=vmax)

        sm = plt.cm.ScalarMappable(cmap='Oranges', norm=plt.Normalize(vmin=vmin, vmax=vmax))
        cbar = fig.colorbar(sm)
        st.pyplot(fig)

    elif option == "Rural":
        st.title("Geospatial Analysis of Rural SPED Schools")
        #SPED RURAL
        sped_province_R = sped_rural.groupby("school.province")["school.id"].nunique().reset_index()
        merged_data_R = pd.merge(provice_data,sped_province_R,left_on="PROVINCE",right_on="school.province",how ="left").fillna(0)

        # set a variable that will call whatever column we want to visualise on the map
        variable = 'school.id'
        # set the range for the choropleth
        vmin, vmax = merged_data_R["school.id"].min(), merged_data_R["school.id"].max()
        # create figure and axes for Matplotlib
        fig, ax = plt.subplots(1, figsize=(15, 10))

        # Complete the code
        merged_data.plot(column=variable, cmap='Oranges', linewidth=0.8, ax=ax, edgecolor='0.8', vmin=vmin, vmax=vmax)

        sm = plt.cm.ScalarMappable(cmap='Oranges', norm=plt.Normalize(vmin=vmin, vmax=vmax))
        cbar = fig.colorbar(sm)
        st.pyplot(fig)
    
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
elif page_nav == 'Interactive Map':
    page_folium_part()
elif page_nav == 'Heat Maps':
    page_geopandas_part()
    
# ()*)(*)(*)(*)(*)(*)(*)(*)(*)(*)(*)(*)(*)(*)(*)(*)(*)(*)
### GUIDE Code to be removed
#my_page = st.sidebar.radio('Data Navigation', ['None','page 1', 'page 2', 'page 3', 'page 4', 'page 5'])
my_page = []


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
## The Team
- Jon Marco Francisco
- Joshua Miguel Bernardino
- Matthew Chan
- Robby Jean J. Pombo
- Rowen Remis R. Iral

*Eskwelabs Data Science Fellows Cohort 7*

*Mentored by Patrick Juan*
""")