"""Configuración general: colores, tiempos de simulación y escenarios."""
import tkinter as tk
from tkinter import ttk
from dataclasses import dataclass

FUENTE = 'Segoe UI'
TAM_FUENTE = 10


@dataclass(frozen=True)
class Tema:
    fondo: str = '#ECE9D8'
    barra: str = '#ECE9D8'
    panel: str = '#FFFFFF'
    panel_claro: str = '#FDF5E6'
    cabecera: str = '#ECE9D8'
    borde: str = '#C0C0C0'
    grafica: str = '#FFFFFF'
    texto: str = '#000000'
    texto_secundario: str = '#000000'
    rejilla: str = '#C0C0C0'
    cpu: str = "#607EAC"
    disipador: str = "#99B3A0"
    ambiente: str = '#808080'
    limite: str = '#C62828'
    ok: str = '#000000'
    aviso: str = '#000000'
    acento: str = '#316AC5'
    tarjeta_clara: str = '#FFFFCC'
    texto_oscuro: str = '#000000'
    texto_oscuro_sec: str = '#000000'
    ok_oscuro: str = '#000000'
    aviso_oscuro: str = '#000000'
    limite_oscuro: str = '#000000'
    tarjeta_fondo: str = '#FFFFFF'
    tarjeta_borde_grosor: int = 3
    titulo: str = '#000000'
    seccion_fondo: str = '#D6DFF7'
    seccion_texto: str = '#000000'
    seccion_borde: str = '#7A96DF'
    boton_borde: str = '#003C74'
    boton_fondo: str = '#F3F2EA'
    boton_activo: str = '#FFFFCC'
    ventana_borde: str = '#0055D4'
    linea_cpu: str = '#0055D4'
    linea_disipador: str = '#1E8E3E'
    linea_ambiente: str = '#808080'
    linea_aviso: str = '#D98E00'


TEMA = Tema()


def aplicar_estilo(raiz):
    raiz.configure(bg=TEMA.fondo)
    raiz.option_add('*Font', (FUENTE, TAM_FUENTE))
    raiz.option_add('*Background', TEMA.fondo)
    raiz.option_add('*Foreground', TEMA.texto)
    raiz.option_add('*Label.Background', TEMA.fondo)
    raiz.option_add('*Label.Foreground', TEMA.texto)
    raiz.option_add('*Button.Foreground', TEMA.texto)
    raiz.option_add('*Checkbutton.Foreground', TEMA.texto)
    raiz.option_add('*Radiobutton.Foreground', TEMA.texto)
    raiz.option_add('*Scale.Foreground', TEMA.texto)
    raiz.option_add('*Scale.Background', TEMA.fondo)
    raiz.option_add('*Scale.TroughColor', TEMA.panel)
    raiz.option_add('*Scale.HighlightThickness', 0)
    raiz.option_add('*Scale.BorderWidth', 1)
    raiz.option_add('*Scale.ActiveBackground', TEMA.boton_activo)
    raiz.option_add('*Canvas.Background', TEMA.grafica)
    raiz.option_add('*Canvas.HighlightThickness', 0)

    estilo = ttk.Style(raiz)
    estilo.theme_use('clam')

    estilo.configure('.', background=TEMA.fondo, foreground=TEMA.texto, font=(FUENTE, TAM_FUENTE),
                     bordercolor=TEMA.boton_borde, lightcolor=TEMA.panel, darkcolor=TEMA.borde)

    estilo.configure('TButton', background=TEMA.boton_fondo, foreground=TEMA.texto,
                     font=(FUENTE, TAM_FUENTE),
                     bordercolor=TEMA.boton_borde, lightcolor=TEMA.panel, darkcolor=TEMA.borde,
                     padding=(10, 3), relief='raised', focuscolor=TEMA.boton_fondo)
    estilo.map('TButton',
               background=[('pressed', TEMA.borde), ('active', TEMA.boton_activo)],
               foreground=[('disabled', TEMA.texto), ('!disabled', TEMA.texto)],
               bordercolor=[('active', TEMA.aviso), ('pressed', TEMA.boton_borde)],
               relief=[('pressed', 'sunken')])

    estilo.configure('TCheckbutton', background=TEMA.fondo, foreground=TEMA.texto,
                     font=(FUENTE, TAM_FUENTE),
                     focuscolor=TEMA.fondo, indicatorbackground=TEMA.panel,
                     indicatorforeground=TEMA.texto, bordercolor=TEMA.acento)
    estilo.map('TCheckbutton', background=[('active', TEMA.fondo)],
               foreground=[('disabled', TEMA.texto), ('!disabled', TEMA.texto)],
               indicatorbackground=[('pressed', TEMA.boton_activo)])

    estilo.configure('TLabel', background=TEMA.fondo, foreground=TEMA.texto,
                     font=(FUENTE, TAM_FUENTE))

    estilo.configure('TCombobox', fieldbackground=TEMA.panel, background=TEMA.boton_fondo,
                     foreground=TEMA.texto, bordercolor=TEMA.acento, arrowcolor=TEMA.texto,
                     lightcolor=TEMA.panel, darkcolor=TEMA.panel)
    estilo.map('TCombobox', fieldbackground=[('readonly', TEMA.panel)],
               foreground=[('readonly', TEMA.texto)],
               selectbackground=[('readonly', TEMA.panel)],
               selectforeground=[('readonly', TEMA.texto)],
               bordercolor=[('focus', TEMA.cpu)])
    raiz.option_add('*TCombobox*Font', (FUENTE, TAM_FUENTE))
    raiz.option_add('*TCombobox*Listbox.Font', (FUENTE, TAM_FUENTE))
    raiz.option_add('*TCombobox*Listbox.Background', TEMA.panel)
    raiz.option_add('*TCombobox*Listbox.Foreground', TEMA.texto)
    raiz.option_add('*TCombobox*Listbox.SelectBackground', TEMA.acento)
    raiz.option_add('*TCombobox*Listbox.SelectForeground', TEMA.panel)

    estilo.configure('TSpinbox', fieldbackground=TEMA.panel, background=TEMA.boton_fondo,
                     foreground=TEMA.texto, bordercolor=TEMA.acento, arrowcolor=TEMA.texto)

    estilo.configure('TFrame', background=TEMA.fondo)
    estilo.configure('Panel.TFrame', background=TEMA.panel)
    estilo.configure('TSeparator', background=TEMA.borde)
    estilo.configure('TScrollbar', background=TEMA.boton_fondo, troughcolor=TEMA.fondo,
                     bordercolor=TEMA.borde, arrowcolor=TEMA.texto)

    estilo.configure('Treeview', background=TEMA.panel, fieldbackground=TEMA.panel,
                     foreground=TEMA.texto, bordercolor=TEMA.borde, rowheight=20,
                     font=(FUENTE, TAM_FUENTE))
    estilo.map('Treeview', background=[('selected', TEMA.acento)],
               foreground=[('selected', TEMA.panel)])
    estilo.configure('Treeview.Heading', background=TEMA.fondo, foreground=TEMA.texto,
                     font=(FUENTE, TAM_FUENTE), relief='raised', bordercolor=TEMA.borde)

    estilo.configure('TNotebook', background=TEMA.fondo, bordercolor=TEMA.borde)
    estilo.configure('TNotebook.Tab', background=TEMA.fondo, foreground=TEMA.texto,
                     font=(FUENTE, TAM_FUENTE), padding=(10, 3), bordercolor=TEMA.borde)
    estilo.map('TNotebook.Tab', background=[('selected', TEMA.panel)],
               foreground=[('selected', TEMA.texto)])


