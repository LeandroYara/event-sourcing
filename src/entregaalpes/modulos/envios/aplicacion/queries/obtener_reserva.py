from entregaalpes.seedwork.aplicacion.queries import Query, QueryHandler, QueryResultado
from entregaalpes.seedwork.aplicacion.queries import ejecutar_query as query
from entregaalpes.modulos.envios.infraestructura.repositorios import RepositorioReservas
from entregaalpes.modulos.envios.dominio.entidades import Reserva
from dataclasses import dataclass
from .base import ReservaQueryBaseHandler
from entregaalpes.modulos.envios.aplicacion.mapeadores import MapeadorReserva
import uuid

@dataclass
class ObtenerReserva(Query):
    id: str

class ObtenerReservaHandler(ReservaQueryBaseHandler):

    def handle(self, query: ObtenerReserva) -> QueryResultado:
        vista = self.fabrica_vista.crear_objeto(Reserva)
        reserva =  self.fabrica_vuelos.crear_objeto(vista.obtener_por(id=query.id)[0], MapeadorReserva())
        return QueryResultado(resultado=reserva)

@query.register(ObtenerReserva)
def ejecutar_query_obtener_reserva(query: ObtenerReserva):
    handler = ObtenerReservaHandler()
    return handler.handle(query)