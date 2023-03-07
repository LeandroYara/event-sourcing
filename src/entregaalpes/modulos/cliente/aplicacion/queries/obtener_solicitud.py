from entregaalpes.seedwork.aplicacion.queries import Query, QueryHandler, ResultadoQuery
import uuid

class ObtenerSolicitud(Query):
    listing_id: uuid.UUID

class ObtenerSolicitudHandler(QueryHandler):

    def handle() -> ResultadoQuery:
        ...