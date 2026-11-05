"""Gráfica de dos ensayos con condiciones iniciales comunes."""
import math
import tkinter as tk

from config import TEMA
from modelo.experimentos import ensayar
from modelo.simulador import Entradas


def mostrar_comparacion(parent, entradas: Entradas) -> None:
    a, b = (ensayar(entradas.carga, entradas.ambiente, ventilador, entradas.proteccion)
            for ventilador in (30, 80))
    ventana = tk.Toplevel(parent)
    ventana.title('Comparación A/B · Ventilación')
    ventana.geometry('790x470')
    ventana.minsize(620, 380)
    ventana.configure(bg=TEMA.fondo)
    tk.Label(ventana, text='Comparación A/B · Temperatura de la CPU',
             bg=TEMA.cabecera, fg='white', font=('Segoe UI', 16, 'bold'),
             pady=10).pack(fill='x')
    proteccion = 'activa' if entradas.proteccion else 'desactivada'
    tk.Label(ventana, bg=TEMA.fondo, fg=TEMA.texto,
             text=f'Carga {entradas.carga:.0f} %   ·   Ambiente inicial {entradas.ambiente:.0f} °C'
                  f'   ·   Protección {proteccion}   ·   120 s simulados').pack(pady=7)
    tk.Label(ventana, bg=TEMA.fondo, fg=TEMA.texto, font=('Segoe UI', 11, 'bold'),
             text=f'A · 30 %   Máx. {a.maxima:.1f} °C     B · 80 %   Máx. {b.maxima:.1f} °C'
                  f'     Diferencia A − B: {a.maxima - b.maxima:+.1f} °C').pack(pady=(0, 6))
    grafica = tk.Canvas(ventana, bg='white', highlightthickness=0)
    grafica.pack(fill='both', expand=True, padx=16, pady=(0, 16))
    minimo = math.floor(entradas.ambiente / 10) * 10
    maximo = max(minimo + 20, math.ceil((max(a.maxima, b.maxima) + 2) / 10) * 10)

    def dibujar(evento):
        grafica.delete('all')
        izq, der, arriba, abajo = 51, evento.width - 23, 34, evento.height - 35

        def x(segundo):
            return izq + segundo / 120 * (der - izq)

        def y(temperatura):
            return abajo - (temperatura - minimo) / (maximo - minimo) * (abajo - arriba)

        for i in range(6):
            valor = minimo + (maximo - minimo) * i / 5
            grafica.create_line(izq, y(valor), der, y(valor), fill=TEMA.rejilla)
            grafica.create_text(izq - 8, y(valor), text=f'{valor:.0f}', anchor='e')
        for segundo in range(0, 121, 20):
            grafica.create_text(x(segundo), abajo + 14, text=str(segundo))
        grafica.create_text(izq - 8, 15, text='°C', anchor='e')
        grafica.create_text(der, abajo + 27, text='Tiempo (s)', anchor='e')
        for ensayo, color, etiqueta, origen in (
            (a, TEMA.cpu, 'A · Ventilador 30 %', izq),
            (b, TEMA.ambiente, 'B · Ventilador 80 %', izq + 160),
        ):
            puntos = [coordenada for t, temp in ensayo.muestras for coordenada in (x(t), y(temp))]
            grafica.create_line(*puntos, fill=color, width=3)
            grafica.create_text(origen, 15, anchor='w', fill=color, text=etiqueta)

    grafica.bind('<Configure>', dibujar)
