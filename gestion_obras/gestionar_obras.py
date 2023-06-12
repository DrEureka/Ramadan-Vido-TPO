import pandas as pd
from peewee import *
from dao.modelo_orm import Obra, database
import os

class GestionarObra:
    @classmethod
    def extraer_datos(cls, archivo_csv):
        ruta_archivo_sanitizado = os.path.join("descarga", os.path.splitext(os.path.basename(archivo_csv))[0] + ".csv")
        # Leer el archivo CSV con pandas
        df = pd.read_csv(ruta_archivo_sanitizado)


        # ciclo for para chequear las columnas
        for _, row in df.iterrows():

            # crear una instancia para cada obra
            obra = Obra(
                entorno=row['entorno'],
                nombre=row['nombre'],
                etapa=row['etapa'],
                tipo=row['tipo'],
                area_responsable=row['area_responsable'],
                descripcion=row['descripcion'],
                monto_contrato=row['monto_contrato'],
                comuna=row['comuna'],
                barrio=row['barrio'],
                direccion=row['direccion'],
                lat=row['lat'],
                lng=row['lng'],
                fecha_inicio=row['fecha_inicio'],
                fecha_fin_inicial=row['fecha_fin_inicial'],
                plazo_meses=row['plazo_meses'],
                porcentaje_avance=row['porcentaje_avance'],
                imagen_1=row['imagen_1'],
                imagen_2=row['imagen_2'],
                imagen_3=row['imagen_3'],
                imagen_4=row['imagen_4'],
                licitacion_oferta_empresa=row['licitacion_oferta_empresa'],
                licitacion_anio=row['licitacion_anio'],
                contratacion_tipo=row['contratacion_tipo'],
                nro_contratacion=row['nro_contratacion'],
                cuit_contratista=row['cuit_contratista'],
                beneficiarios=row['beneficiarios'],
                mano_obra=row['mano_obra'],
                compromiso=row['compromiso'],
                destacada=row['destacada'],
                ba_elige=row['ba_elige'],
                link_interno=row['link_interno'],
                pliego_descarga=row['pliego_descarga'],
                expediente_numero=row['expediente-numero'],
                estudio_ambiental_descarga=row['estudio_ambiental_descarga'],
                financiamiento=row['financiamiento']
            )

            # save en db
            obra.save()

    @classmethod
    def conectar_db(cls):
        # conecto
        database = SqliteDatabase('obras_urbanas.db')
        database.connect()

    @classmethod
    def mapear_orm(cls):
        # creamos las tablas
        database.create_tables([Obra])

    @classmethod
    def limpiar_datos(cls, archivo_csv):
        # abrir el archivo csv
        df = pd.read_csv(archivo_csv)

        # Sanitizar los null
        df = df.replace(r'^\s*$', 'Sin Datos', regex=True)

        # salvo el archivo
        ruta_archivo_sanitizado = os.path.join("descarga", "sanitizado_" + os.path.basename(archivo_csv))
        df.to_csv(ruta_archivo_sanitizado, index=False)

        # llevo el archivo sanitizado a extraer_datos
        cls.extraer_datos(ruta_archivo_sanitizado)
        
    @classmethod
    def nueva_obra(cls):
        # ingrese los datos de la obra
        entorno = input("Entorno: ")
        nombre = input("Nombre: ")
        etapa = input("Etapa: ")
        tipo = input("Tipo: ")
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
        imagen_1 = input("Imagen 1: ")
        imagen_2 = input("Imagen 2: ")
        imagen_3 = input("Imagen 3: ")
        imagen_4 = input("Imagen 4: ")
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

        # creo instancia de obra
        obra = Obra(
            entorno=entorno,
            nombre=nombre,
            etapa=etapa,
            tipo=tipo,
            area_responsable=area_responsable,
            descripcion=descripcion,
            monto_contrato=monto_contrato,
            comuna=comuna,
            barrio=barrio,
            direccion=direccion,
            lat=lat,
            lng=lng,
            fecha_inicio=fecha_inicio,
            fecha_fin_inicial=fecha_fin_inicial,
            plazo_meses=plazo_meses,
            porcentaje_avance=porcentaje_avance,
            imagen_1=imagen_1,
            imagen_2=imagen_2,
            imagen_3=imagen_3,
            imagen_4=imagen_4,
            licitacion_oferta_empresa=licitacion_oferta_empresa,
            licitacion_anio=licitacion_anio,
            contratacion_tipo=contratacion_tipo,
            nro_contratacion=nro_contratacion,
            cuit_contratista=cuit_contratista,
            beneficiarios=beneficiarios,
            mano_obra=mano_obra,
            compromiso=compromiso,
            destacada=destacada,
            ba_elige=ba_elige,
            link_interno=link_interno,
            pliego_descarga=pliego_descarga,
            expediente_numero=expediente_numero,
            estudio_ambiental_descarga=estudio_ambiental_descarga,
            financiamiento=financiamiento
        )

        # guardo la nueva obra
        obra.save()


        return obra


    
    @classmethod
    def obtener_indicadores(cls):
        # tomo las obras de la db
        obras = Obra.select()

        # contamos obras y calculamos porcentaje de avance promedio
        total_obras = len(obras)
        porcentaje_avance_promedio = sum([float(obra.porcentaje_avance) for obra in obras if obra.porcentaje_avance.isdigit()]) / total_obras
        color_cyan = '\033[96m'
        color_reset = '\033[0m'
        print(" ")
        print("Indicadores:")
        print(f"{color_cyan}Total de obras: {total_obras}{color_reset}")
        print(f"{color_cyan}Porcentaje de avance promedio: {porcentaje_avance_promedio}{color_reset}")
        print(" ")
        return obras