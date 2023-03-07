""" Fábricas para la creación de objetos del dominio de vuelos

En este archivo usted encontrará las diferentes fábricas para crear
objetos complejos del dominio de vuelos

"""

from .entidades import Solicitud
from .excepciones import TipoObjetoNoExisteEnDominioEnviosExcepcion
from entregaalpes.seedwork.dominio.repositorios import Mapeador, Repositorio
from entregaalpes.seedwork.dominio.fabricas import Fabrica
from entregaalpes.seedwork.dominio.entidades import Entidad
from entregaalpes.seedwork.dominio.eventos import EventoDominio
from dataclasses import dataclass

@dataclass
class _FabricaSolicitud(Fabrica):
    def crear_objeto(self, obj: any, mapeador: Mapeador) -> any:
        if isinstance(obj, Entidad) or isinstance(obj, EventoDominio):
            return mapeador.entidad_a_dto(obj)
        else:
            solicitud: Solicitud = mapeador.dto_a_entidad(obj)
            
            return solicitud

@dataclass
class FabricaEnvios(Fabrica):
    def crear_objeto(self, obj: any, mapeador: Mapeador) -> any:
        if mapeador.obtener_tipo() == Solicitud.__class__:
            fabrica_solicitud = _FabricaSolicitud()
            return fabrica_solicitud.crear_objeto(obj, mapeador)
        else:
            raise TipoObjetoNoExisteEnDominioEnviosExcepcion()

