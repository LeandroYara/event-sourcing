from entregaalpes.modulos.solicitudes.infraestructura.mapeadores import MapeadorReserva
from entregaalpes.seedwork.aplicacion.comandos import Comando
from entregaalpes.modulos.solicitudes.aplicacion.dto import SolicitudDTO
from .base import CrearSolicitudBaseHandler
from dataclasses import dataclass, field
from entregaalpes.seedwork.aplicacion.comandos import ejecutar_commando as comando

from entregaalpes.modulos.solicitudes.dominio.entidades import Solicitud
from entregaalpes.seedwork.infraestructura.uow import UnidadTrabajoPuerto
from entregaalpes.modulos.solicitudes.aplicacion.mapeadores import MapeadorSo
from entregaalpes.modulos.solicitudes.infraestructura.repositorios import RepositorioReservas, RepositorioEventosReservas

@dataclass
class CrearSolicitud(Comando):
    fecha_creacion: str
    fecha_actualizacion: str
    id: str
    cliente: str


class CrearSolicitudHandler(CrearSolicitudBaseHandler):
    
    def handle(self, comando: CrearSolicitud):
        solicitud_dto = SolicitudDTO(
                fecha_actualizacion=comando.fecha_actualizacion
            ,   fecha_creacion=comando.fecha_creacion
            ,   id=comando.id
            ,   cliente=comando.cliente)

        solicitud: Solicitud = self.fabrica_vuelos.crear_objeto(solicitud_dto, MapeadorReserva())
        reserva.crear_reserva(reserva)

        repositorio = self.fabrica_repositorio.crear_objeto(RepositorioReservas)
        repositorio_eventos = self.fabrica_repositorio.crear_objeto(RepositorioEventosReservas)

        UnidadTrabajoPuerto.registrar_batch(repositorio.agregar, reserva, repositorio_eventos_func=repositorio_eventos.agregar)
        UnidadTrabajoPuerto.commit()


@comando.register(CrearReserva)
def ejecutar_comando_crear_reserva(comando: CrearReserva):
    handler = CrearReservaHandler()
    handler.handle(comando)
    