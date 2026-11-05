"""Configuración general: colores, tiempos de simulación y escenarios."""
from dataclasses import dataclass

FUENTE = 'Segoe UI'   


@dataclass(frozen=True)
class Tema:
    """Paleta extraída de la imagen de referencia (dashboard oscuro con acentos amarillo y verde)."""
    
    fondo: str = '#161815'          
    barra: str = '#2C2F2B'          
    panel: str = '#2C2F2B'          
    panel_claro: str = '#424542'    
    cabecera: str = '#393B38'       
    borde: str = '#383B38'
    grafica: str = '#2C2F2B'
    texto: str = '#FFFFFF'
    texto_secundario: str = '#A6A9A6'
    rejilla: str = '#5A5D5A'
    cpu: str = '#FFCA00'            
    disipador: str = '#31C75C'      
    ambiente: str = '#6FA8DC'       
    limite: str = '#E07A8E'         
    ok: str = '#31C75C'
    aviso: str = '#FFCA00'
    acento: str = '#31C75C'
    tarjeta_clara: str = '#FFFFFF'
    texto_oscuro: str = '#161815'
    texto_oscuro_sec: str = '#5A5D5A'
    ok_oscuro: str = '#1A7736'
    aviso_oscuro: str = '#B98400'
    limite_oscuro: str = '#B83A55'


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