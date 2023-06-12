import os
import requests

# Mod en descarga_csv.py para que sea una funcion


def descargar_archivo():
    url = "https://cdn.buenosaires.gob.ar/datosabiertos/datasets/secretaria-general-y-relaciones-internacionales/ba-obras/observatorio-de-obras-urbanas.csv"
    archivo_csv = "observatorio-de-obras-urbanas.csv"
    ruta_archivo = os.path.join("descarga", archivo_csv)

    if os.path.exists(ruta_archivo):
        print("Atención: El archivo ya existe.")
        return
    else:
        try:
            response = requests.get(url)
            response.raise_for_status()  # Lanza una excepción en caso de error en la respuesta

            with open(ruta_archivo, "wb") as archivo:
                archivo.write(response.content)

            print("Archivo esta descargado exitosamente.")

        except requests.exceptions.RequestException as e:
            print("Error al descargar el archivo:", str(e))
