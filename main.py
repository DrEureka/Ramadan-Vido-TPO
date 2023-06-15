from gestion_obras.gestionar_obras import GestionarObra
from descarga.descarga_csv import descargar_archivo
from dao.modelo_orm import Entorno, Etapa, Tipo, AreaResponsable, Direccion, Licitacion, Contratacion, Beneficiario, ManoObra, Compromiso, Financiamiento, Obra
import sys
import time
import os

def maquina_escribir(texto):
    for letra in texto:
        sys.stdout.write(letra)
        sys.stdout.flush()
        time.sleep(0.1)  # Ajusta el valor para controlar la velocidad de escritura

    sys.stdout.write('\n')

def print_color(text, color):
    color_reset = '\033[0m'
    print(color + text + color_reset)

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
            todoOkVerde = '\033[32m'
            print_color("Archivo descargado exitosamente.", todoOkVerde)

        elif opcion == "2":
            # crear db y verifico si existe
            if GestionarObra.db_existe():
                todoOkVerde='\033[32m'
                print_color("La base de datos ya está creada. No se realizará la creación nuevamente.", todoOkVerde)

            else:
                GestionarObra.conectar_db()
                GestionarObra.mapear_orm()
                print("Base de datos creada exitosamente.")

        elif opcion == "3":
            atencionAmarillo= '\033[33m'
            print_color("Cargando datos a la db por favor espere...", atencionAmarillo)
            # Gestionar obras
            ruta_archivo_csv = os.path.join(os.path.dirname(__file__), "descarga", "observatorio-de-obras-urbanas.csv")
            ruta_archivo_sanitizado = os.path.join("descarga", "sanitizado_observatorio-de-obras-urbanas.csv")

            try:
                if not Obra.select().exists():
                    GestionarObra.limpiar_datos(ruta_archivo_csv)
                    GestionarObra.extraer_datos(ruta_archivo_sanitizado)
                    todoOkVerde = '\033[32m'
                    print_color("Carga completada.   ", todoOkVerde)
                    print_color("Obras gestionadas exitosamente.", todoOkVerde)
                else:
                    errorRojo = '\033[31m'
                    print_color("La base de datos ya contiene registros. No se realizará la carga de datos.", errorRojo)

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


            print("Saliendo del programa.\n")
            color = '\033[32m'
            color_reset = '\033[0m'
            print("Trabajo Práctico Final Integrador 2023\n")
            print("Materia: Desarrollo de Sistemas Orientados a Objetos")
            print("Curso: 1er Año")
            print("Profesor: Eduardo Iberti")
            texto = (color + "Programa realizado por: Daniel, Ramadan.\nVido Viloria, Alessandrio Gabrielle."+color_reset)
            maquina_escribir(texto)

            break

        else:
            errorRojo = '\033[31m'
            print_color("Opción inválida. Por favor, ingrese una opción válida.", errorRojo)


if __name__ == "__main__":
    main()
