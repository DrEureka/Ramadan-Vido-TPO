from dao.modelo_orm import Entorno, Etapa, Tipo, AreaResponsable, Direccion, Licitacion, Contratacion, Beneficiario, \
    ManoObra, Compromiso, Financiamiento, Obra, database
from peewee import fn




class Obras():
    def __init__(self, avance, porcentajeAvance) -> None:
        self.avance = avance
        self.porcentajeAvance = porcentajeAvance

    @property
    def avance(self):
        return self.etapa.tipoEtapa

    @property
    def porcentajeAvance(self):
        if self.etapa.tipoEtapa == 'Nuevo proyecto':
            Obra.porcentaje_avance = 0
            Obra.porcentaje_avance.save()
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

    def nuevo_proyecto(self):
        if self.porcentajeAvance > 0:
            print('No está permitido retroceder de etapa.')
        else:
            self.etapa.tipoEtapa = 'Nuevo proyecto'
            self.etapa.save()
            print('Proyecto iniciado con éxito.')

    def iniciar_contratacion(self):
        if self.porcentajeAvance < 0:
            print('No se puede retroceder el avance de la obra.')
        elif self.porcentajeAvance > 10:
            print('No es posible adelantarse en el avance de la obra.')
        else:
            self.etapa.tipoEtapa = 'Iniciar contratación'
            self.etapa.save()
            print('Avance exitoso.')

    def adjudicar_obra(self):
        if self.porcentajeAvance < 10:
            print('No se puede retroceder el avance de la obra.')
        elif self.porcentajeAvance > 20:
            print('No es posible adelantarse en el avance de la obra.')
        else:
            self.etapa.tipoEtapa = 'Adjudicación de obra'
            self.etapa.save()
            print('Avance exitoso.')

    def iniciar_obra(self):
        if self.porcentajeAvance < 20:
            print('No se puede retroceder el avance de la obra.')
        elif self.porcentajeAvance > 30:
            print('No es posible adelantarse en el avance de la obra.')
        else:
            self.etapa.tipoEtapa = 'Inicio de obra'
            self.etapa.save()
            print('Avance exitoso.')

    def actualizar_porcentaje_avance(self):
        if self.porcentajeAvance < 30:
            print('No se puede retroceder el avance de la obra.')
        elif self.porcentajeAvance > 40:
            print('No es posible adelantarse en el avance de la obra.')
        else:
            self.etapa.tipoEtapa = 'Actualización de porcentaje de avance'
            self.etapa.save()
            print('Avance exitoso.')

    def incrementar_plazo(self):
        if self.porcentajeAvance < 40:
            print('No se puede retroceder el avance de la obra.')
        elif self.porcentajeAvance > 60:
            print('No es posible adelantarse en el avance de la obra.')
        else:
            self.etapa.tipoEtapa = 'Incremento de plazo'
            self.etapa.save()
            print('Avance exitoso.')

    def incrementar_mano_obra(self):
        if self.porcentajeAvance < 60:
            print('No se puede retroceder el avance de la obra.')
        elif self.porcentajeAvance > 80:
            print('No es posible adelantarse en el avance de la obra.')
        else:
            self.etapa.tipoEtapa = 'Incremento de mano de obra'
            self.etapa.save()
            print('Avance exitoso.')

    def finalizar_obra(self):
        if self.porcentajeAvance < 80:
            print('No se puede retroceder el avance de la obra.')
        elif self.porcentajeAvance > 100:
            print('No es posible superar el máximo alcanzado en el avance.')
        else:
            self.etapa.tipoEtapa = 'Finalizada'
            self.etapa.save()
            print('Avance exitoso.')

    def rescindir_obra(self):
        if self.porcentajeAvance < 0:
            print('No es posible rescindir la obra.')
        else:
            self.etapa.tipoEtapa = 'Obra rescindida'
            self.etapa.save()
            print('Obra rescindida.')

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

    def obtener_avance_por_nombre(nombre):
        try:
            existeObra = (
                Obra.select(Obra.id, Obra.nombre, Etapa.tipoEtapa).join(Etapa).where(Obra.nombre ** f'%{nombre}%').order_by(fn.LENGTH(Obra.nombre))
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