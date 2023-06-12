from peewee import *
import peewee


database = SqliteDatabase('obras_urbanas.db')


class BaseModel(Model):
    class Meta:
        database = database


class Obra(BaseModel):
    id = AutoField(primary_key=True)
    entorno = CharField()
    nombre = CharField()
    etapa = CharField()
    tipo = CharField()
    area_responsable = CharField()
    descripcion = CharField()
    monto_contrato = CharField()
    comuna = CharField()
    barrio = CharField()
    direccion = CharField()
    lat = CharField()
    lng = CharField()
    fecha_inicio = CharField()
    fecha_fin_inicial = CharField()
    plazo_meses = CharField()
    porcentaje_avance = CharField()
    imagen_1 = CharField()
    imagen_2 = CharField()
    imagen_3 = CharField()
    imagen_4 = CharField()
    licitacion_oferta_empresa = CharField()
    licitacion_anio = CharField()
    contratacion_tipo = CharField()
    nro_contratacion = CharField()
    cuit_contratista = CharField()
    beneficiarios = CharField()
    mano_obra = CharField()
    compromiso = CharField()
    destacada = CharField()
    ba_elige = CharField()
    link_interno = CharField()
    pliego_descarga = CharField()
    expediente_numero = CharField()
    estudio_ambiental_descarga = CharField()
    financiamiento = CharField()


try:
    database.connect()
except peewee.OperationalError:
    # exelente! esta la db
    print("La base de datos ya existe. No se creará una nueva.")
else:
    # creando la db

    database.create_tables([Obra])
    print("Se ha creado la base de datos y las tablas.")
