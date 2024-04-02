import json
import re

import geopandas as gpd
import matplotlib.pyplot as plt
import streamlit as st

from poly2tile_bounds import polygon_to_tiles, split_singe_tile

st.set_page_config(layout="wide")

st.title("GeoJSON to Tiles Bounds")

# Sidebar for user inputs and navigation
st.sidebar.header("Navigation")
page = st.sidebar.radio("Go to", ["GeoJSON to Tile Bounds", "Split Tile"])

if page == "GeoJSON to Tile Bounds":
    # Sidebar for user inputs
    st.sidebar.header("Input GeoJSON")
    input_method = st.sidebar.selectbox(
        "Input Method", ["Upload GeoJSON File", "Enter GeoJSON"]
    )

    input_geojson = None
    if input_method == "Upload GeoJSON File":
        uploaded_file = st.sidebar.file_uploader(
            "Choose a GeoJSON file", type=["geojson"]
        )
        if uploaded_file is not None:
            input_geojson = gpd.read_file(uploaded_file)
    else:
        input_geojson_str = st.sidebar.text_area("Enter GeoJSON")
        try:
            input_geojson = gpd.GeoDataFrame.from_features(
                json.loads(input_geojson_str), crs="EPSG:4326"
            )
        except json.JSONDecodeError:
            st.error("Invalid GeoJSON input")
            input_geojson = None

    zoom_level = st.sidebar.slider("Zoom Level", min_value=2, max_value=22, value=15)

    # Main content area
    if input_geojson is not None:
        st.header("Input GeoJSON")
        st.write(input_geojson)

        with st.spinner(f"Generating tiles for zoom level {zoom_level}..."):
            tiles_geom = polygon_to_tiles(input_geojson, zoom_level)
            tiles_gdf = gpd.GeoDataFrame.from_features(tiles_geom, crs="EPSG:4326")

        st.subheader("Display")
        fig, ax = plt.subplots(figsize=(8, 8))
        input_geojson.plot(
            ax=ax, edgecolor="red", facecolor="none", label="Input GeoJSON"
        )
        tiles_gdf.boundary.plot(
            ax=ax, edgecolor="black", facecolor="none", label="Tiles"
        )
        ax.legend()
        st.pyplot(fig)

        st.subheader("Download")
        tiles_geojson = json.dumps(tiles_geom)
        st.download_button(
            label="Download Tiles GeoJSON",
            data=tiles_geojson,
            file_name="tiles.geojson",
            mime="application/json",
        )

        st.subheader("Tiles GeoJSON")
        st.json(tiles_geom, expanded=False)

elif page == "Split Tile":
    st.sidebar.header("Split Tile")
    tile_input_method = st.sidebar.radio(
        "Tile Input Method", ["String Input", "Number Input"]
    )

    if tile_input_method == "Number Input":
        tile_x = st.sidebar.number_input("Tile X", value=24025)
        tile_y = st.sidebar.number_input("Tile Y", value=13707)
        tile_z = st.sidebar.number_input("Tile Z", value=10)
    else:
        tile_string = st.sidebar.text_input(
            "Enter Tile String", value="Tile(x=24025, y=13707, z=10)"
        )
        tile_pattern = r"Tile\(x=(\d+), y=(\d+), z=(\d+)\)"
        match = re.match(tile_pattern, tile_string)
        if match:
            tile_x = int(match.group(1))
            tile_y = int(match.group(2))
            tile_z = int(match.group(3))
        else:
            st.error("Invalid tile string format")
    split_zoom_level = st.sidebar.number_input("Split Zoom Level", value=17)

    if st.sidebar.button("Split Tile"):
        splitted_tiles = split_singe_tile(tile_x, tile_y, tile_z, split_zoom_level)
        st.write("Splitted Tiles GeoJSON:")
        st.download_button(
            label="Download Splitted Tiles GeoJSON",
            data=json.dumps(splitted_tiles),
            file_name="splitted_tiles.geojson",
            mime="application/json",
        )
        splitted_gdf = gpd.GeoDataFrame.from_features(splitted_tiles, crs="EPSG:4326")

        fig, ax = plt.subplots(figsize=(10, 10))
        splitted_gdf.boundary.plot(ax=ax, edgecolor="black", facecolor="none")
        st.pyplot(fig)
        st.json(splitted_tiles, expanded=False)
