from entregaalpes.seedwork.aplicacion.dto import Mapeador as AppMap
from entregaalpes.seedwork.dominio.repositorios import Mapeador as RepMap
from entregaalpes.modulos.solicitudes.dominio.entidades import Solicitud
from entregaalpes.modulos.solicitudes.dominio.objetos_valor import Segmento, Leg
from .dto import SolicitudDTO

from datetime import datetime

class MapeadorSolicitudDTOJson(AppMap):
    
    def externo_a_dto(self, externo: dict) -> SolicitudDTO:
        reserva_dto = SolicitudDTO()

        return reserva_dto

    def dto_a_externo(self, dto: SolicitudDTO) -> dict:
        return dto.__dict__

class MapeadorSolicitud(RepMap):
    _FORMATO_FECHA = '%Y-%m-%dT%H:%M:%SZ'

    def obtener_tipo(self) -> type:
        return Solicitud.__class__

    def locacion_a_dict(self, locacion):
        if not locacion:
            return dict(codigo=None, nombre=None, fecha_actualizacion=None, fecha_creacion=None, cliente=None)
        
        return dict(
                    codigo=locacion.codigo
                ,   nombre=locacion.nombre
                ,   fecha_actualizacion=locacion.fecha_actualizacion.strftime(self._FORMATO_FECHA)
                ,   fecha_creacion=locacion.fecha_creacion.strftime(self._FORMATO_FECHA)
                ,   cliente=locacion.cliente
        )
        

    def entidad_a_dto(self, entidad: Solicitud) -> SolicitudDTO:
        
        fecha_creacion = entidad.fecha_creacion.strftime(self._FORMATO_FECHA)
        fecha_actualizacion = entidad.fecha_actualizacion.strftime(self._FORMATO_FECHA)
        _id = str(entidad.id)
        
        return Solicitud(fecha_creacion, fecha_actualizacion, _id)

    def dto_a_entidad(self, dto: SolicitudDTO) -> Solicitud:
        solicitud = Solicitud()
        
        return solicitud



