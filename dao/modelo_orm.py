from peewee import *

database = SqliteDatabase('obras_urbanas.db')


class BaseModel(Model):
    class Meta:
        database = database


class Entorno(BaseModel):
    id = AutoField(primary_key=True)
    nombre = CharField()


class Etapa(BaseModel):
    id = AutoField(primary_key=True)
    nombre = CharField()


class Tipo(BaseModel):
    id = AutoField(primary_key=True)
    nombre = CharField()


class AreaResponsable(BaseModel):
    id = AutoField(primary_key=True)
    nombre = CharField()


class Direccion(BaseModel):
    id = AutoField(primary_key=True)
    nombre = CharField()
    lat = CharField()
    lng = CharField()


class Licitacion(BaseModel):
    id = AutoField(primary_key=True)
    oferta_empresa = CharField()
    anio = CharField()


class Contratacion(BaseModel):
    id = AutoField(primary_key=True)
    tipo = CharField()
    nro_contratacion = CharField()
    cuit_contratista = CharField()


class Beneficiario(BaseModel):
    id = AutoField(primary_key=True)
    nombre = CharField()


class ManoObra(BaseModel):
    id = AutoField(primary_key=True)
    descripcion = CharField()


class Compromiso(BaseModel):
    id = AutoField(primary_key=True)
    descripcion = CharField()


class Financiamiento(BaseModel):
    id = AutoField(primary_key=True)
    descripcion = CharField()


class Obra(BaseModel):
    id = AutoField(primary_key=True)
    nombre = CharField()
    descripcion = CharField()
    monto_contrato = CharField()
    fecha_inicio = CharField()
    fecha_fin_inicial = CharField()
    plazo_meses = CharField()
    porcentaje_avance = CharField()
    imagen_1 = CharField()
    imagen_2 = CharField()
    imagen_3 = CharField()
    imagen_4 = CharField()
    destacada = CharField()
    ba_elige = CharField()
    link_interno = CharField()
    pliego_descarga = CharField()
    expediente_numero = CharField()
    estudio_ambiental_descarga = CharField()
    financiamiento = ForeignKeyField(Financiamiento, backref='obras')
    entorno = ForeignKeyField(Entorno, backref='obras')
    etapa = ForeignKeyField(Etapa, backref='obras')
    tipo = ForeignKeyField(Tipo, backref='obras')
    area_responsable = ForeignKeyField(AreaResponsable, backref='obras')
    direccion = ForeignKeyField(Direccion, backref='obras')
    licitacion = ForeignKeyField(Licitacion, backref='obras')
    contratacion = ForeignKeyField(Contratacion, backref='obras')
    beneficiario = ForeignKeyField(Beneficiario, backref='obras')
    mano_obra = ForeignKeyField(ManoObra, backref='obras')
    compromiso = ForeignKeyField(Compromiso, backref='obras')


def create_tables():
    with database:
        database.create_tables([
            Entorno, Etapa, Tipo, AreaResponsable, Direccion, Licitacion, Contratacion,
            Beneficiario, ManoObra, Compromiso, Financiamiento, Obra
        ])


try:
    database.connect()
except OperationalError:
    print("La base de datos ya existe. No se creará una nueva.")
else:
    create_tables()
    print("Se ha creado la base de datos y las tablas.")