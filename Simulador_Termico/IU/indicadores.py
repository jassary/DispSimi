"""Lecturas numéricas: temperaturas, estado, derivadas, equilibrio y energía."""
from __future__ import annotations

import tkinter as tk

from config import Tema
from modelo.simulador import Balance, Entradas, Simulador


class PanelIndicadores(tk.Frame):
    UMBRAL_EQUILIBRIO = 0.005   

    def __init__(self, master, tema: Tema):
        super().__init__(master, bg=tema.fondo)
        self.tema = tema
        fila = tk.Frame(self, bg=tema.fondo)
        fila.pack()
        self._principal = tk.Label(fila, font=('Arial', 14, 'bold'), fg=tema.texto, bg=tema.fondo)
        self._principal.pack(side='left')
        self._estado = tk.Label(fila, font=('Arial', 12, 'bold'), bg=tema.fondo)
        self._estado.pack(side='left', padx=14)
        self._derivadas = tk.Label(self, font=('Arial', 11), fg=tema.texto, bg=tema.fondo)
        self._derivadas.pack()
        self._extra = tk.Label(self, font=('Arial', 10), fg=tema.texto_secundario, bg=tema.fondo)
        self._extra.pack()

    def actualizar(self, sim: Simulador, e: Entradas, b: Balance) -> None:
        self._principal.configure(
            text=f'CPU: {sim.t_cpu:.1f} °C    Disipador: {sim.t_disipador:.1f} °C    '
                 f'Potencia: {b.potencia:.0f} W    Tiempo: {sim.tiempo:.0f} s')
        texto, color = self._estado_cpu(sim.t_cpu, b)
        self._estado.configure(text=texto, fg=color)
        self._derivadas.configure(
            text=f'dT/dt CPU: {b.dtc_dt:+.3f} °C/s {self._tendencia(b.dtc_dt)}      '
                 f'dT/dt disipador: {b.dtd_dt:+.3f} °C/s {self._tendencia(b.dtd_dt)}')
        tc_eq, td_eq = sim.equilibrio(e)
        self._extra.configure(
            text=f'Equilibrio previsto (dT/dt = 0, sin protección): CPU {tc_eq:.0f} °C, '
                 f'disipador {td_eq:.0f} °C   •   τ disipador = Cd/H = '
                 f'{sim.constante_tiempo_disipador(e.ventilador):.0f} s   •   '
                 f'Energía E = ∫P dt = {sim.energia_j / 1000:.2f} kJ')

    def _tendencia(self, derivada: float) -> str:
        if derivada > self.UMBRAL_EQUILIBRIO:
            return '▲ se calienta'
        if derivada < -self.UMBRAL_EQUILIBRIO:
            return '▼ se enfría'
        return '≈ equilibrio'

    def _estado_cpu(self, t_cpu: float, b: Balance) -> tuple[str, str]:
        t = self.tema
        if b.apagado:
            return '⛔ Apagado de emergencia', t.limite
        if b.throttling:
            return '⚠ Throttling activo', t.limite
        if t_cpu < 60:
            return '● Normal', t.ok
        if t_cpu < 85:
            return '● Caliente', t.aviso
        return '● Crítico (simulado)', t.limite
