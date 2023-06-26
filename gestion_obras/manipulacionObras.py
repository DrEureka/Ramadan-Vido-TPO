from dao.modelo_orm import Entorno, Etapa, Tipo, AreaResponsable, Direccion, Licitacion, Contratacion, Beneficiario, \
    ManoObra, Compromiso, Financiamiento, Obra, database
from peewee import fn


class Obras:
    def __init__(self, obra, tipo_etapa, porcentajeAvance) -> None:
        self.tipo_etapa = tipo_etapa
        self.porcentaje_avance = porcentajeAvance

    #  @property
    #  def avance(self):
    #      return self.etapa.tipoEtapa

    @property
    def porcentajeAvance(self):
        if self.etapa.tipoEtapa == 'Sin iniciar':
            self.porcentaje_avance = 0
            self.save()
            return 0

        elif self.etapa.tipoEtapa == 'Inicio de contratación':
            Obra.porcentaje_avance = 10
            Obra.porcentaje_avance.save()
            return 10
        elif self.etapa.tipoEtapa == 'Adjudicación de obra':
            Obra.porcentaje_avance = 20
            Obra.porcentaje_avance.save()
            return 20
        elif self.etapa.tipoEtapa == 'Inicio de obra':
            Obra.porcentaje_avance = 30
            Obra.porcentaje_avance.save()
            return 30
        elif self.etapa.tipoEtapa == 'Actualización de porcentaje de avance':
            Obra.porcentaje_avance = 40
            Obra.porcentaje_avance.save()
            return 40
        elif self.etapa.tipoEtapa == 'Incremento de plazo':
            Obra.porcentaje_avance = 60
            Obra.porcentaje_avance.save()
            return 60
        elif self.etapa.tipoEtapa == 'Incremento de mano de obra':
            Obra.porcentaje_avance = 80
            Obra.porcentaje_avance.save()
            return 80
        elif self.etapa.tipoEtapa == 'Finalizada':
            Obra.porcentaje_avance = 100
            Obra.porcentaje_avance.save()
            return 100
        elif self.etapa.tipoEtapa == 'Obra rescindida':
            Obra.porcentaje_avance = 0
            Obra.porcentaje_avance.save()
            return 0
        else:
            Obra.porcentaje_avance = 0
            Obra.porcentaje_avance.save()
            return 0

    def nuevo_proyecto(self, obra, porcentaje_avance):
        print(obra)
        print(porcentaje_avance)
        if porcentaje_avance > 0:
            print('No está permitido retroceder de etapa.')
        else:
            database.close()
            database.connect()
            obra_actualizada = Obra.get_by_id(obra.id)
            Etapa.update(tipoEtapa='Proyecto').where(Etapa.id == obra_actualizada.id).execute()
            obra_actualizada.porcentaje_avance = 10
            obra_actualizada.save()
            database.close()
            print('Proyecto iniciado con éxito.')
            print("")

    def iniciar_contratacion(self, obra, porcentaje_avance):
        if porcentaje_avance > 10:
            print('No se puede retroceder el avance de la obra.')
        elif porcentaje_avance < 10:
            print('No es posible adelantarse en el avance de la obra.')
        else:
            tipo_contratacion = input('Ingrese el tipo de contrataci[on]: ')
            nro_contratacion = input('Ingrese el n[umero de contrataci[on]')
            database.close()
            database.connect()
            obra_actualizada = Obra.get_by_id(obra.id)
            Etapa.update(tipoEtapa='Inicio de contratacion').where(Etapa.id == obra_actualizada.id).execute()
            Contratacion.update(tipo=tipo_contratacion).where(Contratacion.id == obra_actualizada.id).execute()
            Contratacion.update(nro_contratacion=nro_contratacion).where(
                Contratacion.id == obra_actualizada.id).execute()
            obra_actualizada.porcentaje_avance = 20
            obra_actualizada.save()
            database.close()
            print('Avance exitoso.')
            print("")

    def adjudicar_obra(self, obra, porcentaje_avance):
        if porcentaje_avance > 20:
            print('No se puede retroceder el avance de la obra.')
            return
        elif porcentaje_avance < 20:
            print('No es posible adelantarse en el avance de la obra.')
            return
        else:
            database.close()
            database.connect()
            empresa = input('Ingrese la obra a la que desea adjudicar la empresa: ')

            try:
                empresaABuscar = Licitacion.get(Licitacion.oferta_empresa == empresa)
                print("La empresa se ha cargado con éxito")
                print(empresaABuscar)
            except Licitacion.DoesNotExist:
                print("La empresa ingresada no existe en la base de datos.")
                return

            nro_expediente = input('Ingrese el número de expediente: ')
            obra_actualizada = Obra.get_by_id(obra.id)
            Etapa.update(tipoEtapa='Adjudicacion de obra').where(Etapa.id == obra_actualizada.id).execute()
            Licitacion.update(oferta_empresa=empresa).where(Licitacion.id == obra_actualizada.id).execute()
            Obra.update(expediente_numero=nro_expediente).where(Obra.id == obra_actualizada.id).execute()
            obra_actualizada.porcentaje_avance = 30
            obra_actualizada.save()
            database.close()
            print('Avance exitoso.')
            print("")

    def iniciar_obra(self, obra):
        database.close()
        database.connect()
        # print("Dato de id", obra)

        # Valores
        destacada = input("¿La obra es destacada? (SI/NO): ")
        fecha_inicio = input("Ingrese la fecha de inicio de la obra (DD/MM/AAAA): ")
        fecha_fin_inicial = input("Ingrese la fecha de finalización inicial de la obra (DD/MM/AAAA): ")

        # obtengo listado de financiamiento
        descripciones_financiamiento = (Financiamiento
                                        .select(Financiamiento.descripcion)
                                        .distinct())

        # muestro listado de opciones
        print("Opciones de descripción de financiamiento:")
        for financiamiento in descripciones_financiamiento:
            print(financiamiento.descripcion)

        # dame datos
        descripcion_financiamiento = input("Ingrese la descripción del financiamiento: ")

        cantidad_mano_obra = input("Ingrese la cantidad de mano de obra (entero): ")

        # datos para guardar en obra
        obra.destacada = destacada
        obra.fecha_inicio = fecha_inicio
        obra.fecha_fin_inicial = fecha_fin_inicial

        # obtengo el id de obra igual a mano de obra
        mano_obra = ManoObra.get(ManoObra.id == obra)

        # actualizo obra
        mano_obra.cantidad = cantidad_mano_obra
        mano_obra.save()

        # obtengo el id de obra igual a financiamiento
        financiamiento = Financiamiento.get(Financiamiento.id == obra)

        # actualiza financiamineto
        financiamiento.descripcion = descripcion_financiamiento
        financiamiento.save()

        # guardo en base de datos
        obra.save()

        database.close()
        print("La obra ha sido modificada exitosamente.")
        print("")

    def actualizar_porcentaje_avance(self, obra, porcentaje_avance):
        database.close()
        database.connect()
        obra_actualizada = Obra.get_by_id(obra.id)
        Etapa.update(tipoEtapa='Actualización del porcentaje de avance').where(
            Etapa.id == obra_actualizada.id).execute()
        avanceActual = porcentaje_avance
        obra_actualizada.save()
        database.close()
        print('El porcentaje de avance actual de la obra es de:', avanceActual)

    print("")

    def incrementar_plazo(self, obra):
        database.close()
        database.connect()
        plazo_actual = obra.plazo_meses
        print("Plazo actual:", plazo_actual)
        nuevo_plazo = int(input("Ingrese el nuevo plazo en meses: "))

        if nuevo_plazo >= plazo_actual:
            obra.plazo_meses = nuevo_plazo
            obra.save()
            print("Plazo actualizado exitosamente.")

        else:
            print("El nuevo plazo debe ser mayor o igual al plazo actual.")
        database.close()
        print("El plazo de la obra se ha incrementado exitosamente.")
        print("")

    def incrementar_mano_obra(self, obra, porcentaje_avance, tipo_etapa):
        if self.porcentajeAvance < 60:
            print('No se puede retroceder el avance de la obra.')
        elif self.porcentajeAvance > 80:
            print('No es posible adelantarse en el avance de la obra.')
        else:
            self.etapa.tipoEtapa = 'Incremento de mano de obra'
            self.etapa.save()
            print('Avance exitoso.')
        print("")

    def finalizar_obra(self, obra, porcentaje_avance, tipo_etapa):
        database.close()
        database.connect()
        obra_actualizada = Obra.get_by_id(obra.id)
        Etapa.update(tipoEtapa='Finalizada').where(Etapa.id == obra_actualizada.id).execute()
        obra_actualizada.porcentaje_avance = 100
        obra_actualizada.save()
        database.close()
        print('Obra finalizada con éxito.')
        print("")

    def rescindir_obra(self, obra, porcentaje_avance, tipo_etapa):
        if porcentaje_avance < 0:
            print('No es posible rescindir la obra.')
        else:
            database.close()
            database.connect()
            obra_actualizada = Obra.get_by_id(obra.id)
            Etapa.update(tipoEtapa='Rescindida').where(Etapa.id == obra_actualizada.id).execute()
            obra_actualizada.porcentaje_avance = 0
            obra_actualizada.save()
            database.close()
            print('Obra rescindida con éxito.')
        print("")

    def obtener_avance_por_id(id):
        try:
            existeAvance = (
                Obra.select(Etapa.tipoEtapa).join(Etapa).where(Obra.id == id)
            )
            if existeAvance.exists():
                verAvance = existeAvance.get().etapa.tipoEtapa
                return verAvance
            else:
                return None
        except Obra.DoesNotExist:
            return None

    def obtener_avance_por_nombre(self):
        try:
            existeObra = (
                Obra.select(Obra.id, Obra.nombre, Etapa.tipoEtapa).join(Etapa).where(
                    Obra.nombre ** f'%{self}%').order_by(fn.LENGTH(Obra.nombre))
            )
            resultados = []
            for obra in existeObra:
                resultados.append({
                    'id': obra.id,
                    'nombre': obra.nombre,
                    'avance': obra.etapa.tipoEtapa
                })

            return resultados
        except Obra.DoesNotExist:
            return None
