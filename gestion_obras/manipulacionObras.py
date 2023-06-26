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

    def iniciar_contratacion(self, obra, porcentaje_avance):
        if porcentaje_avance < 10:
            print('No se puede retroceder el avance de la obra.')
        elif porcentaje_avance > 10:
            print('No es posible retroceder en el avance de la obra.')
        else:
            tipo_contratacion = input('Ingrese el tipo de contrataci[on]: ')
            nro_contratacion = input('Ingrese el n[umero de contrataci[on]')
            database.close()
            database.connect()
            obra_actualizada = Obra.get_by_id(obra.id)
            Etapa.update(tipoEtapa='Inicio de contratacion').where(Etapa.id == obra_actualizada.id).execute()
            Contratacion.update(tipo=tipo_contratacion).where(Contratacion.id == obra_actualizada.id).execute()
            Contratacion.update(nro_contratacion=nro_contratacion).where(Contratacion.id == obra_actualizada.id).execute()
            obra_actualizada.porcentaje_avance = 20
            obra_actualizada.save()
            database.close()
            print('Avance exitoso.')

    def adjudicar_obra(self, obra, porcentaje_avance):
        if porcentaje_avance < 20:
            print('No se puede retroceder el avance de la obra.')
            return
        elif porcentaje_avance > 20:
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

            nro_expediente = input('Ingrese el número de contratación: ')
            obra_actualizada = Obra.get_by_id(obra.id)
            Etapa.update(tipoEtapa='Adjudicacion de obra').where(Etapa.id == obra_actualizada.id).execute()
            Licitacion.update(oferta_empresa=empresa).where(Licitacion.id == obra_actualizada.id).execute()
            Obra.update(expediente_numero=nro_expediente).where(Obra.id == obra_actualizada.id).execute()
            obra_actualizada.porcentaje_avance = 30
            obra_actualizada.save()
            database.close()
            print('Avance exitoso.')

    def iniciar_obra(self, obra):
        print("dato de id", obra)
        # valores
        destacada = input("¿La obra es destacada? (SI/NO): ")
        fecha_inicio = input("Ingrese la fecha de inicio de la obra (YYYY-MM-DD): ")
        fecha_fin_inicial = input("Ingrese la fecha de finalización inicial de la obra (YYYY-MM-DD): ")
        descripcion_financiamiento = input("Ingrese la descripción del financiamiento: ")
        cantidad_mano_obra = input("Ingrese la cantidad de mano de obra (entero): ")

        # chequear los datos para guardar
        obra.destacada = destacada
        obra.fecha_inicio = fecha_inicio
        obra.fecha_fin_inicial = fecha_fin_inicial

        # financiamiento y obra
        obra.financiamiento.descripcion = descripcion_financiamiento
        obra.mano_obra.cantidad = int(cantidad_mano_obra)

        # guardo en base
        obra.save()

        print("La obra ha sido iniciada exitosamente.")

    def actualizar_porcentaje_avance(self, obra, porcentaje_avance, tipo_etapa):
        if self.porcentajeAvance < 30:
            print('No se puede retroceder el avance de la obra.')
        elif self.porcentajeAvance > 40:
            print('No es posible adelantarse en el avance de la obra.')
        else:
            self.etapa.tipoEtapa = 'Actualización de porcentaje de avance'
            self.etapa.save()
            print('Avance exitoso.')

    def incrementar_plazo(self, obra, porcentaje_avance, tipo_etapa):
        if self.porcentajeAvance < 40:
            print('No se puede retroceder el avance de la obra.')
        elif self.porcentajeAvance > 60:
            print('No es posible adelantarse en el avance de la obra.')
        else:
            self.etapa.tipoEtapa = 'Incremento de plazo'
            self.etapa.save()
            print('Avance exitoso.')

    def incrementar_mano_obra(self, obra, porcentaje_avance, tipo_etapa):
        if self.porcentajeAvance < 60:
            print('No se puede retroceder el avance de la obra.')
        elif self.porcentajeAvance > 80:
            print('No es posible adelantarse en el avance de la obra.')
        else:
            self.etapa.tipoEtapa = 'Incremento de mano de obra'
            self.etapa.save()
            print('Avance exitoso.')

    def finalizar_obra(self, obra, porcentaje_avance, tipo_etapa):
        if porcentaje_avance < 100:
            print('No se puede retroceder el avance de la obra.')
        elif porcentaje_avance > 100:
            print('No es posible superar el máximo alcanzado en el avance.')
        else:
            database.close()
            database.connect()
            obra_actualizada = Obra.get_by_id(obra.id)
            Etapa.update(tipoEtapa='Finalizada').where(Etapa.id == obra_actualizada.id).execute()
            obra_actualizada.porcentaje_avance = 100
            obra_actualizada.save()
            database.close()
            print('Obra finalizada con éxito.')

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
