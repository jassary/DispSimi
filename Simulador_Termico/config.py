"""Configuración general: colores, tiempos de simulación y escenarios."""
from dataclasses import dataclass

FUENTE = 'Segoe UI'   # si no existe (Linux/Mac), Tkinter usa una fuente parecida


@dataclass(frozen=True)
class Tema:
    """Paleta extraída de la imagen de referencia (dashboard oscuro con acentos amarillo y verde)."""
    # superficies
    fondo: str = '#161815'          # fondo general de la ventana
    barra: str = '#2C2F2B'          # barra lateral
    panel: str = '#2C2F2B'          # tarjetas
    panel_claro: str = '#424542'    # insignias de iconos, ítem activo/hover, cajas del diagrama
    cabecera: str = '#393B38'       # cabecera de la tabla
    borde: str = '#383B38'
    grafica: str = '#2C2F2B'
    # texto
    texto: str = '#FFFFFF'
    texto_secundario: str = '#A6A9A6'
    rejilla: str = '#5A5D5A'
    # series y estados (sobre fondo oscuro)
    cpu: str = '#FFCA00'            # amarillo (primera serie de la referencia)
    disipador: str = '#31C75C'      # verde (segunda serie de la referencia)
    ambiente: str = '#6FA8DC'       # la referencia solo tiene 2 series: este azul suave es el tercero
    limite: str = '#E07A8E'         # rosa (estado UNPAID de la referencia)
    ok: str = '#31C75C'
    aviso: str = '#FFCA00'
    acento: str = '#31C75C'
    # tarjeta blanca de resalte (como "Marketing goal" de la referencia)
    tarjeta_clara: str = '#FFFFFF'
    texto_oscuro: str = '#161815'
    texto_oscuro_sec: str = '#5A5D5A'
    ok_oscuro: str = '#1A7736'
    aviso_oscuro: str = '#B98400'
    limite_oscuro: str = '#B83A55'


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