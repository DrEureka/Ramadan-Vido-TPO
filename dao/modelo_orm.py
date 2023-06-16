from peewee import *

database = SqliteDatabase('obras_urbanas.db')


class BaseModel(Model):
    class Meta:
        database = database


class Entorno(BaseModel):
    id = AutoField(primary_key=True)
    zona = CharField(null=True)


class Etapa(BaseModel):
    id = AutoField(primary_key=True)
    tipoEtapa = CharField(null=True)


class Tipo(BaseModel):
    id = AutoField(primary_key=True)
    tipoEdificio = CharField(null=True)


class AreaResponsable(BaseModel):
    id = AutoField(primary_key=True)
    ministerio = CharField(null=True)


class Direccion(BaseModel):
    id = AutoField(primary_key=True)
    ubicacion = CharField(null=True)
    lat = FloatField(null=True)
    lng = FloatField(null=True)


class Licitacion(BaseModel):
    id = AutoField(primary_key=True)
    oferta_empresa = CharField(null=True)
    anio = IntegerField(null=True)


class Contratacion(BaseModel):
    id = AutoField(primary_key=True)
    tipo = CharField(null=True)
    nro_contratacion = CharField(null=True)
    cuit_contratista = IntegerField(null=True)


class Beneficiario(BaseModel):
    id = AutoField(primary_key=True)
    tipo = CharField(null=True)


class ManoObra(BaseModel):
    id = AutoField(primary_key=True)
    cantidad = CharField(null=True)


class Compromiso(BaseModel):
    id = AutoField(primary_key=True)
    descripcion = CharField(null=True)


class Financiamiento(BaseModel):
    id = AutoField(primary_key=True)
    descripcion = CharField(null=True)


class Obra(BaseModel):
    id = AutoField(primary_key=True)
    nombre = CharField(null=True)
    descripcion = CharField(null=True)
    monto_contrato = IntegerField(null=True)
    fecha_inicio = DateField(null=True)
    fecha_fin_inicial = DateField(null=True)
    plazo_meses = IntegerField(null=True)
    porcentaje_avance = IntegerField(null=True)
    imagen_1 = CharField(null=True)
    imagen_2 = CharField(null=True)
    imagen_3 = CharField(null=True)
    imagen_4 = CharField(null=True)
    destacada = CharField(null=True)
    ba_elige = CharField(null=True)
    link_interno = CharField(null=True)
    pliego_descarga = CharField(null=True)
    expediente_numero = CharField(null=True)
    estudio_ambiental_descarga = CharField(null=True)
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
    with database.atomic():
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
