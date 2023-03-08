from entregaalpes.seedwork.aplicacion.queries import Query, QueryHandler, QueryResultado
from entregaalpes.seedwork.aplicacion.queries import ejecutar_query as query
from entregaalpes.modulos.solicitudes.infraestructura.repositorios import RepositorioReservas
from entregaalpes.modulos.solicitudes.dominio.entidades import Solicitud
from dataclasses import dataclass
from .base import SolicitudQueryBaseHandler
from entregaalpes.modulos.solicitudes.aplicacion.mapeadores import MapeadorSolicitud
import uuid

@dataclass
class ObtenerSolicitud(Query):
    id: str

class ObtenerSolicitudHandler(SolicitudQueryBaseHandler):

    def handle(self, query: ObtenerSolicitud) -> QueryResultado:
        vista = self.fabrica_vista.crear_objeto(Solicitud)
        solicitud =  self.fabrica_envios.crear_objeto(vista.obtener_por(id=query.id)[0], MapeadorSolicitud())
        return QueryResultado(resultado=solicitud)

@query.register(ObtenerSolicitud)
def ejecutar_query_obtener_solicitud(query: ObtenerSolicitud):
    handler = ObtenerSolicitudHandler()
    return handler.handle(query)