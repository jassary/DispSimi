# IU/esquema.py
"""Diagrama de flujo de calor: CPU → disipador → aire."""
from __future__ import annotations

import tkinter as tk

from config import Tema
from modelo.simulador import Balance


class Esquema(tk.Canvas):
    ALTO = 140
    ANCHO_MIN = 800
    Y_SUP, Y_INF = 22, 108        
    Y_FLECHA = 65
    NOTA = ('El ventilador mueve aire: no produce frío. '
            'El calor fluye espontáneamente hacia zonas de menor temperatura.')
    CAJAS = (('cpu', 0.17, 'PROCESADOR'),
             ('disipador', 0.50, 'DISIPADOR'),
             ('aire', 0.83, 'AIRE AMBIENTE'))

    def __init__(self, master, tema: Tema):
        super().__init__(master, height=self.ALTO, bg=tema.panel, highlightthickness=0)
        self.tema = tema
        self._ultimo: tuple | None = None
        self._ids: dict[str, int] = {}
        self.bind('<Configure>', self._al_redimensionar)
        self._construir()

    def _construir(self) -> None:
        self.delete('all')
        self._ids.clear()
        t = self.tema
        w = max(self.winfo_width(), self.ANCHO_MIN)
        m = min(110, w * 0.12)            
        colores = {'cpu': t.cpu, 'disipador': t.disipador, 'aire': t.ambiente}
        centros = []

        for clave, frac, titulo in self.CAJAS:
            x = w * frac
            centros.append(x)
            self.create_rectangle(x - m, self.Y_SUP, x + m, self.Y_INF,
                                  fill=colores[clave], outline=t.texto, width=1)
            self.create_text(x, self.Y_SUP + 14, text=titulo, fill=t.texto,
                             font=('Arial', 10, 'bold'))
            self._ids[f't_{clave}'] = self.create_text(
                x, self.Y_SUP + 42, text='--.- °C', fill=t.texto, font=('Arial', 16, 'bold'))
            self._ids[f'd_{clave}'] = self.create_text(
                x, self.Y_SUP + 68, text='', fill=t.texto, font=('Arial', 9))

        for nombre, (x1, x2) in zip(('q_conduccion', 'q_salida'), zip(centros, centros[1:])):
            self.create_line(x1 + m + 4, self.Y_FLECHA, x2 - m - 4, self.Y_FLECHA,
                             arrow='last', width=3, fill=t.texto)
            self._ids[nombre] = self.create_text((x1 + x2) / 2, self.Y_FLECHA - 12, text='',
                                                 fill=t.texto, font=('Arial', 9, 'bold'))

        self.create_text(w / 2, self.ALTO - 12, text=self.NOTA,
                         fill=t.texto_secundario, font=('Arial', 9, 'italic'))
        self._ids['aviso'] = self.create_text(w * 0.17, 10, text='', fill=t.limite,
                                              font=('Arial', 9, 'bold'))

    def _al_redimensionar(self, _evento) -> None:
        self._construir()
        if self._ultimo:
            self.actualizar(*self._ultimo)

    def actualizar(self, t_cpu: float, t_disipador: float, t_ambiente: float,
                   balance: Balance) -> None:
        self._ultimo = (t_cpu, t_disipador, t_ambiente, balance)
        cambios = {
            't_cpu': f'{t_cpu:.1f} °C',
            't_disipador': f'{t_disipador:.1f} °C',
            't_aire': f'{t_ambiente:.1f} °C',
            'd_cpu': f'Genera {balance.potencia:.0f} W',
            'd_disipador': f'Almacena {balance.conduccion - balance.salida:+.1f} W',
            'd_aire': f'Recibe {balance.salida:.1f} W',
            'q_conduccion': f'Conducción {balance.conduccion:.1f} W',
            'q_salida': f'Convección {balance.salida:.1f} W',
            'aviso': ('⛔ APAGADO DE EMERGENCIA (pulse Reiniciar)' if balance.apagado else
                      '⚠ PROTECCIÓN TÉRMICA: potencia reducida' if balance.throttling else ''),
        }
        for clave, texto in cambios.items():
            self.itemconfig(self._ids[clave], text=texto)
