

from entregaalpes.modulos.envios.dominio.eventos import SolicitudCreada
from entregaalpes.seedwork.aplicacion.handlers import Handler

class HandlerSolicitudDominio(Handler):

    @staticmethod
    def handle_solicitud_creada(evento):
        print('================ SOLICITUD CREADA ===========')
        

    