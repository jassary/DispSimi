# IU/app.py
"""Ventana principal: conecta controles, modelo, historial y dibujos."""
from __future__ import annotations

import tkinter as tk
from tkinter import filedialog, messagebox, ttk

from config import (DT_SIMULACION, MARGEN_FUTURO_S, MAX_REGISTROS, PASOS_POR_TICK,
                    PERIODO_TICK_MS, TEMA, VENTANA_GRAFICA_S)
from datos.historial import Historial, Registro
from IU.controles import PanelControles
from IU.esquema import Esquema
from IU.grafica import Grafica
from IU.guia import mostrar_guia
from IU.indicadores import PanelIndicadores
from modelo.simulador import Entradas, Simulador


class AplicacionSimulador(tk.Frame):
    def __init__(self, master: tk.Tk):
        super().__init__(master, bg=TEMA.fondo)
        self._configurar_ventana()

        self.sim = Simulador()
        self.hist = Historial(MAX_REGISTROS)
        self.activo = True

        self._construir_ui()
        self._atajos_teclado()
        self.reiniciar()
        self.after(PERIODO_TICK_MS, self._tick)

    # ---------- construcción ----------
    def _configurar_ventana(self) -> None:
        self.master.title('Termodinámica en la computadora | Feria científica')
        self.master.geometry('1150x880')
        self.master.minsize(950, 740)
        self.master.configure(bg=TEMA.fondo)
        estilo = ttk.Style(self.master)
        for elemento in ('TFrame', 'TLabel', 'TCheckbutton'):
            estilo.configure(elemento, background=TEMA.fondo, foreground=TEMA.texto)

    def _construir_ui(self) -> None:
        tk.Label(self, text='TERMODINÁMICA EN LA COMPUTADORA', font=('Arial', 22, 'bold'),
                 fg=TEMA.ambiente, bg=TEMA.fondo).pack(pady=(10, 0))
        tk.Label(self, text='Generación y disipación del calor en la placa madre',
                 font=('Arial', 13), fg=TEMA.texto, bg=TEMA.fondo).pack()
        tk.Label(self, text='SIMULACIÓN EDUCATIVA • No utiliza sensores ni controla el equipo real',
                 fg=TEMA.aviso, bg=TEMA.fondo).pack(pady=(2, 0))

        self.controles = PanelControles(
            self, TEMA,
            on_pausar=self.pausar,
            on_reiniciar=self.reiniciar,
            on_exportar=self.exportar,
            on_guia=lambda: mostrar_guia(self.master),
        )
        self.controles.pack(fill='x', padx=16)

        self.indicadores = PanelIndicadores(self, TEMA)
        self.indicadores.pack(fill='x', padx=16, pady=4)

        self.esquema = Esquema(self, TEMA)
        self.esquema.pack(fill='x', padx=16, pady=4)

        self.grafica = Grafica(self, TEMA)
        self.grafica.pack(fill='both', expand=True, padx=16, pady=(4, 6))

        tk.Label(self, fg=TEMA.texto_secundario, bg=TEMA.fondo,
                 text='Atajos: P = pausar/continuar, R = reiniciar').pack(pady=(0, 6))

    def _atajos_teclado(self) -> None:
        for tecla, accion in (('p', self.pausar), ('r', self.reiniciar)):
            self.master.bind(f'<KeyPress-{tecla}>', lambda _e, a=accion: a())
            self.master.bind(f'<KeyPress-{tecla.upper()}>', lambda _e, a=accion: a())

    # ---------- bucle de simulación ----------
    def _tick(self) -> None:
        if self.activo:
            e = self.controles.entradas()
            for _ in range(PASOS_POR_TICK * self.controles.velocidad()):
                self.sim.avanzar(e, DT_SIMULACION)
            self._registrar(e)
        self._dibujar()
        self.after(PERIODO_TICK_MS, self._tick)

    def _registrar(self, e: Entradas) -> None:
        s, b = self.sim, self.sim.balance(e)
        self.hist.agregar(Registro(
            s.tiempo, s.t_cpu, s.t_disipador, e.ambiente, e.carga, e.ventilador,
            b.potencia, b.dtc_dt, b.dtd_dt, int(b.throttling), int(b.apagado)))

    def _dibujar(self) -> None:
        e = self.controles.entradas()
        b = self.sim.balance(e)
        self.indicadores.actualizar(self.sim, e, b)
        self.esquema.actualizar(self.sim.t_cpu, self.sim.t_disipador, e.ambiente, b)
        self.grafica.actualizar(
            self.hist.ultimos(VENTANA_GRAFICA_S - MARGEN_FUTURO_S),
            limite=self.sim.p.t_max if e.proteccion else None,
            tangentes=self.controles.mostrar_tangentes(),
        )

    # ---------- acciones del usuario ----------
    def pausar(self) -> None:
        self.activo = not self.activo
        self.controles.set_pausado(not self.activo)

    def reiniciar(self) -> None:
        e = self.controles.entradas()
        self.sim.reiniciar(e.ambiente)
        self.hist.limpiar()
        self._registrar(e)
        self._dibujar()

    def exportar(self) -> None:
        ruta = filedialog.asksaveasfilename(
            parent=self.master, defaultextension='.csv',
            initialfile='experimento_calor.csv', filetypes=[('CSV', '*.csv')])
        if not ruta:
            return
        try:
            self.hist.exportar_csv(ruta)
            messagebox.showinfo('Datos guardados',
                                f'Se guardaron {len(self.hist)} registros simulados.',
                                parent=self.master)
        except OSError as error:
            messagebox.showerror('No se pudo guardar', str(error), parent=self.master)
