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
    boton: str = '#E6E6E6'          # fondo de botones y listas desplegables
    titulo: str = '#0275D8'         # color del título principal


# Paletas disponibles. Para cambiar la apariencia, edite PALETA_ACTIVA.
PALETAS = {
    'Clásico': Tema(),
    'Océano oscuro': Tema(
        fondo='#0F1B2D', panel='#1C2B44', grafica='#13233A',
        texto='#E6EDF5', texto_secundario='#9FB3C8', rejilla='#2E4566',
        cpu='#FF6B6B', disipador='#FFB547', ambiente='#4FC3F7',
        limite='#FF3B5C', ok='#4ADE80', aviso='#FBBF24',
        boton='#24406B', titulo='#4FC3F7'),
    'Atardecer': Tema(
        fondo='#FFF8F0', panel='#F3E3D3', grafica='#FFFDF9',
        texto='#3B2A20', texto_secundario='#7A6253', rejilla='#E2CDB8',
        cpu='#E4572E', disipador='#F3A712', ambiente='#29335C',
        limite='#A4161A', ok='#2A9D8F', aviso='#B35C00',
        boton='#F0D9C2', titulo='#E4572E'),
    'Bosque': Tema(
        fondo='#F4F7F2', panel='#DCE6D5', grafica='#FBFDF9',
        texto='#1F2D1F', texto_secundario='#56685A', rejilla='#C3D1BC',
        cpu='#C0392B', disipador='#D98E04', ambiente='#2C7DA0',
        limite='#7B1E1E', ok='#2D6A4F', aviso='#B07D05',
        boton='#CFDDC6', titulo='#2D6A4F'),
}

PALETA_ACTIVA = 'Océano oscuro'
TEMA = PALETAS[PALETA_ACTIVA]

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