def crear_encabezado(padre, titulo, subtitulo, aviso):
    marco = tk.Frame(padre, bg=TEMA.fondo)
    tk.Label(marco, text=titulo, bg=TEMA.fondo, fg=TEMA.texto,
             font=(FUENTE, TAM_FUENTE, 'bold'), anchor='w', justify='left').pack(fill='x')
    tk.Label(marco, text=subtitulo, bg=TEMA.fondo, fg=TEMA.texto,
             font=(FUENTE, TAM_FUENTE), anchor='w', justify='left').pack(fill='x')
    tk.Label(marco, text=aviso, bg=TEMA.fondo, fg=TEMA.texto,
             font=(FUENTE, TAM_FUENTE), anchor='w', justify='left').pack(fill='x')
    return marco


def crear_seccion(padre, titulo):
    marco = tk.Frame(padre, bg=TEMA.panel, highlightbackground=TEMA.seccion_borde,
                     highlightcolor=TEMA.seccion_borde, highlightthickness=1)
    cabecera = tk.Frame(marco, bg=TEMA.seccion_fondo)
    cabecera.pack(fill='x')
    tk.Label(cabecera, text=titulo, bg=TEMA.seccion_fondo, fg=TEMA.seccion_texto,
             font=(FUENTE, TAM_FUENTE, 'bold'), anchor='w').pack(side='left', padx=8, pady=3)
    cuerpo = tk.Frame(marco, bg=TEMA.panel)
    cuerpo.pack(fill='both', expand=True)
    return marco, cuerpo


def crear_tarjeta(padre, titulo, color):
    marco = tk.Frame(
        padre,
        bg=TEMA.tarjeta_fondo,
        highlightbackground=color,
        highlightcolor=color,
        highlightthickness=TEMA.tarjeta_borde_grosor,
    )
    lbl_titulo = tk.Label(marco, text=titulo, bg=TEMA.tarjeta_fondo, fg=TEMA.texto, font=(FUENTE, TAM_FUENTE, 'bold'))
    lbl_temp = tk.Label(marco, text='--', bg=TEMA.tarjeta_fondo, fg=TEMA.texto, font=(FUENTE, TAM_FUENTE, 'bold'))
    lbl_detalle = tk.Label(marco, text='', bg=TEMA.tarjeta_fondo, fg=TEMA.texto, font=(FUENTE, TAM_FUENTE))
    lbl_titulo.pack(padx=24, pady=(10, 0))
    lbl_temp.pack(padx=24)
    lbl_detalle.pack(padx=24, pady=(0, 10))
    return marco, lbl_temp, lbl_detalle


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