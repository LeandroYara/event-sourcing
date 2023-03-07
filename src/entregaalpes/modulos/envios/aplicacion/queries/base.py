from entregaalpes.seedwork.aplicacion.queries import QueryHandler
from entregaalpes.modulos.envios.infraestructura.fabricas import FabricaVista
from entregaalpes.modulos.envios.dominio.fabricas import FabricaEnvios

class SolicitudQueryBaseHandler(QueryHandler):
    def __init__(self):
        self._fabrica_vista: FabricaVista = FabricaVista()
        self._fabrica_envios: FabricaEnvios = FabricaEnvios()

    @property
    def fabrica_vista(self):
        return self._fabrica_vista
    
    @property
    def fabrica_envios(self):
        return self._fabrica_envios    