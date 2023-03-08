""" Repositorios para el manejo de persistencia de objetos de dominio en la capa de infrastructura del dominio de vuelos

En este archivo usted encontrará las diferentes repositorios para
persistir objetos dominio (agregaciones) en la capa de infraestructura del dominio de vuelos

"""

from entregaalpes.config.db import db
from entregaalpes.modulos.solicitudes.dominio.fabricas import FabricaEnvios
from entregaalpes.modulos.solicitudes.dominio.repositorios import RepositorioSolicitudes, RepositorioEventosSolicitudes
from entregaalpes.modulos.solicitudes.dominio.objetos_valor import NombreAero, Leg, Segmento
from entregaalpes.modulos.solicitudes.dominio.entidades import Solicitud
from .dto import Solicitud as SolicitudDTO
from .dto import EventosSolicitud
from .mapeadores import MapeadorSolicitud, MapadeadorEventosSolicitud
from uuid import UUID
from pulsar.schema import *


class RepositorioSolicitudesSQLAlchemy(RepositorioSolicitudes):

    def __init__(self):
        self._fabrica_envios: FabricaEnvios = FabricaEnvios()

    @property
    def fabrica_vuelos(self):
        return self._fabrica_vuelos

    def obtener_por_id(self, id: UUID) -> Solicitud:
        reserva_dto = db.session.query(SolicitudDTO).filter_by(id=str(id)).one()
        return self.fabrica_vuelos.crear_objeto(reserva_dto, MapeadorSolicitud())

    def obtener_todos(self) -> list[Solicitud]:
        # TODO
        raise NotImplementedError

    def agregar(self, solicitud: Solicitud):
        reserva_dto = self.fabrica_vuelos.crear_objeto(solicitud, MapeadorSolicitud())

        db.session.add(reserva_dto)

    def actualizar(self, solicitud: Solicitud):
        # TODO
        raise NotImplementedError

    def eliminar(self, solicitud_id: UUID):
        # TODO
        raise NotImplementedError

class RepositorioEventosSolicitudSQLAlchemy(RepositorioEventosSolicitudes):

    def __init__(self):
        self._fabrica_vuelos: FabricaEnvios = FabricaEnvios()

    @property
    def fabrica_envios(self):
        return self._fabrica_vuelos

    def obtener_por_id(self, id: UUID) -> Solicitud:
        solicitud_dto = db.session.query(SolicitudDTO).filter_by(id=str(id)).one()
        return self.fabrica_envios.crear_objeto(solicitud_dto, MapadeadorEventosSolicitud())

    def obtener_todos(self) -> list[Solicitud]:
        raise NotImplementedError

    def agregar(self, evento):
        solicitud_evento = self.fabrica_vuelos.crear_objeto(evento, MapadeadorEventosSolicitud())

        parser_payload = JsonSchema(solicitud_evento.data.__class__)
        json_str = parser_payload.encode(solicitud_evento.data)

        evento_dto = EventosSolicitud()
        evento_dto.id = str(evento.id)
        evento_dto.id_entidad = str(evento.id_reserva)
        evento_dto.fecha_evento = evento.fecha_creacion
        evento_dto.version = str(solicitud_evento.specversion)
        evento_dto.tipo_evento = evento.__class__.__name__
        evento_dto.formato_contenido = 'JSON'
        evento_dto.nombre_servicio = str(solicitud_evento.service_name)
        evento_dto.contenido = json_str

        db.session.add(evento_dto)

    def actualizar(self, solicitud: Solicitud):
        raise NotImplementedError

    def eliminar(self, reserva_id: UUID):
        raise NotImplementedError
