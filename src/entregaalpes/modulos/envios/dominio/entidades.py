"""Entidades del dominio de vuelos

En este archivo usted encontrará las entidades del dominio de vuelos

"""

from __future__ import annotations
from dataclasses import dataclass, field
import datetime
import uuid

import entregaalpes.modulos.envios.dominio.objetos_valor as ov
from entregaalpes.modulos.envios.dominio.eventos import SolicitudCreada, SolicitudAprobada, SolicitudCancelada, SolicitudPagada
from entregaalpes.seedwork.dominio.entidades import AgregacionRaiz, Entidad

@dataclass

@dataclass
class Cliente(Entidad):
    clase: ov.Clase = field(default_factory=ov.Clase)
    tipo: ov.TipoPasajero = field(default_factory=ov.TipoPasajero)

@dataclass
class Solicitud(AgregacionRaiz):
    id_cliente: uuid.UUID = field(hash=True, default=None)
    estado: ov.EstadoSolicitud = field(default=ov.EstadoSolicitud.PENDIENTE)

    def crear_solicitud(self, solicitud: Solicitud):
        self.id_cliente = solicitud.id_cliente
        self.estado = solicitud.estado
        self.fecha_creacion = datetime.datetime.now()

        self.agregar_evento(SolicitudCreada(id_reserva=self.id, id_cliente=self.id_cliente, estado=self.estado.name, fecha_creacion=self.fecha_creacion))
        # TODO Agregar evento de compensación

    def aprobar_solicitud(self):
        self.estado = ov.EstadoSolicitud.APROBADA
        self.fecha_actualizacion = datetime.datetime.now()

        self.agregar_evento(SolicitudAprobada(self.id, self.fecha_actualizacion))
        # TODO Agregar evento de compensación

    def cancelar_solicitud(self):
        self.estado = ov.EstadoSolicitud.CANCELADA
        self.fecha_actualizacion = datetime.datetime.now()

        self.agregar_evento(SolicitudCancelada(self.id, self.fecha_actualizacion))
        # TODO Agregar evento de compensación
    
    def pagar_solicitud(self):
        self.estado = ov.EstadoReserva.PAGADA
        self.fecha_actualizacion = datetime.datetime.now()

        self.agregar_evento(SolicitudPagada(self.id, self.fecha_actualizacion))
        # TODO Agregar evento de compensación
