# IU/grafica.py
"""Curvas de temperatura en función del tiempo, con rectas tangentes (dT/dt)."""
from __future__ import annotations

import math
import tkinter as tk

from config import MARGEN_FUTURO_S, VENTANA_GRAFICA_S, Tema
from datos.historial import Registro


class Grafica(tk.Canvas):
    MARGENES = (55, 20, 32, 38)   # izquierda, derecha, arriba, abajo [px]
    TANGENTE_ATRAS_S = 15         # cuánto se dibuja la tangente hacia el pasado

    def __init__(self, master, tema: Tema):
        super().__init__(master, bg=tema.grafica, highlightthickness=0)
        self.tema = tema
        # (campo de temperatura, campo de derivada o None, color)
        self.series = (('cpu_C', 'dtc_dt', tema.cpu),
                       ('disipador_C', 'dtd_dt', tema.disipador),
                       ('ambiente_C', None, tema.ambiente))

    def actualizar(self, filas: list[Registro], limite: float | None = None,
                   tangentes: bool = True) -> None:
        self.delete('all')
        if not filas:
            return
        t = self.tema
        w, h = max(self.winfo_width(), 400), max(self.winfo_height(), 200)
        mi, md, ma, mb = self.MARGENES
        izq, der, arr, aba = mi, w - md, ma, h - mb

        actual = filas[-1]
        inicio = max(0.0, actual.tiempo_s - (VENTANA_GRAFICA_S - MARGEN_FUTURO_S))
        maximo = max(max(r.cpu_C, r.disipador_C, r.ambiente_C) for r in filas)
        if limite is not None:
            maximo = max(maximo, limite)
        ymax = max(60, math.ceil((maximo + 5) / 20) * 20)

        def px(tiempo: float) -> float:
            return izq + (tiempo - inicio) / VENTANA_GRAFICA_S * (der - izq)

        def py(temp: float) -> float:
            return aba - temp / ymax * (aba - arr)

        # Rejilla y ejes
        for i in range(6):
            valor = ymax * i / 5
            self.create_line(izq, py(valor), der, py(valor), fill=t.rejilla)
            self.create_text(izq - 8, py(valor), text=f'{valor:.0f}', anchor='e', fill=t.texto)
        for i in range(7):
            tiempo = inicio + VENTANA_GRAFICA_S * i / 6
            self.create_text(px(tiempo), aba + 14, text=f'{tiempo:.0f}', fill=t.texto)
        self.create_text(8, 14, text='°C', anchor='w', fill=t.texto)
        self.create_text(der, aba + 30, text='Tiempo simulado (s)', anchor='e', fill=t.texto)
        leyenda = 'CPU (rojo)  •  Disipador (naranja)  •  Ambiente (azul)'
        if tangentes:
            leyenda += '  •  Punteadas: rectas tangentes, pendiente = dT/dt'
        self.create_text(izq, 14, anchor='w', text=leyenda, fill=t.texto)

        if limite is not None:
            self.create_line(izq, py(limite), der, py(limite), fill=t.limite, dash=(6, 4))
            self.create_text(der - 4, py(limite) - 8, anchor='e', fill=t.limite,
                             text=f'Límite de protección {limite:.0f} °C')

        # Curvas
        for campo, _, color in self.series:
            puntos: list[float] = []
            for r in filas:
                puntos += (px(r.tiempo_s), py(getattr(r, campo)))
            if len(puntos) >= 4:
                self.create_line(*puntos, fill=color, width=2)

        # Rectas tangentes:  T(t) ≈ T(t0) + (dT/dt)·(t − t0)
        if tangentes:
            for campo, derivada, color in self.series:
                if derivada is None:
                    continue
                t0, T0, m = actual.tiempo_s, getattr(actual, campo), getattr(actual, derivada)
                ta, tb = self._tramo_tangente(t0, T0, m, inicio, ymax)
                self.create_line(px(ta), py(T0 + m * (ta - t0)), px(tb), py(T0 + m * (tb - t0)),
                                 fill=color, width=2, dash=(5, 3))
                self.create_oval(px(t0) - 4, py(T0) - 4, px(t0) + 4, py(T0) + 4,
                                 fill=color, outline=t.texto)

    def _tramo_tangente(self, t0: float, T0: float, m: float,
                        inicio: float, ymax: float) -> tuple[float, float]:
        """Intervalo [ta, tb] de la tangente recortado para no salirse del área."""
        ta, tb = max(inicio, t0 - self.TANGENTE_ATRAS_S), t0 + MARGEN_FUTURO_S
        if m != 0:
            for borde in (0.0, ymax):
                t_borde = t0 + (borde - T0) / m
                if t_borde > t0:
                    tb = min(tb, t_borde)
                elif t_borde < t0:
                    ta = max(ta, t_borde)
        return ta, tb
