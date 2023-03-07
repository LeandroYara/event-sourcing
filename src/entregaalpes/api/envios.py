import entregaalpes.seedwork.presentacion.api as api
import json
from entregaalpes.modulos.envios.aplicacion.dto import ReservaDTO
from entregaalpes.seedwork.dominio.excepciones import ExcepcionDominio

from flask import redirect, render_template, request, session, url_for
from flask import Response
from entregaalpes.modulos.envios.aplicacion.mapeadores import MapeadorSolicitudDTOJson
from entregaalpes.modulos.envios.aplicacion.comandos.crear_reserva import CrearSolicitud
from entregaalpes.modulos.envios.aplicacion.queries.obtener_reserva import ObtenerReserva
from entregaalpes.seedwork.aplicacion.comandos import ejecutar_commando
from entregaalpes.seedwork.aplicacion.queries import ejecutar_query

bp = api.crear_blueprint('envios', '/envios')

@bp.route('/solicitud', methods=('POST',))
def solicitar_usando_comando():
    try:
        # NOTE Asignamos el valor 'pulsar' para usar la Unidad de trabajo de Pulsar y 
        # no la defecto de SQLAlchemy
        session['uow_metodo'] = 'pulsar'

        solicitud_dict = request.json

        map_solicitud = MapeadorSolicitudDTOJson()
        solicitud_dto = map_solicitud.externo_a_dto(solicitud_dict)

        comando = CrearSolicitud(solicitud_dto.fecha_creacion, solicitud_dto.fecha_actualizacion, solicitud_dto.id, solicitud_dto.cliente)
        
        # TODO Reemplaze es todo código sincrono y use el broker de eventos para propagar este comando de forma asíncrona
        # Revise la clase Despachador de la capa de infraestructura
        ejecutar_commando(comando)
        
        return Response('{}', status=202, mimetype='application/json')
    except ExcepcionDominio as e:
        return Response(json.dumps(dict(error=str(e))), status=400, mimetype='application/json')

@bp.route('/solicitud', methods=('GET',))
@bp.route('/solicitud/<id>', methods=('GET',))
def dar_solicitud_usando_query(id=None):
    if id:
        query_resultado = ejecutar_query(ObtenerReserva(id))
        map_reserva = MapeadorSolicitudDTOJson()
        
        return map_reserva.dto_a_externo(query_resultado.resultado)
    else:
        return [{'message': 'GET!'}]