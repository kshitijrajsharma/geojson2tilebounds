## GeoJSON to Tile Bounds

This project provides two tools for working with GeoJSON data and generating tile bounds:

- A Streamlit application for converting GeoJSON polygons into tile bounds and visualizing the results.
- A Python script (geojson2tiles.py) for converting GeoJSON polygons into tile bounds using parallel processing.

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

- Geojson to tile bounds 
![tilebounds](https://github.com/kshitijrajsharma/geojson2tilebounds/assets/36752999/7a1f8389-1fed-4852-8d42-a4eebf685f53)


- Split tiles 
![chrome-capture-2024-3-2](https://github.com/kshitijrajsharma/geojson2tilebounds/assets/36752999/1e41abeb-0ce1-463b-82df-9649646bd49d)



Note: The geojson2tiles script is also used by the Streamlit app, so any changes made to the script will be reflected in the app as well.
