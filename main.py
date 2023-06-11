from gestion_obras.gestionar_obras import GestionarObra
from descarga.descarga_csv import descargar_archivo
import os


def menu():
    print("Menú:")
    print("1. Descargar archivo")
    print("2. Crear base de datos")
    print("3. Gestionar obras")
    print("4. Salir")


def main():
    opcion = None

    while opcion != "4":
        menu()
        opcion = input("Ingrese la opción deseada: ")

        if opcion == "1":
            # llamo a la funcion y descargo
            descargar_archivo()
            print("Archivo descargado exitosamente.")

        elif opcion == "2":
            # crear db

            GestionarObra.conectar_db()
            GestionarObra.mapear_orm()
            print("Base de datos creada exitosamente.")

        elif opcion == "3":

            # Gestionar obras

            ruta_archivo_csv = os.path.join(os.path.dirname(
                __file__), "descarga", "observatorio-de-obras-urbanas.csv")
            ruta_archivo_sanitizado = os.path.join(
                "descarga", "sanitizado_" + "observatorio-de-obras-urbanas.csv")

            GestionarObra.limpiar_datos(ruta_archivo_csv)
            GestionarObra.extraer_datos(ruta_archivo_sanitizado)
            print("Obras gestionadas exitosamente.")

        elif opcion == "4":
            print("Saliendo del programa.")
            break

        else:
            print("Opción inválida. Por favor, ingrese una opción válida.")


if __name__ == "__main__":
    main()
