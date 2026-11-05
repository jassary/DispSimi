from dataclasses import dataclass


@dataclass(frozen=True)
class Tema:
    fondo: str = '#EFF4F8'
    panel: str = '#FFFFFF'
    grafica: str = '#FFFFFF'
    texto: str = '#152F45'
    texto_secundario: str = '#4A657A'
    rejilla: str = '#DDE7EF'
    cpu: str = '#BA3448'
    disipador: str = '#9F5909'
    ambiente: str = '#127297'
    limite: str = '#A42139'
    ok: str = '#12705D'
    aviso: str = '#99570B'
    cabecera: str = '#073577'
    acento: str = '#1458A5'


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
