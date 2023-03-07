from __future__ import annotations
from dataclasses import dataclass, field
import uuid
from entregaalpes.seedwork.dominio.eventos import (EventoDominio)
from datetime import datetime

class EventoSolicitud(EventoDominio):
    ...

@dataclass
class SolicitudCreada(EventoSolicitud):
    id_solicitud: uuid.UUID = None
    id_cliente: uuid.UUID = None
    estado: str = None
    fecha_creacion: datetime = None
    
@dataclass
class SolicitudCancelada(EventoSolicitud):
    id_solicitud: uuid.UUID = None
    fecha_actualizacion: datetime = None

@dataclass
class SolicitudAprobada(EventoSolicitud):
    id_solicitud: uuid.UUID = None
    fecha_actualizacion: datetime = None

@dataclass
class SolicitudPagada(EventoSolicitud):
    id_solicitud: uuid.UUID = None
    fecha_actualizacion: datetime = None