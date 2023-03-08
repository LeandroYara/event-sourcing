import os

from flask import Flask, render_template, request, url_for, redirect, jsonify, session
from flask_swagger import swagger

# Identifica el directorio base
basedir = os.path.abspath(os.path.dirname(__file__))

def registrar_handlers():
    import entregaalpes.modulos.cliente.aplicacion
    import entregaalpes.modulos.solicitudes.aplicacion

def importar_modelos_alchemy():
    import entregaalpes.modulos.cliente.infraestructura.dto
    import entregaalpes.modulos.pagos.infraestructura.dto
    import entregaalpes.modulos.solicitudes.infraestructura.dto

def comenzar_consumidor(app):
    """
    Este es un código de ejemplo. Aunque esto sea funcional puede ser un poco peligroso tener 
    threads corriendo por si solos. Mi sugerencia es en estos casos usar un verdadero manejador
    de procesos y threads como Celery.
    """

    import threading
    import entregaalpes.modulos.cliente.infraestructura.consumidores as cliente
    import entregaalpes.modulos.pagos.infraestructura.consumidores as pagos
    import entregaalpes.modulos.solicitudes.infraestructura.consumidores as envios

    # Suscripción a eventos
    threading.Thread(target=cliente.suscribirse_a_eventos).start()
    threading.Thread(target=pagos.suscribirse_a_eventos).start()
    threading.Thread(target=envios.suscribirse_a_eventos, args=[app]).start()

    # Suscripción a comandos
    threading.Thread(target=cliente.suscribirse_a_comandos).start()
    threading.Thread(target=pagos.suscribirse_a_comandos).start()
    threading.Thread(target=envios.suscribirse_a_comandos, args=[app]).start()

def create_app(configuracion={}):
    # Init la aplicacion de Flask
    app = Flask(__name__, instance_relative_config=True)
    
    app.secret_key = '9d58f98f-3ae8-4149-a09f-3a8c2012e32c'
    app.config['SESSION_TYPE'] = 'filesystem'
    app.config['TESTING'] = configuracion.get('TESTING')

     # Inicializa la DB
    from entregaalpes.config.db import init_db, database_connection

    app.config['SQLALCHEMY_DATABASE_URI'] = database_connection(configuracion, basedir=basedir)
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    init_db(app)

    from entregaalpes.config.db import db

    importar_modelos_alchemy()
    registrar_handlers()

    with app.app_context():
        db.create_all()
        if not app.config.get('TESTING'):
            comenzar_consumidor(app)

     # Importa Blueprints
    from . import cliente
    from . import pagos
    from . import envios

    # Registro de Blueprints
    app.register_blueprint(cliente.bp)
    app.register_blueprint(pagos.bp)
    app.register_blueprint(envios.bp)

    @app.route("/spec")
    def spec():
        swag = swagger(app)
        swag['info']['version'] = "1.0"
        swag['info']['title'] = "My API"
        return jsonify(swag)

    @app.route("/health")
    def health():
        return {"status": "up"}

    return app
