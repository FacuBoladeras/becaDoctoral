import os
import glob
import rasterio
import numpy as np

def reclasificar_pixel(value):
    # Definir los rangos de reclasificación según los criterios dados
    if value in [0, 2, 1, 3, 5, 8]:  # water, trees, flooded_vegetation, snow_and_ice
        return 0  # Clase 0
    elif value in [4, 6, 7]:  # grass, crops, shrub_and_scrub, built, bare
        return 1  # Clase 1
    else:
        return 0  # Por defecto, clase 0

def reclasificar_geotiffs(input_folder, output_folder):
    # Listar todos los archivos GeoTIFF en la carpeta de entrada
    input_files = glob.glob(os.path.join(input_folder, '*.tif'))

    # Iterar sobre cada archivo GeoTIFF
    for input_path in input_files:
        # Construir la ruta de salida basada en el nombre del archivo de entrada
        file_name = os.path.basename(input_path)
        output_path = os.path.join(output_folder, file_name)

        with rasterio.open(input_path) as src:
            # Leer la matriz de píxeles del GeoTIFF
            data = src.read(1)

            # Crear una matriz vacía para almacenar los valores reclasificados
            reclasificado = np.zeros_like(data)

            # Aplicar la función de reclasificación a cada píxel
            for i in range(data.shape[0]):
                for j in range(data.shape[1]):
                    reclasificado[i, j] = reclasificar_pixel(data[i, j])

            # Obtener los metadatos de la imagen original para usarlos en la imagen de salida
            profile = src.profile

        # Escribir la matriz reclasificada en un nuevo archivo GeoTIFF
        with rasterio.open(output_path, 'w', **profile) as dst:
            dst.write(reclasificado, 1)

        print(f"Archivo reclasificado guardado en: {output_path}")

folder = "C:\\Users\\Facu\\Desktop\\dinamicWorld"
ouotput = "C:\\Users\\Facu\\Desktop\\dinamicWorld"
reclasificar_geotiffs(folder, ouotput)
