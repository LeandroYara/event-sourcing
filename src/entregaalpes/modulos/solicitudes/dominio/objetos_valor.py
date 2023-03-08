from __future__ import annotations

from dataclasses import dataclass, field
from entregaalpes.modulos.solicitudes.dominio.entidades import Cliente
from entregaalpes.seedwork.dominio.objetos_valor import ObjetoValor, Codigo, Ruta, Locacion
from datetime import datetime
from enum import Enum

@dataclass(frozen=True)
class NombreCliente():
    nombre: str

@dataclass(frozen=True)
class Leg(Ruta):
    fecha_salida: datetime
    fecha_llegada: datetime
    origen: Locacion
    destino: Locacion

    def origen(self) -> Locacion:
        return self.origen

    def destino(self) -> Locacion:
        return self.destino

    def fecha_salida(self) -> datetime:
        return self.fecha_salida
    
    def fecha_llegada(self) -> datetime:
        return self.fecha_llegada

@dataclass(frozen=True)
class Segmento(Ruta):
    legs: list[Leg]

    def origen(self) -> Locacion:
        return self.legs[0].origen

    def destino(self) -> Locacion:
        return self.legs[-1].destino

    def fecha_salida(self) -> datetime:
        return self.legs[0].fecha_salida
    
    def fecha_llegada(self) -> datetime:
        return self.legs[-1].fecha_llegada

class TipoPaquete(str, Enum):
    DOMICILIO = "Domicilio"
    PAQUETE = "Paquete"

@dataclass(frozen=True)
class ParametroBusca(ObjetoValor):
    pasajeros: list[Cliente] = field(default_factory=list)


class EstadoSolicitud(str, Enum):
    APROBADA = "Aprobada"
    PENDIENTE = "Pendiente"
    CANCELADA = "Cancelada"
    PAGADA = "Pagada"