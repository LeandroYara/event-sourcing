from tokenize import String
from pulsar.schema import *
from dataclasses import dataclass, field
from entregaalpes.seedwork.infraestructura.schema.v1.comandos import (ComandoIntegracion)

class ComandoCrearItinerarioPayload(ComandoIntegracion):
    id_usuario = String()
    # TODO Cree los records para itinerarios

class ComandoCrearReserva(ComandoIntegracion):
    data = ComandoCrearItinerarioPayload()