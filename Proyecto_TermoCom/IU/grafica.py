"""Curvas de temperatura en función del tiempo, con rectas tangentes (dT/dt)."""
from __future__ import annotations

import math
import tkinter as tk

from config import MARGEN_FUTURO_S, VENTANA_GRAFICA_S, Tema
from datos.historial import Registro


class Grafica(tk.Canvas):
    MARGENES = (55, 20, 32, 38)   
    TANGENTE_ATRAS_S = 15         
    def __init__(self, master, tema: Tema):
        super().__init__(master, bg=tema.grafica, highlightthickness=0)
        self.tema = tema
        self._estado = None
        self._vista = None
        self._cursor = None
        self.bind('<Motion>', self._mover_cursor)
        self.bind('<Leave>', self._quitar_cursor)
        self.bind('<Configure>', self._redimensionar)
        
        self.series = (('cpu_C', 'dtc_dt', tema.cpu),
                       ('disipador_C', 'dtd_dt', tema.disipador),
                       ('ambiente_C', None, tema.ambiente))

    def actualizar(self, filas: list[Registro], limite: float | None = None,
                   tangentes: bool = True, ventana: int = VENTANA_GRAFICA_S,
                   eventos: tuple[tuple[float, str], ...] = ()) -> None:
        estado = (filas, limite, tangentes, ventana, eventos)
        if estado == self._estado:
            return
        self._estado = estado
        self.delete('all')
        if not filas:
            self._vista = None
            return
        t = self.tema
        w, h = max(self.winfo_width(), 400), max(self.winfo_height(), 100)
        mi, md, ma, mb = self.MARGENES
        izq, der, arr, aba = mi, w - md, ma, h - mb

        actual = filas[-1]
        margen = ventana * MARGEN_FUTURO_S / VENTANA_GRAFICA_S
        inicio = max(0.0, actual.tiempo_s - (ventana - margen))
        maximo = max(max(r.cpu_C, r.disipador_C, r.ambiente_C) for r in filas)
        if limite is not None:
            maximo = max(maximo, limite)
        ymax = max(60, math.ceil((maximo + 5) / 20) * 20)

        def px(tiempo: float) -> float:
            return izq + (tiempo - inicio) / ventana * (der - izq)

        def py(temp: float) -> float:
            return aba - temp / ymax * (aba - arr)

        visibles = tuple((segundo, evento) for segundo, evento in eventos if segundo >= inicio)
        self._vista = (filas, inicio, izq, der, arr, aba, px, ventana, visibles)

        for i in range(6):
            valor = ymax * i / 5
            self.create_line(izq, py(valor), der, py(valor), fill=t.rejilla)
            self.create_text(izq - 8, py(valor), text=f'{valor:.0f}', anchor='e', fill=t.texto)
        for i in range(7):
            tiempo = inicio + ventana * i / 6
            self.create_text(px(tiempo), aba + 14, text=f'{tiempo:.0f}', fill=t.texto)
        self.create_text(8, 14, text='°C', anchor='w', fill=t.texto)
        self.create_text(der, aba + 30, text='Tiempo simulado (s)', anchor='e', fill=t.texto)
        leyenda = 'CPU (rojo)  •  Disipador (naranja)  •  Ambiente (azul)'
        if tangentes:
            leyenda += '  •  Punteadas: rectas tangentes, pendiente = dT/dt'
        self.create_text(izq, 14, anchor='w', text=leyenda, fill=t.texto)
        if visibles:
            self.create_text(der, 14, anchor='e', text='◆ Eventos', fill=t.acento)
        for segundo, etiqueta in visibles:
            x = px(segundo)
            color = t.limite if etiqueta == 'Apagado térmico' else t.acento
            self.create_line(x, arr, x, aba, fill=color, dash=(2, 4))
            self.create_polygon(x - 4, arr, x, arr - 4, x + 4, arr, x, arr + 4,
                                fill=color, outline='')

        if limite is not None:
            self.create_line(izq, py(limite), der, py(limite), fill=t.limite, dash=(6, 4))
            self.create_text(der - 4, py(limite) - 8, anchor='e', fill=t.limite,
                             text=f'Reducción de potencia · {limite:.0f} °C')

        for campo, _, color in self.series:
            puntos: list[float] = []
            for r in filas:
                puntos += (px(r.tiempo_s), py(getattr(r, campo)))
            if len(puntos) >= 4:
                self.create_line(*puntos, fill=color, width=2)

        if tangentes:
            for campo, derivada, color in self.series:
                if derivada is None:
                    continue
                t0, T0, m = actual.tiempo_s, getattr(actual, campo), getattr(actual, derivada)
                ta, tb = self._tramo_tangente(t0, T0, m, inicio, ymax, margen)
                self.create_line(px(ta), py(T0 + m * (ta - t0)), px(tb), py(T0 + m * (tb - t0)),
                                 fill=color, width=2, dash=(5, 3))
                self.create_oval(px(t0) - 4, py(T0) - 4, px(t0) + 4, py(T0) + 4,
                                 fill=color, outline=t.texto)

        if self._cursor:
            self._dibujar_cursor(*self._cursor)

    def _redimensionar(self, _evento) -> None:
        estado = self._estado
        if estado is not None:
            self._estado = None
            self.actualizar(*estado)

    def _mover_cursor(self, evento) -> None:
        self._cursor = (evento.x, evento.y)
        self._dibujar_cursor(*self._cursor)

    def _quitar_cursor(self, _evento) -> None:
        self._cursor = None
        self.delete('cursor')

    def _dibujar_cursor(self, x: int, y: int) -> None:
        self.delete('cursor')
        if self._vista is None:
            return
        filas, inicio, izq, der, arr, aba, px, ventana, eventos = self._vista
        if not (izq <= x <= der and arr <= y <= aba):
            return
        tiempo = inicio + (x - izq) * ventana / (der - izq)
        punto = min(filas, key=lambda fila: abs(fila.tiempo_s - tiempo))
        pos = px(punto.tiempo_s)
        self.create_line(pos, arr, pos, aba, fill=self.tema.texto_secundario, dash=(2, 4),
                         tags='cursor')
        etiqueta = (f'{punto.tiempo_s:.2f} s  |  CPU {punto.cpu_C:.1f} °C  |  '
                    f'Disipador {punto.disipador_C:.1f} °C  |  Aire {punto.ambiente_C:.1f} °C')
        cercanos = [(abs(px(t) - x), t) for t, _ in eventos if abs(px(t) - x) <= 7]
        if cercanos:
            _, evento_t = min(cercanos)
            etiquetas = dict.fromkeys(nombre for t, nombre in eventos if t == evento_t)
            etiqueta = f'{evento_t:.2f} s · ' + ' / '.join(etiquetas)
        texto = self.create_text(izq + 6, aba - 13, text=etiqueta, anchor='w', fill=self.tema.texto,
                         font=('Segoe UI', 9, 'bold'), tags='cursor')
        fondo = self.create_rectangle(*self.bbox(texto), fill=self.tema.panel,
                                      outline=self.tema.rejilla, tags='cursor')
        self.tag_lower(fondo, texto)

    def _tramo_tangente(self, t0: float, T0: float, m: float,
                        inicio: float, ymax: float, margen: float) -> tuple[float, float]:
        """Intervalo [ta, tb] de la tangente recortado para no salirse del área."""
        ta, tb = max(inicio, t0 - self.TANGENTE_ATRAS_S), t0 + margen
        if m != 0:
            for borde in (0.0, ymax):
                t_borde = t0 + (borde - T0) / m
                if t_borde == t0:
                    if (borde == ymax and m > 0) or (borde == 0 and m < 0):
                        tb = t0
                    else:
                        ta = t0
                elif t_borde > t0:
                    tb = min(tb, t_borde)
                elif t_borde < t0:
                    ta = max(ta, t_borde)
        return ta, tb
