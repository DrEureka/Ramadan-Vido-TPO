import os
import requests

# Mod en descarga_csv.py para que sea una funcion


def descargar_archivo():
    url = "https://cdn.buenosaires.gob.ar/datosabiertos/datasets/secretaria-general-y-relaciones-internacionales/ba-obras/observatorio-de-obras-urbanas.csv"
    archivo_csv = "observatorio-de-obras-urbanas.csv"
    ruta_archivo = os.path.join("descarga", archivo_csv)

    response = requests.get(url)
    with open(ruta_archivo, "wb") as archivo:
        archivo.write(response.content)
