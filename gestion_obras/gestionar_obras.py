import pandas as pd
from peewee import *
from dao.modelo_orm import Entorno, Etapa, Imagenes, Tipo, AreaResponsable, Direccion, Licitacion, Contratacion, \
    Beneficiario, \
    ManoObra, Compromiso, Financiamiento, Obra, database
import os


class GestionarObra:
    def __init__(self):
        pass

    @classmethod
    def extraer_datos(cls, archivo_csv):
        database.close()
        database.connect()
        ruta_archivo_sanitizado = os.path.join("descarga", os.path.splitext(os.path.basename(archivo_csv))[0] + ".csv")
        # Leer el archivo CSV con pandas
        df = pd.read_csv(ruta_archivo_sanitizado)

        # Ciclo for para chequear las columnas
        total_filas = len(df)
        for i, (_, row) in enumerate(df.iterrows(), start=1):
            # Mostrar el progreso
            print(f"Procesando obra {i} de {total_filas}")

            imagen = Imagenes.create(imagen_1=row['imagen_1'], imagen_2=row['imagen_2'], imagen_3=row['imagen_3'],
                                     imagen_4=row['imagen_4'])
            # Crear una instancia para cada obra

            obra = Obra(
                entorno=Entorno.create(zona=row['entorno']),
                nombre=row['nombre'],
                etapa=Etapa.create(tipoEtapa=row['etapa']),
                tipo=Tipo.create(tipoEdificio=row['tipo']),
                area_responsable=AreaResponsable.create(ministerio=row['area_responsable']),
                descripcion=row['descripcion'],
                monto_contrato=row['monto_contrato'],
                direccion=Direccion.create(comuna=row['comuna'], barrio=row['barrio'], ubicacion=row['direccion'],
                                           lat=row['lat'], lng=row['lng']),
                fecha_inicio=row['fecha_inicio'],
                fecha_fin_inicial=row['fecha_fin_inicial'],
                plazo_meses=row['plazo_meses'],
                porcentaje_avance=row['porcentaje_avance'],
                imagen_1=imagen,
                imagen_2=imagen,
                imagen_3=imagen,
                imagen_4=imagen,
                licitacion=Licitacion.create(oferta_empresa=row['licitacion_oferta_empresa'],
                                             anio=row['licitacion_anio']),
                contratacion=Contratacion.create(tipo=row['contratacion_tipo'],
                                                 nro_contratacion=row['nro_contratacion'],
                                                 cuit_contratista=row['cuit_contratista']),
                beneficiario=Beneficiario.create(tipo=row['beneficiarios']),
                mano_obra=ManoObra.create(cantidad=row['mano_obra']),
                compromiso=Compromiso.create(descripcion=row['compromiso']),
                destacada=row['destacada'],
                ba_elige=row['ba_elige'],
                link_interno=row['link_interno'],
                pliego_descarga=row['pliego_descarga'],
                expediente_numero=row['expediente-numero'],
                estudio_ambiental_descarga=row['estudio_ambiental_descarga'],
                financiamiento=Financiamiento.create(descripcion=row['financiamiento'])
            )

            print("Guardando obra...")
            # save en db

            obra.save()
            database.close()

    @classmethod
    def mapear_orm(cls):
        # creamos las tablas
        database.create_tables([Obra])

    @classmethod
    def db_existe(cls):
        db_file = 'obras_urbanas.db'
        return os.path.exists(db_file)

    @classmethod
    def limpiar_datos(cls, archivo_csv):
        # abrir el archivo csv
        df = pd.read_csv(archivo_csv)

        # Sanitizar los null
        df = df.fillna('Sin Datos')
        df = df.where(df.notna(), None)
        df = df.replace(r'^\s*$', 'Sin Datos', regex=True)

        # salvo el archivo
        ruta_archivo_sanitizado = os.path.join("descarga", "sanitizado_" + os.path.basename(archivo_csv))
        df.to_csv(ruta_archivo_sanitizado, index=False)

        # llevo el archivo sanitizado a extraer_datos
        cls.extraer_datos(ruta_archivo_sanitizado)

    @classmethod
    def nueva_obra(cls):
        # Ingresar los datos de la obra
        entorno = input("Zona del entorno: ")
        nombre = input("Nombre de la obra: ")
        # Opciones para etapa
        print("Selecciona una opción para la etapa")
        print("1. Sin iniciar")
        print("2. Pausada")
        print("3. Finalizado")
        print("4. Mostrar más opciones")
        opcion_etapa = input("Opción: ")

        if opcion_etapa == "1":
            etapa = "Sin iniciar"
        elif opcion_etapa == "2":
            etapa = "Proyecto"
        elif opcion_etapa == "3":
            etapa = "Finalizado"
        elif opcion_etapa == "4":
            # Mostrar más opciones
            print("5. Proyecto finalizado")
            print("6. Proyecto")
            print("7. Prox. Licitación")
            print("8. Proc. Adm")
            print("9. Neutralizada")
            print("10. Licitación")
            print("11. Inicial")
            print("12. Etapa 3 - frente 1")
            print("13. En proyecto")
            print("14. En obra")
            print("15. En licitación")
            print("16. En ejecución")
            print("17. Desestimada")
            print("18. Adjudicada")
            opcion_etapa_mas = input("Opción: ")

            if opcion_etapa_mas == "5":
                etapa = "Proyecto finalizado"
            elif opcion_etapa_mas == "6":
                etapa = "Pausada"
            elif opcion_etapa_mas == "7":
                etapa = "Prox. Licitación"
            elif opcion_etapa_mas == "8":
                etapa = "Proc. Adm"
            elif opcion_etapa_mas == "9":
                etapa = "Neutralizada"
            elif opcion_etapa_mas == "10":
                etapa = "Licitación"
            elif opcion_etapa_mas == "11":
                etapa = "Inicial"
            elif opcion_etapa_mas == "12":
                etapa = "Etapa 3 - frente 1"
            elif opcion_etapa_mas == "13":
                etapa = "En proyecto"
            elif opcion_etapa_mas == "14":
                etapa = "En obra"
            elif opcion_etapa_mas == "15":
                etapa = "En licitación"
            elif opcion_etapa_mas == "16":
                etapa = "En ejecución"
            elif opcion_etapa_mas == "17":
                etapa = "Desestimada"
            elif opcion_etapa_mas == "18":
                etapa = "Adjudicada"
            else:
                etapa = "Sin Datos"
        else:
            etapa = "Sin Datos"
        # Opciones para tipo
        print("Selecciona una opción para el tipo")
        print("1. Sin Datos")
        print("2. Infraestructura")
        print("3. Hidráulica e Infraestructura/ Espacio Público")
        print("4. Instalaciones")
        print("5. Espacio Público")
        opcion_tipo = input("Opción: ")

        if opcion_tipo == "1":
            tipo = "Sin Datos"
        elif opcion_tipo == "2":
            tipo = "Infraestructura"
        elif opcion_tipo == "3":
            tipo = "Hidráulica e Infraestructura/ Espacio Público"
        elif opcion_tipo == "4":
            tipo = "Instalaciones"
        elif opcion_tipo == "5":
            tipo = "Espacio Público"
        else:
            tipo = "Sin Datos"
        area_responsable = input("Área responsable: ")
        descripcion = input("Descripción: ")
        monto_contrato = input("Monto de contrato: ")
        comuna = input("Comuna: ")
        barrio = input("Barrio: ")
        direccion = input("Dirección: ")
        lat = input("Latitud: ")
        lng = input("Longitud: ")
        fecha_inicio = input("Fecha de inicio: ")
        fecha_fin_inicial = input("Fecha de finalización inicial: ")
        plazo_meses = input("Plazo en meses: ")
        porcentaje_avance = input("Porcentaje de avance: ")
        agregar_imagenes = input("¿Desea agregar imágenes? (Si/No): ")
        if agregar_imagenes.lower() == "si":
            imagen_1 = input("Imagen 1: ")
            imagen_2 = input("Imagen 2: ")
            imagen_3 = input("Imagen 3: ")
            imagen_4 = input("Imagen 4: ")
        else:
            imagen_1 = "Sin Datos"
            imagen_2 = "Sin Datos"
            imagen_3 = "Sin Datos"
            imagen_4 = "Sin Datos"
        licitacion_oferta_empresa = input("Licitación oferta empresa: ")
        licitacion_anio = input("Año de licitación: ")
        contratacion_tipo = input("Tipo de contratación: ")
        nro_contratacion = input("Número de contratación: ")
        cuit_contratista = input("CUIT del contratista: ")
        beneficiarios = input("Beneficiarios: ")
        mano_obra = input("Mano de obra: ")
        compromiso = input("Compromiso: ")
        destacada = input("Destacada: ")
        ba_elige = input("BA elige: ")
        link_interno = input("Link interno: ")
        pliego_descarga = input("Descarga de pliego: ")
        expediente_numero = input("Número de expediente: ")
        estudio_ambiental_descarga = input("Descarga de estudio ambiental: ")
        financiamiento = input("Financiamiento: ")
        imagenes = Imagenes.create(imagen_1=imagen_1, imagen_2=imagen_2, imagen_3=imagen_3, imagen_4=imagen_4)
        # Verifico si ingreso un campo vacio y le doy una leyenda "Sin Datos"
        if entorno.strip() == "":
            entorno = "Sin Datos"
        if nombre.strip() == "":
            nombre = "Sin Datos"
        if area_responsable.strip() == "":
            area_responsable = "Sin Datos"

        if descripcion.strip() == "":
            descripcion = "Sin Datos"

        if monto_contrato.strip() == "":
            monto_contrato = "Sin Datos"

        if comuna.strip() == "":
            comuna = "Sin Datos"

        if barrio.strip() == "":
            barrio = "Sin Datos"

        if direccion.strip() == "":
            direccion = "Sin Datos"

        if lat.strip() == "":
            lat = "Sin Datos"

        if lng.strip() == "":
            lng = "Sin Datos"

        if fecha_inicio.strip() == "":
            fecha_inicio = "Sin Datos"

        if fecha_fin_inicial.strip() == "":
            fecha_fin_inicial = "Sin Datos"

        if plazo_meses.strip() == "":
            plazo_meses = "Sin Datos"

        if porcentaje_avance.strip() == "":
            porcentaje_avance = "Sin Datos"

        if licitacion_oferta_empresa.strip() == "":
            licitacion_oferta_empresa = "Sin Datos"

        if licitacion_anio.strip() == "":
            licitacion_anio = "Sin Datos"

        if contratacion_tipo.strip() == "":
            contratacion_tipo = "Sin Datos"

        if nro_contratacion.strip() == "":
            nro_contratacion = "Sin Datos"

        if cuit_contratista.strip() == "":
            cuit_contratista = "Sin Datos"

        if beneficiarios.strip() == "":
            beneficiarios = "Sin Datos"

        if mano_obra.strip() == "":
            mano_obra = "Sin Datos"

        if compromiso.strip() == "":
            compromiso = "Sin Datos"

        if destacada.strip() == "":
            destacada = "Sin Datos"

        if ba_elige.strip() == "":
            ba_elige = "Sin Datos"

        if link_interno.strip() == "":
            link_interno = "Sin Datos"

        if pliego_descarga.strip() == "":
            pliego_descarga = "Sin Datos"

        if expediente_numero.strip() == "":
            expediente_numero = "Sin Datos"

        if estudio_ambiental_descarga.strip() == "":
            estudio_ambiental_descarga = "Sin Datos"

        if financiamiento.strip() == "":
            financiamiento = "Sin Datos"

        # Crear instancia de obra
        database.close()
        database.connect()
        obra = Obra(
            entorno=Entorno.create(zona=entorno),
            nombre=nombre,
            etapa=Etapa.create(tipoEtapa=etapa),
            tipo=Tipo.create(tipoEdificio=tipo),
            area_responsable=AreaResponsable.create(ministerio=area_responsable),
            descripcion=descripcion,
            monto_contrato=monto_contrato,
            comuna=Comuna.create(nombre=comuna),
            barrio=Barrio.create(nombre=barrio),
            direccion=Direccion.create(ubicacion=direccion, lat=lat, lng=lng),
            fecha_inicio=fecha_inicio,
            fecha_fin_inicial=fecha_fin_inicial,
            plazo_meses=plazo_meses,
            porcentaje_avance=porcentaje_avance,
            imagen_1=imagenes,
            imagen_2=imagenes,
            imagen_3=imagenes,
            imagen_4=imagenes,
            licitacion=Licitacion.create(oferta_empresa=licitacion_oferta_empresa, anio=licitacion_anio),
            contratacion=Contratacion.create(tipo=contratacion_tipo, nro_contratacion=nro_contratacion,
                                             cuit_contratista=cuit_contratista),
            beneficiario=Beneficiario.create(tipo=beneficiarios),
            mano_obra=ManoObra.create(cantidad=mano_obra),
            compromiso=Compromiso.create(descripcion=compromiso),
            destacada=destacada,
            ba_elige=ba_elige,
            link_interno=link_interno,
            pliego_descarga=pliego_descarga,
            expediente_numero=expediente_numero,
            estudio_ambiental_descarga=estudio_ambiental_descarga,
            financiamiento=Financiamiento.create(descripcion=financiamiento)
        )
        obra.save()
        database.close()
        print("Obra creada exitosamente.")

    @staticmethod
    def obtener_indicadores():
        database.close()
        database.connect()
        obras = Obra.select()
        color_cyan = '\033[96m'
        color_reset = '\033[0m'
        total_obras = len(obras)
        porcentaje_avance_values = [obra.porcentaje_avance for obra in obras]
        porcentaje_avance_filtered = [float(obra.porcentaje_avance) for obra in obras if
                                      isinstance(obra.porcentaje_avance,
                                                 (int, float)) and 0 <= obra.porcentaje_avance <= 100]
        #  print("Valores de porcentaje_avance:", porcentaje_avance_values)
        # print("Valores filtrados:", porcentaje_avance_filtered)

        porcentaje_avance_total = sum(porcentaje_avance_filtered)
        porcentaje_avance_promedio = porcentaje_avance_total / total_obras if total_obras > 0 else 0
        print("")
        # listado de areas responsables
        areas_responsables = AreaResponsable.select(AreaResponsable.ministerio).distinct()
        print(f"{color_cyan}Listado de todas las áreas responsables:{color_reset}")
        for area in areas_responsables:
            print(f"Responsables: {area.ministerio}")

        print("")
        # listado de los tipos de obra
        tipos_obra = [(obra.id, obra.nombre) for obra in Obra.select()]
        tipos_obra = sorted(list(set(tipos_obra)), key=lambda x: x[0])  # Ordenar por el primer elemento (ID)
        print(f"{color_cyan}Listado de todos los tipos de obra:{color_reset}")
        for tipo in tipos_obra:
            print(f"ID: {tipo[0]}, Nombre de la obra: {tipo[1]}")
        print("")

        # Listado de todos los barrios pertenecientes a las comunas 1, 2 y 3
        comunas = [1, 2, 3]
        barrios = [obra.direccion.barrio for obra in
                   Obra.select().join(Direccion).where(Direccion.id << comunas)]
        barrios = list(set(barrios))
        print(f"{color_cyan}Listado de todos los barrios pertenecientes a las comunas 1, 2 y 3:{color_reset} ")
        for barrio in barrios:
            print(barrio)
        print("")
        # cantidad de obras "FINALIZADAS" en comuna 1
        cantidad_obras_finalizadas_comuna1 = (
            Obra.select()
                .join(Etapa, JOIN.INNER, on=(Obra.etapa_id == Etapa.id))
                .join(Direccion, JOIN.INNER, on=(Etapa.id == Direccion.id))
                .where(Direccion.comuna == 1, Etapa.tipoEtapa == "Finalizada")
                .count()
        )
        print(f"{color_cyan}Cantidad de obras 'Finalizadas' en la comuna 1:{color_reset} {cantidad_obras_finalizadas_comuna1}")
        print("")
        # cantidad de obras finalizadas con plazo 24 meses

        cantidad_obras_finalizadas_plazo_24m = Obra.select().join(Etapa).where(Etapa.tipoEtapa == "Finalizada",
                                                                   Obra.plazo_meses <= 24).count()
        print(
            f"{color_cyan}Cantidad de obras 'Finalizadas' en un plazo menor o igual a 24 meses: {color_reset}{cantidad_obras_finalizadas_plazo_24m}")


        print(" ")
        print(f"{color_cyan}Total de obras:{color_reset} {total_obras}")
        print(f"{color_cyan}Porcentaje de avance promedio en todas las obras:{color_reset} {porcentaje_avance_promedio}")
        print(" ")
        database.close()
        return obras
