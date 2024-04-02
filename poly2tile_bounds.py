import json
import os
from multiprocessing import Pool

import geopandas as gpd
import mercantile
from shapely.geometry import shape


def split_singe_tile(tile_x, tile_y, tile_z, split_zoom_level):
    children_tiles = mercantile.children(
        mercantile.Tile(tile_x, tile_y, tile_z), zoom=split_zoom_level
    )
    print(f"Tile splitted into {len(children_tiles)} children tiles")
    features = []
    for tile in children_tiles:
        features.append(mercantile.feature(tile))
    feature_collection = {"type": "FeatureCollection", "features": features}
    return feature_collection


def polygon_to_tiles(polygon_input, zoom_level):
    input_crs = "EPSG:4326"
    if isinstance(polygon_input, gpd.GeoDataFrame):
        gdf = polygon_input
    elif isinstance(polygon_input, dict):
        gdf = gpd.GeoDataFrame.from_features(polygon_input, crs=input_crs)
    elif isinstance(polygon_input, str):
        if os.path.isfile(polygon_input):
            gdf = gpd.read_file(polygon_input, crs=input_crs)
        else:
            try:
                polygon_geojson = json.loads(polygon_input)
                gdf = gpd.GeoDataFrame.from_features(polygon_geojson, crs=input_crs)
            except json.JSONDecodeError:
                raise ValueError("String input is not a valid GeoJSON or file path.")
    else:
        raise ValueError("Invalid geojson input")

    # gdf = gdf.to_crs(epsg=3857)
    gdf.plot()

    # Parallel processing for generating tiles
    with Pool() as pool:
        features = pool.starmap(
            process_row, [(row.geometry, zoom_level) for _, row in gdf.iterrows()]
        )

    features = sum(features, [])
    print(
        f"Found {len(features)} tiles at zoom level {zoom_level} intersecting with the original geometry."
    )

    feature_collection = {"type": "FeatureCollection", "features": features}
    return feature_collection


def process_row(geometry, zoom_level):
    west, south, east, north = geometry.bounds
    tiles = mercantile.tiles(west, south, east, north, zooms=zoom_level)
    features = []
    for tile in tiles:
        tile_feature = mercantile.feature(tile)
        tile_geom = shape(tile_feature["geometry"])
        if tile_geom.intersects(geometry):
            features.append(tile_feature)
    return features
