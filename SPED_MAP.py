import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import geopandas as gpd
import folium
from streamlit_folium import folium_static 
import warnings
warnings.filterwarnings('ignore')

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

my_page = st.sidebar.radio('Page Navigation', ['Interactive Map', 'Heat Maps'])

if my_page=="Interactive Map":

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

if my_page=="Heat Maps":
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