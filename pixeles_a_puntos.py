import rasterio
from rasterio.features import shapes
import geopandas as gpd
from shapely.geometry import shape, Point
import json
from affine import Affine

def centroids_from_binary_geotiff(geotiff_path, output_geojson_path):
    # Abrir el archivo GeoTIFF
    with rasterio.open(geotiff_path) as src:
        # Leer la matriz de píxeles como int16
        data = src.read(1, masked=True)

        # Obtener transformación de coordenadas
        transform = src.transform

        # Obtener formas y valores de los contornos de los píxeles con valor 0
        results = (
            {'raster_val': int(value), 'geometry': shape(s)}
            for s, value in shapes(data, mask=data == 0, transform=transform)
        )
        # Convertir los resultados en una lista de diccionarios
        features = list(results)

    # Crear un GeoDataFrame a partir de las características y el CRS del GeoTIFF
    gdf = gpd.GeoDataFrame.from_features(features, crs=src.crs)

    # Transformar las geometrías al sistema de coordenadas proyectado deseado (EPSG:22185)
    gdf = gdf.to_crs('EPSG:22185')

    # Calcular los centroides de las geometrías y agregarlos como una nueva columna
    gdf['centroid'] = gdf['geometry'].centroid

    # Eliminar columnas adicionales de geometría si existen
    if 'geometry' in gdf.columns:
        gdf = gdf.drop(columns=['geometry'])

    # Guardar el GeoDataFrame como un GeoJSON de puntos
    gdf.to_file(output_geojson_path, driver='GeoJSON')

    print(f"GeoJSON de centroides guardado en: {output_geojson_path}")

    
    
input = "C:\\Users\\Facu\\Desktop\\dinamicWorld\\cobertura2023_int16.tif"
output = "C:\\Users\\Facu\\Desktop\\dinamicWorld\\cobertura2023.geojson"
centroids_from_binary_geotiff(input, output)
