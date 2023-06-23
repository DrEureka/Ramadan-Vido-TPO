from dao.modelo_orm import Entorno, Etapa, Tipo, AreaResponsable, Direccion, Licitacion, Contratacion, Beneficiario, \
    ManoObra, Compromiso, Financiamiento, Obra, database

class Obrasee():
    def __init__(self) -> None:
        pass

    def nuevo_proyecto(self):
        pass

    def iniciar_contratacion(self):
        pass

    def adjudicar_obra(self):
        pass

    def iniciar_obra(self):
        pass

    def actualizar_porcentaje_avance(self):
        pass

    def incrementar_plazo(self):
        pass

    def incrementar_mano_obra(self):
        pass

    def finalizar_obra(self):
        pass

    def rescindir_obra(self):
        pass

    def obtener_avance_por_id(id):
        try:
            avance = Obra.select(Obra.etapa).where(Obra.id == id).scalar()
            return avance
        except avance.DoesNotExist:
            return None