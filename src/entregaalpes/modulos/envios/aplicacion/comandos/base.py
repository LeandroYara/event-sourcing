from entregaalpes.seedwork.aplicacion.comandos import ComandoHandler
from entregaalpes.modulos.envios.infraestructura.fabricas import FabricaRepositorio
from entregaalpes.modulos.envios.dominio.fabricas import FabricaVuelos

class CrearSolicitudBaseHandler(ComandoHandler):
    def __init__(self):
        self._fabrica_repositorio: FabricaRepositorio = FabricaRepositorio()
        self._fabrica_vuelos: FabricaVuelos = FabricaVuelos()

    @property
    def fabrica_repositorio(self):
        return self._fabrica_repositorio
    
    @property
    def fabrica_vuelos(self):
        return self._fabrica_vuelos    
    