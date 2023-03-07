from dataclasses import dataclass, field
from entregaalpes.seedwork.aplicacion.dto import DTO

@dataclass(frozen=True)
class LegDTO(DTO):
    fecha_salida: str
    fecha_llegada: str
    origen: str
    destino: str

@dataclass(frozen=True)
class SolicitudDTO(DTO):
    fecha_creacion: str = field(default_factory=str)
    fecha_actualizacion: str = field(default_factory=str)
    id: str = field(default_factory=str)
    cliente: str = field(default_factory=str)