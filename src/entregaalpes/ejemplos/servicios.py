from entregaalpes.modulos.envios.dominio.objetos_valor import Odo, ParametroBusca
from entregaalpes.modulos.envios.dominio.entidades import Itinerario, Proveedor
from entregaalpes.modulos.envios.dominio.repositorios import RepositorioProveedores as rp
from entregaalpes.seedwork.dominio.servicios import Servicio
from entregaalpes.modulos.envios.dominio.mixins import FiltradoItinerariosMixin
from entregaalpes.modulos.envios.dominio.reglas import MinimoUnAdulto, RutaValida

class ServicioBusqueda(Servicio, FiltradoItinerariosMixin):

    def buscar_itinerarios(self, odos: list[Odo], parametros: ParametroBusca) -> list[Itinerario]:
        itinerarios: list[Itinerario] = list()
        proveedores:list[Proveedor] = rp.obtener_todos()
        
        self.validar_regla(MinimoUnAdulto(parametros.pasajeros))
        [self.validar_regla(RutaValida(ruta)) for odo in odos for segmento in odo.segmentos for ruta in segmento.legs]

        itinerarios.append([proveedor.obtener_itinerarios(odos, parametros) for proveedor in proveedores])

        return self.filtrar_mejores_itinerarios(itinerarios)