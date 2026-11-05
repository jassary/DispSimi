"""Sliders, botones, velocidad, escenarios y opciones."""
from __future__ import annotations

import tkinter as tk
from tkinter import ttk
from typing import Callable

from config import ESCENARIOS, VELOCIDADES, Tema
from modelo.simulador import Entradas


class PanelControles(ttk.Frame):
    """Lo único que app.py usa: entradas(), velocidad(), mostrar_tangentes(), set_pausado()."""

    SLIDERS = (
        ('Carga del procesador (%)', 'carga', 0, 100, 25),
        ('Ventilador (%)', 'ventilador', 0, 100, 50),
        ('Temperatura ambiente (°C)', 'ambiente', 10, 40, 28),
    )

    def __init__(self, master, tema: Tema, *,
                 on_pausar: Callable[[], None],
                 on_reiniciar: Callable[[], None],
                 on_exportar: Callable[[], None],
                 on_guia: Callable[[], None]):
        super().__init__(master, padding=8)
        self.tema = tema
        self._vars: dict[str, tk.DoubleVar] = {}
        self._velocidad = tk.StringVar(value=VELOCIDADES[0])
        self._proteccion = tk.BooleanVar(value=True)
        self._tangentes = tk.BooleanVar(value=True)

        self._crear_sliders()
        self._crear_botones(on_pausar, on_reiniciar, on_exportar, on_guia)
        self._crear_opciones()

    # ---------- construcción ----------
    def _crear_sliders(self) -> None:
        zona = ttk.Frame(self)
        zona.pack(fill='x')
        for col, (nombre, attr, minimo, maximo, inicial) in enumerate(self.SLIDERS):
            var = tk.DoubleVar(value=inicial)
            self._vars[attr] = var

            marco = ttk.Frame(zona, padding=4)
            marco.grid(row=0, column=col, sticky='ew')
            zona.columnconfigure(col, weight=1)

            ttk.Label(marco, text=nombre).pack()
            tk.Scale(marco, from_=minimo, to=maximo, orient='horizontal',
                     variable=var, length=260,
                     bg=self.tema.fondo, fg=self.tema.texto,
                     troughcolor=self.tema.panel,
                     highlightthickness=0).pack(fill='x')

    def _crear_botones(self, on_pausar, on_reiniciar, on_exportar, on_guia) -> None:
        barra = ttk.Frame(self, padding=(0, 8, 0, 0))
        barra.pack(fill='x')

        self._boton_pausa = ttk.Button(barra, text='Pausar', command=on_pausar)
        self._boton_pausa.pack(side='left', padx=4)
        ttk.Button(barra, text='Reiniciar', command=on_reiniciar).pack(side='left', padx=4)
        ttk.Button(barra, text='Guardar datos CSV', command=on_exportar).pack(side='left', padx=4)
        ttk.Button(barra, text='Guía para exponer', command=on_guia).pack(side='left', padx=4)

        ttk.Label(barra, text='Velocidad:').pack(side='left', padx=(18, 4))
        ttk.Combobox(barra, textvariable=self._velocidad, values=VELOCIDADES,
                     state='readonly', width=4).pack(side='left')
        ttk.Label(barra, text='× tiempo simulado').pack(side='left')

    def _crear_opciones(self) -> None:
        fila = ttk.Frame(self, padding=(0, 6, 0, 0))
        fila.pack(fill='x')

        ttk.Label(fila, text='Escenario:').pack(side='left', padx=(4, 4))
        combo = ttk.Combobox(fila, values=list(ESCENARIOS), state='readonly', width=20)
        combo.set('Elegir…')
        combo.bind('<<ComboboxSelected>>', lambda _e: self.aplicar_escenario(combo.get()))
        combo.pack(side='left')

        ttk.Checkbutton(fila, text='Protección térmica (throttling y apagado)',
                        variable=self._proteccion).pack(side='left', padx=(18, 0))
        ttk.Checkbutton(fila, text='Mostrar rectas tangentes (dT/dt)',
                        variable=self._tangentes).pack(side='left', padx=(18, 0))

    def aplicar_escenario(self, nombre: str) -> None:
        carga, ventilador, ambiente = ESCENARIOS[nombre]
        self._vars['carga'].set(carga)
        self._vars['ventilador'].set(ventilador)
        self._vars['ambiente'].set(ambiente)

    def entradas(self) -> Entradas:
        """Lee los controles UNA vez y devuelve un objeto del modelo."""
        return Entradas(
            carga=self._vars['carga'].get(),
            ventilador=self._vars['ventilador'].get(),
            ambiente=self._vars['ambiente'].get(),
            proteccion=self._proteccion.get(),
        )

    def velocidad(self) -> int:
        return int(self._velocidad.get())

    def mostrar_tangentes(self) -> bool:
        return self._tangentes.get()

    def set_pausado(self, pausado: bool) -> None:
        """Cambia el texto del botón según el estado de la simulación."""
        self._boton_pausa.configure(text='Continuar' if pausado else 'Pausar')
