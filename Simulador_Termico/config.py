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

# Tiempo
DT_SIMULACION = 0.05      # paso de integración de Euler [s simulados]
PERIODO_TICK_MS = 100     # refresco de la interfaz [ms reales]
PASOS_POR_TICK = 2        # a 1×: 2 · 0.05 s = 0.1 s simulados cada 100 ms → tiempo real
VELOCIDADES = ('1', '5', '10')

# Gráfica
VENTANA_GRAFICA_S = 180   # ancho total del eje X [s]
MARGEN_FUTURO_S = 20      # espacio a la derecha para ver la recta tangente "hacia el futuro"

# Datos
MAX_REGISTROS = 100_000   # tope de memoria del historial

# Escenarios rápidos: nombre -> (carga %, ventilador %, ambiente °C)
ESCENARIOS = {
    'Reposo': (5, 30, 25),
    'Navegación': (30, 40, 28),
    'Videojuego': (100, 80, 28),
    'Ventilador averiado': (100, 0, 28),
    'Día caluroso': (80, 50, 38),
}
