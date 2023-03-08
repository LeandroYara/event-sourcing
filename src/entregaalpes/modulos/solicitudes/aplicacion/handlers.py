from entregaalpes.modulos.solicitudes.dominio.eventos import SolicitudCreada, SolicitudCancelada, SolicitudAprobada, SolicitudPagada
from entregaalpes.seedwork.aplicacion.handlers import Handler
from entregaalpes.modulos.solicitudes.infraestructura.despachadores import Despachador

class HandlerReservaIntegracion(Handler):

    @staticmethod
    def handle_solicitud_creada(evento):
        despachador = Despachador()
        despachador.publicar_evento(evento, 'eventos-solicitud')

    @staticmethod
    def handle_solicitud_cancelada(evento):
        despachador = Despachador()
        despachador.publicar_evento(evento, 'eventos-solicitud')

    @staticmethod
    def handle_solicitud_aprobada(evento):
        despachador = Despachador()
        despachador.publicar_evento(evento, 'eventos-solicitud')

    @staticmethod
    def handle_solicitud_pagada(evento):
        despachador = Despachador()
        despachador.publicar_evento(evento, 'eventos-solicitud')


    