import uuid
from entregaalpes.seedwork.aplicacion.comandos import Comando, ComandoHandler    

class AgregarSolicitudUsuario(Comando):
    id_usuario: uuid.UUID
    id_solicitud: uuid.UUID

class AgregarSolicitudUsuarioHandler(ComandoHandler):
    ...