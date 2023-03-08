from entregaalpes.seedwork.infraestructura.vistas import Vista
from entregaalpes.modulos.solicitudes.dominio.entidades import Solicitud
from entregaalpes.config.db import db
from .dto import Solicitud as SolicitudDTO

class VistaSolicitud(Vista):
    def obtener_por(id=None, estado=None, id_cliente=None, **kwargs) -> Solicitud:
        params = dict()

        if id:
            params['id'] = str(id)
        
        if estado:
            params['estado'] = str(estado)
        
        if id_cliente:
            params['id_cliente'] = str(id_cliente)
            
        # TODO Convierta ReservaDTO a Reserva y valide que la consulta es correcta
        return db.session.query(SolicitudDTO).filter_by(**params)
