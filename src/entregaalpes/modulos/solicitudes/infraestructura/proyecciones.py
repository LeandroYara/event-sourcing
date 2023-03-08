from entregaalpes.seedwork.infraestructura.proyecciones import Proyeccion, ProyeccionHandler
from entregaalpes.seedwork.infraestructura.proyecciones import ejecutar_proyeccion as proyeccion
from entregaalpes.modulos.solicitudes.infraestructura.fabricas import FabricaRepositorio
from entregaalpes.modulos.solicitudes.infraestructura.repositorios import RepositorioSolicitudes
from entregaalpes.modulos.solicitudes.dominio.entidades import Solicitud
from entregaalpes.modulos.solicitudes.infraestructura.dto import Solicitud as SolicitudDTO

from entregaalpes.seedwork.infraestructura.utils import millis_a_datetime
import datetime
import logging
import traceback
from abc import ABC, abstractmethod
from .dto import SolicitudAnalitica

class ProyeccionSolicitud(Proyeccion, ABC):
    @abstractmethod
    def ejecutar(self):
        ...

class ProyeccionSolicitudesTotales(ProyeccionSolicitud):
    ADD = 1
    DELETE = 2
    UPDATE = 3

    def __init__(self, fecha_creacion, operacion):
        self.fecha_creacion = millis_a_datetime(fecha_creacion)
        self.operacion = operacion

    def ejecutar(self, db=None):
        if not db:
            logging.error('ERROR: DB del app no puede ser nula')
            return
        # NOTE esta no usa repositorios y de una vez aplica los cambios. Es decir, no todo siempre debe ser un repositorio
        record = db.session.query(SolicitudAnalitica).filter_by(fecha_creacion=self.fecha_creacion.date()).one_or_none()

        if record and self.operacion == self.ADD:
            record.total += 1
        elif record and self.operacion == self.DELETE:
            record.total -= 1 
            record.total = max(record.total, 0)
        else:
            db.session.add(SolicitudAnalitica(fecha_creacion=self.fecha_creacion.date(), total=1))
        
        db.session.commit()

class ProyeccionSolicitudesLista(ProyeccionSolicitud):
    def __init__(self, id_reserva, id_cliente, estado, fecha_creacion, fecha_actualizacion):
        self.id_reserva = id
        self.id_cliente = id_cliente
        self.estado = estado
        self.fecha_creacion = millis_a_datetime(fecha_creacion)
        self.fecha_actualizacion = millis_a_datetime(fecha_actualizacion)
    
    def ejecutar(self, db=None):
        if not db:
            logging.error('ERROR: DB del app no puede ser nula')
            return
        
        fabrica_repositorio = FabricaRepositorio()
        repositorio = fabrica_repositorio.crear_objeto(RepositorioSolicitudes)
        
        repositorio.agregar(
            Solicitud(
                id=str(self.id_reserva), 
                id_cliente=str(self.id_cliente), 
                estado=str(self.estado), 
                fecha_creacion=self.fecha_creacion, 
                fecha_actualizacion=self.fecha_actualizacion))
        
        # TODO ¿Y si la reserva ya existe y debemos actualizarla? Complete el método para hacer merge

        # TODO ¿Tal vez podríamos reutilizar la Unidad de Trabajo?
        db.session.commit()

class ProyeccionSolicitudHandler(ProyeccionHandler):
    
    def handle(self, proyeccion: ProyeccionSolicitud):
        from entregaalpes.config.db import db

        proyeccion.ejecutar(db=db)
        

@proyeccion.register(ProyeccionSolicitudesLista)
@proyeccion.register(ProyeccionSolicitudesTotales)
def ejecutar_proyeccion_reserva(proyeccion, app=None):
    if not app:
        logging.error('ERROR: Contexto del app no puede ser nulo')
        return
    try:
        with app.app_context():
            handler = ProyeccionSolicitudHandler()
            handler.handle(proyeccion)
            
    except:
        traceback.print_exc()
        logging.error('ERROR: Persistiendo!')
    