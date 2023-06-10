from peewee import *
import peewee
import os

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
    descripcion = TextField()
    monto_contrato = FloatField()
    comuna = IntegerField()
    barrio = CharField()
    direccion = CharField()
    lat = FloatField()
    lng = FloatField()
    fecha_inicio = DateField()
    fecha_fin_inicial = DateField()
    plazo_meses = IntegerField()
    porcentaje_avance = IntegerField()
    imagen_1 = CharField()
    imagen_2 = CharField()
    imagen_3 = CharField()
    imagen_4 = CharField()
    licitacion_oferta_empresa = CharField()
    licitacion_anio = IntegerField()
    contratacion_tipo = CharField()
    nro_contratacion = CharField()
    cuit_contratista = CharField()
    beneficiarios = IntegerField()
    mano_obra = IntegerField()
    compromiso = IntegerField()
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
