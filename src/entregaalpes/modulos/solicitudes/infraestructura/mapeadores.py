""" Mapeadores para la capa de infrastructura del dominio de vuelos

En este archivo usted encontrará los diferentes mapeadores
encargados de la transformación entre formatos de dominio y DTOs

"""

from entregaalpes.seedwork.dominio.repositorios import Mapeador
from entregaalpes.seedwork.infraestructura.utils import unix_time_millis
from entregaalpes.modulos.solicitudes.dominio.objetos_valor import Leg, Segmento
from entregaalpes.modulos.solicitudes.dominio.entidades import Solicitud
from entregaalpes.modulos.solicitudes.dominio.eventos import SolicitudAprobada, SolicitudCancelada, SolicitudAprobada, SolicitudPagada, SolicitudCreada, EventoSolicitud

from .dto import Solicitud as SolicitudDTO
from .excepciones import NoExisteImplementacionParaTipoFabricaExcepcion
from pulsar.schema import *

class MapadeadorEventosSolicitud(Mapeador):

    # Versiones aceptadas
    versions = ('v1',)

    LATEST_VERSION = versions[0]

    def __init__(self):
        self.router = {
            SolicitudCreada: self._entidad_a_solicitud_creada,
            SolicitudAprobada: self._entidad_a_solicitud_aprobada,
            SolicitudCancelada: self._entidad_a_solicitud_cancelada,
            SolicitudPagada: self._entidad_a_solicitud_pagada
        }

    def obtener_tipo(self) -> type:
        return EventoSolicitud.__class__

    def es_version_valida(self, version):
        for v in self.versions:
            if v == version:
                return True
        return False

    def _entidad_a_solicitud_creada(self, entidad: SolicitudCreada, version=LATEST_VERSION):
        def v1(evento):
            from .schema.v1.eventos import ReservaCreadaPayload, EventoReservaCreada

            payload = ReservaCreadaPayload(
                id_reserva=str(evento.id_reserva), 
                id_cliente=str(evento.id_cliente), 
                estado=str(evento.estado), 
                fecha_creacion=int(unix_time_millis(evento.fecha_creacion))
            )
            evento_integracion = EventoReservaCreada(id=str(evento.id))
            evento_integracion.id = str(evento.id)
            evento_integracion.time = int(unix_time_millis(evento.fecha_creacion))
            evento_integracion.specversion = str(version)
            evento_integracion.type = 'SolicitudCreada'
            evento_integracion.datacontenttype = 'AVRO'
            evento_integracion.service_name = 'aeroalpes'
            evento_integracion.data = payload

            return evento_integracion
                    
        if not self.es_version_valida(version):
            raise Exception(f'No se sabe procesar la version {version}')

        if version == 'v1':
            return v1(entidad)       

    def _entidad_a_solicitud_aprobada(self, entidad: SolicitudAprobada, version=LATEST_VERSION):
        # TODO
        raise NotImplementedError
    
    def _entidad_a_solicitud_cancelada(self, entidad: SolicitudCancelada, version=LATEST_VERSION):
        # TODO
        raise NotImplementedError
    
    def _entidad_a_solicitud_pagada(self, entidad: SolicitudPagada, version=LATEST_VERSION):
        # TODO
        raise NotImplementedError

    def entidad_a_dto(self, entidad: EventoSolicitud, version=LATEST_VERSION) -> SolicitudDTO:
        if not entidad:
            raise NoExisteImplementacionParaTipoFabricaExcepcion
        func = self.router.get(entidad.__class__, None)

        if not func:
            raise NoExisteImplementacionParaTipoFabricaExcepcion

        return func(entidad, version=version)

    def dto_a_entidad(self, dto: SolicitudDTO, version=LATEST_VERSION) -> Solicitud:
        raise NotImplementedError


class MapeadorSolicitud(Mapeador):
    _FORMATO_FECHA = '%Y-%m-%dT%H:%M:%SZ'
    
    def obtener_tipo(self) -> type:
        return Solicitud.__class__

    def entidad_a_dto(self, entidad: Solicitud) -> SolicitudDTO:
        
        solicitud_dto = SolicitudDTO()
        solicitud_dto.fecha_creacion = entidad.fecha_creacion
        solicitud_dto.fecha_actualizacion = entidad.fecha_actualizacion
        solicitud_dto.id = str(entidad.id)

        return solicitud_dto

    def dto_a_entidad(self, dto: SolicitudDTO) -> Solicitud:
        solicitud = Solicitud(dto.id, dto.fecha_creacion, dto.fecha_actualizacion)
        
        return solicitud