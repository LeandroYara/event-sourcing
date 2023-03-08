""" Interfaces para los repositorios del dominio de vuelos

En este archivo usted encontrará las diferentes interfaces para repositorios
del dominio de vuelos

"""

from abc import ABC
from entregaalpes.seedwork.dominio.repositorios import Repositorio

class RepositorioSolicitudes(Repositorio, ABC):
    ...

class RepositorioEventosSolicitudes(Repositorio, ABC):
    ...