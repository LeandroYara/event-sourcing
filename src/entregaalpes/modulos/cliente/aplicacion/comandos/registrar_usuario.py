from entregaalpes.seedwork.aplicacion.comandos import Comando, ComandoHandler

class RegistrarUsuario(Comando):
    nombres: str
    apellidos: str
    correo: str
    contrasena: str
    es_empresarial: bool

class RegistrarUsuarioHandler(ComandoHandler):
    ...