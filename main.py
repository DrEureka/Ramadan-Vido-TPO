from gestion_obras.gestionar_obras import GestionarObra
from descarga.descarga_csv import descargar_archivo
from dao.modelo_orm import Obra
import os


def menu():
    print("Menú:")
    print("1. Descargar archivo")
    print("2. Crear base de datos")
    print("3. Gestionar obras")
    print("4. Obtener estadisticas de la db")
    print("5. Crear una nueva obra")
    print("6. Salir")


def main():
    opcion = None

    while opcion != "6":
        menu()
        opcion = input("Ingrese la opción deseada: ")

        if opcion == "1":
            # llamo a la funcion y descargo
            descargar_archivo()
            print("Archivo descargado exitosamente.")

        elif opcion == "2":
            # crear db y verifico si existe
            if GestionarObra.db_existe():
                print("La base de datos ya está creada. No se realizará la creación nuevamente.")
            else:
                GestionarObra.conectar_db()
                GestionarObra.mapear_orm()
                print("Base de datos creada exitosamente.")

        elif opcion == "3":
            print("Cargando datos por favor espere...")
            # Gestionar obras
            ruta_archivo_csv = os.path.join(os.path.dirname(__file__), "descarga", "observatorio-de-obras-urbanas.csv")
            ruta_archivo_sanitizado = os.path.join("descarga", "sanitizado_observatorio-de-obras-urbanas.csv")

            try:
                if not Obra.select().exists():
                    GestionarObra.limpiar_datos(ruta_archivo_csv)
                    GestionarObra.extraer_datos(ruta_archivo_sanitizado)
                    print("Carga completada.   ")
                    print("Obras gestionadas exitosamente.")
                else:
                    print("La base de datos ya contiene registros. No se realizará la carga de datos.")
            except Exception as e:
                print("Se produjo un error al gestionar las obras:")
                print(str(e))
            # Gestionar obras
            #
            # ruta_archivo_csv = os.path.join(os.path.dirname(
            #     __file__), "descarga", "observatorio-de-obras-urbanas.csv")
            # ruta_archivo_sanitizado = os.path.join(
            #     "descarga", "sanitizado_" + "observatorio-de-obras-urbanas.csv")
            #
            # GestionarObra.limpiar_datos(ruta_archivo_csv)
            # GestionarObra.extraer_datos(ruta_archivo_sanitizado)
            # print("Obras gestionadas exitosamente.")
        elif opcion == "4":
            #obtengo los datos de la db
            GestionarObra.obtener_indicadores()
        elif opcion == "5":
            #creo una nueva obra test....
            GestionarObra.nueva_obra()
        elif opcion == "6":
            print("Saliendo del programa.")
            break

        else:
            print("Opción inválida. Por favor, ingrese una opción válida.")


if __name__ == "__main__":
    main()
