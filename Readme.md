## GeoJSON to Tiles

This project provides two tools for working with GeoJSON data and generating tiles:

- A Streamlit application for converting GeoJSON polygons into tiles and visualizing the results.
- A Python script (geojson2tiles.py) for converting GeoJSON polygons into tiles using parallel processing.

## Prerequisites

Before running the Streamlit app or the Python script, make sure you have the following dependencies installed:

- Python 3.x
- geopandas
- mercantile
- shapely
- streamlit (for the Streamlit app)

You can install these dependencies using pip:
```bash
pip install geopandas mercantile shapely streamlit
```

### Using the Streamlit App

Navigate to the project directory.
Run the Streamlit app with the following command:

```bash
streamlit run streamlit_app.py
```
The app will open in your default web browser. If not, you can access it by clicking the URL provided in the terminal output.
        
- In the sidebar, you can either upload a GeoJSON file or enter the GeoJSON string or json directly.
    - Adjust the zoom level using the slider.
    - The app will generate tiles from the input GeoJSON and display them on the map.
    - You can download the tiles GeoJSON or view the raw GeoJSON data.
- In the sidebar, you can also split a specific tile by providing the tile coordinates (x, y, z) and the desired split zoom level.


Note: The geojson2tiles script is also used by the Streamlit app, so any changes made to the script will be reflected in the app as well.