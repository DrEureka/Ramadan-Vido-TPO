from gestion_obras.gestionar_obras import GestionarObra
from gestion_obras.manipulacionObras import Obras
from descarga.descarga_csv import descargar_archivo

from gestion_obras.manipulacionObras import Entorno, Etapa, Tipo, AreaResponsable, Direccion, Licitacion, Contratacion, Beneficiario, ManoObra, Compromiso, Financiamiento, Obra

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
    print("6. Obtener avance de una obra")
    print("7. Editar avance de obra")
    print("8. Salir")

def subMenuObAvance():
    print('Elija una opción: ')
    print('1. filtrar avance por id')
    print('2. filtrar por nombre de obra')
    print('3. Atras')

def subMenuEdAvance():
    print('Elija una opción:')
    print('1. Coloque el id de la obra a la que desea editar el avance')
    print('2. Atras')

def subMenuAvances():
    print('Elija una opción:')
    print('1. Nuevo proyecto')
    print('2. Iniciar contrataci[on]')
    print('3. Adjudicar obra')
    print('4. Iniciar obra')
    print('5. Actualizar porcentaje de avance')
    print('6. Incrementar plazo')
    print('7. Incrementar mano de obra')
    print('8. Finalizar obra')
    print('9. Rescindir obra')
    print('0. Atras')

def main():
    opcion = None

    while opcion != "8":
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
                 #   GestionarObra.extraer_datos(ruta_archivo_sanitizado)
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
            opcionOb = None
            while opcionOb != "3":
                subMenuObAvance()
                opcionOb = input("Ingrese la opción deseada: ")
                if opcionOb == "1":
                    idColocar = int(input("Ingrese el id: "))
                    idAvance = Obras.obtener_avance_por_id(idColocar)
                    print(idAvance)
                elif opcionOb == "2":
                    buscarNombre = input("Ingrese el nombre de la obra: ")

                    print()
                    buscarObra = Obras.obtener_avance_por_nombre(buscarNombre)
                    cantidadBusqueda = len(buscarObra)

                    print("Se encontraron Registros: ", cantidadBusqueda)
                    if buscarObra:
                        for resultado in buscarObra:
                            print(f"ID: {resultado['id']}")
                            print(f"Nombre: {resultado['nombre']}")
                            print(f"Avance: {resultado['avance']}")
                            print()
                    else:
                        print("No se encontraron resultados.")


        elif opcion == "7":
            opcionEd = None
            while opcionEd != "2":
                subMenuEdAvance()
                opcionEd = input("Ingrese la opción deseada: ")
                if opcionEd == "1":
                    idColocar = int(input("Ingrese el id:"))
                    try:

                        obra = Obra.select().join(Etapa).where(Obra.id == idColocar).get()
                        porcentaje_avance = obra.porcentaje_avance
                        tipo_etapa = obra.etapa.tipoEtapa


                    except Exception as i:
                        print("No se encontró ninguna obra con el ID especificado.", i)
                        return
                    if obra:
                        obras = Obras(obra, tipo_etapa, porcentaje_avance)
                        opcionAv = None
                        while opcionAv != "0":
                            subMenuAvances()
                            opcionAv = input('Ingrese la opción deseada: ')
                            if opcionAv == "1":
                                obras.nuevo_proyecto(obra, porcentaje_avance)
                            elif opcionAv == "2":
                                obras.iniciar_contratacion(obra, porcentaje_avance)
                            elif opcionAv == "3":
                                obras.adjudicar_obra(obra, porcentaje_avance)
                            elif opcionAv == "4":
                                obras.iniciar_obra(obra)
                            elif opcionAv == "5":
                                obras.actualizar_porcentaje_avance()
                            elif opcionAv == "6":
                                obras.incrementar_plazo()
                            elif opcionAv == "7":
                                obras.incrementar_mano_obra()
                            elif opcionAv == "8":
                                obras.finalizar_obra()
                            elif opcionAv == "9":
                                obras.rescindir_obra()
                            else:
                                errorRojo = '\033[31m'
                                print_color("Opción inválida. Por favor, ingrese una opción válida.", errorRojo)
                    else:
                        print("La obra no existe")

        elif opcion == "8":
            print("Saliendo del programa.\n")
            color = '\033[32m'
            color_reset = '\033[0m'
            print("Trabajo Práctico Final Integrador 2023\n")
            print("Materia: Desarrollo de Sistemas Orientados a Objetos")
            print("Curso: 1er Año")
            print("Profesor: Eduardo Iberti")
            texto = (color + "Programa realizado por: Daniel, Ramadan.\nAlessandrio Gabrielle, Vido Viloria."+color_reset)
            maquina_escribir(texto)

            break

        else:
            errorRojo = '\033[31m'
            print_color("Opción inválida. Por favor, ingrese una opción válida.", errorRojo)


if __name__ == "__main__":
    main()