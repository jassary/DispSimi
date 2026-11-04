"""Configuración general: colores, tiempos de simulación y escenarios."""
from dataclasses import dataclass


@dataclass(frozen=True)
class Tema:
    fondo: str = '#FFFFFF'
    panel: str = '#D4D4D4'
    grafica: str = '#F7F7F7'
    texto: str = '#2B2B2B'
    texto_secundario: str = '#5A5A5A'
    rejilla: str = '#B3B3B3'
    cpu: str = '#D9534F'
    disipador: str = '#F0AD4E'
    ambiente: str = '#0275D8'
    limite: str = '#8B0000'
    ok: str = '#2E8B57'
    aviso: str = '#C77C02'


TEMA = Tema()

DT_SIMULACION = 0.05      
PERIODO_TICK_MS = 100     
PASOS_POR_TICK = 2        
VELOCIDADES = ('1', '5', '10')


VENTANA_GRAFICA_S = 180   
MARGEN_FUTURO_S = 20      


MAX_REGISTROS = 100_000   


ESCENARIOS = {
    'Reposo': (5, 30, 25),
    'Navegación': (30, 40, 28),
    'Videojuego': (100, 80, 28),
    'Ventilador averiado': (100, 0, 28),
    'Día caluroso': (80, 50, 38),
}
