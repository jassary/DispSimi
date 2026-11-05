"""Ventana principal: conecta controles, modelo, historial y dibujos."""
from __future__ import annotations

from collections import deque
from dataclasses import replace
from pathlib import Path
import tkinter as tk
from tkinter import filedialog, messagebox, ttk

from config import (DT_SIMULACION, MARGEN_FUTURO_S, MAX_REGISTROS, PASOS_POR_TICK,
                    PERIODO_TICK_MS, TEMA, VENTANA_GRAFICA_S)
from datos.historial import Historial, Registro
from IU.comparacion import mostrar_comparacion
from IU.controles import PanelControles
from IU.esquema import Esquema
from IU.grafica import Grafica
from IU.guia import mostrar_guia
from IU.indicadores import PanelIndicadores
from modelo.experimentos import ventilacion_automatica
from modelo.simulador import Entradas, Simulador


class AplicacionSimulador(tk.Frame):
    def __init__(self, master: tk.Tk):
        super().__init__(master, bg=TEMA.fondo)
        self._configurar_ventana()

        self.sim = Simulador()
        self.hist = Historial(MAX_REGISTROS)
        self.activo = False
        self.eventos = deque(maxlen=300)
        self.ventilacion_auto = tk.BooleanVar()
        self.zoom = tk.StringVar(value='180')
        self.demo = tk.StringVar(value='Enfriamiento')
        self._demostracion = None
        self._exposicion = False

        self._construir_ui()
        self._atajos_teclado()
        self.reiniciar()
        self.controles.set_pausado(True)
        self.after(PERIODO_TICK_MS, self._tick)


    def _configurar_ventana(self) -> None:
        self.master.title('Termodinámica en la computadora | Feria científica')
        ancho = min(1160, self.master.winfo_screenwidth() - 30)
        alto = min(790, self.master.winfo_screenheight() - 80)
        self.master.geometry(f'{ancho}x{alto}')
        self.master.minsize(840, 620)
        self.master.option_add('*Font', ('Segoe UI', 10))
        self.master.configure(bg=TEMA.fondo)
        estilo = ttk.Style(self.master)
        estilo.theme_use('clam')
        estilo.configure('TButton', padding=(10, 5), foreground=TEMA.texto)
        estilo.configure('Accion.TButton', background=TEMA.acento, foreground='white')
        estilo.map('Accion.TButton', background=[('active', TEMA.cabecera)])
        for elemento in ('TFrame', 'TLabel', 'TCheckbutton'):
            estilo.configure(elemento, background=TEMA.fondo, foreground=TEMA.texto)

    def _construir_ui(self) -> None:
        cabecera = tk.Frame(self, bg=TEMA.cabecera, padx=18, pady=8)
        cabecera.pack(fill='x')
        logo = Path(__file__).resolve().parents[1] / 'logo_uni.png'
        self.logo = tk.PhotoImage(file=str(logo)).subsample(9, 9)
        tk.Label(cabecera, image=self.logo, bg='white', padx=9, pady=6).pack(
            side='left', padx=(0, 14))
        tk.Label(cabecera, text='UNIVERSIDAD NACIONAL DE INGENIERÍA  /  NICARAGUA',
                 font=('Segoe UI', 9, 'bold'), fg='#9FD9F4',
                 bg=TEMA.cabecera).pack(anchor='w')
        tk.Label(cabecera, text='Termodinámica en la computadora',
                 font=('Segoe UI', 21, 'bold'), fg='white',
                 bg=TEMA.cabecera).pack(anchor='w')

        self.controles = PanelControles(
            self, TEMA,
            on_pausar=self.pausar,
            on_paso=self.paso,
            on_reiniciar=self.reiniciar,
            on_exportar=self.exportar,
            on_guia=lambda: mostrar_guia(self.master),
        )
        self.controles.pack(fill='x', padx=16)
        self.herramientas = ttk.Frame(self, padding=(2, 2))
        self.herramientas.pack(fill='x', padx=16)
        ttk.Checkbutton(self.herramientas, text='Ventilador automático',
                        variable=self.ventilacion_auto, command=self._modo_ventilador).pack(side='left')
        ttk.Button(self.herramientas, text='Comparar A/B',
                   command=lambda: mostrar_comparacion(self.master, self._entradas())).pack(
                       side='left', padx=(10, 5))
        ttk.Label(self.herramientas, text='Zoom (s)').pack(side='left', padx=(5, 3))
        ttk.Combobox(self.herramientas, state='readonly', textvariable=self.zoom,
                     values=('30', '60', '180'), width=4).pack(side='left')
        ttk.Button(self.herramientas, text='Exposición · F11',
                   command=self.exposicion).pack(side='right')

        self.panel_demo = ttk.Frame(self, padding=(0, 4))
        ttk.Button(self.panel_demo, text='Salir · Esc', command=self.exposicion).pack(side='right')
        ttk.Combobox(self.panel_demo, state='readonly', textvariable=self.demo,
                     values=('Enfriamiento', 'Ventilador averiado', 'Recuperación'),
                     width=20).pack(side='left')
        ttk.Button(self.panel_demo, text='Iniciar demostración',
                   command=self.iniciar_demo).pack(side='left', padx=8)
        self.mensaje_demo = ttk.Label(self.panel_demo, text='Elige una demostración.')
        self.mensaje_demo.pack(side='left')

        self.indicadores = PanelIndicadores(self, TEMA)
        self.indicadores.pack(fill='x', padx=16, pady=4)

        self.esquema = Esquema(self, TEMA)
        self.esquema.pack(fill='x', padx=16, pady=4)

        self.grafica = Grafica(self, TEMA)
        self.grafica.pack(fill='both', expand=True, padx=16, pady=(4, 6))

        tk.Label(self, fg=TEMA.texto_secundario, bg=TEMA.fondo,
                 text='P  Iniciar o pausar     ·     R  Reiniciar     ·     Datos simulados').pack(pady=(0, 6))

    def _atajos_teclado(self) -> None:
        self.master.bind('<F11>', lambda _evento: self.exposicion())
        self.master.bind('<Escape>', lambda _evento: self._salir_exposicion())
        for tecla, accion in (('p', self.pausar), ('r', self.reiniciar)):
            self.master.bind(f'<KeyPress-{tecla}>', lambda _e, a=accion: a())
            self.master.bind(f'<KeyPress-{tecla.upper()}>', lambda _e, a=accion: a())

    def _tick(self) -> None:
        if self.activo:
            velocidad = 5 if self._demostracion else self.controles.velocidad()
            self._avanzar(PASOS_POR_TICK * velocidad)
        self._dibujar()
        self.after(PERIODO_TICK_MS, self._tick)

    def _entradas(self) -> Entradas:
        entradas = self.controles.entradas()
        if self.ventilacion_auto.get():
            entradas = replace(entradas, ventilador=ventilacion_automatica(self.sim.t_cpu))
        return entradas

    def _modo_ventilador(self) -> None:
        automatico = self.ventilacion_auto.get()
        self.controles.activar_ventilador_manual(not automatico)
        self.eventos.append((self.sim.tiempo, 'Ventilador automático' if automatico else 'Ventilador manual'))

    def _avanzar(self, pasos: int) -> None:
        e = self._entradas()
        if e != self._ajustes:
            for campo, etiqueta in (('carga', 'Carga'), ('ambiente', 'Ambiente'),
                                    ('ventilador', 'Ventilación'), ('proteccion', 'Protección')):
                if campo == 'ventilador' and self.ventilacion_auto.get():
                    continue
                if getattr(e, campo) != getattr(self._ajustes, campo):
                    self.eventos.append((self.sim.tiempo, etiqueta))
        for _ in range(pasos):
            e = self._entradas()
            reducia, apagada = self.sim.throttling, self.sim.apagado
            self.sim.avanzar(e, DT_SIMULACION)
            if self.sim.apagado and not apagada:
                self.eventos.append((self.sim.tiempo, 'Apagado térmico'))
            elif self.sim.throttling != reducia:
                self.eventos.append((self.sim.tiempo, 'Potencia reducida' if self.sim.throttling
                                     else 'Potencia restaurada'))
            if self._demostracion:
                self._actualizar_demo()
                if not self.activo:
                    break
        self._ajustes = self._entradas()
        self._registrar(self._ajustes)

    def paso(self) -> None:
        if self.activo:
            self.pausar()
        self._avanzar(1)
        self._dibujar()

    def _registrar(self, e: Entradas) -> None:
        s, b = self.sim, self.sim.balance(e)
        self.hist.agregar(Registro(
            s.tiempo, s.t_cpu, s.t_disipador, e.ambiente, e.carga, e.ventilador,
            b.potencia, b.dtc_dt, b.dtd_dt, int(b.throttling), int(b.apagado)))

    def _dibujar(self) -> None:
        e = self._entradas()
        b = self.sim.balance(e)
        self.indicadores.actualizar(self.sim, e, b)
        self.esquema.actualizar(self.sim.t_cpu, self.sim.t_disipador, e.ambiente, b, self.sim.tiempo)
        ventana = int(self.zoom.get())
        self.grafica.actualizar(
            self.hist.ultimos(ventana * (1 - MARGEN_FUTURO_S / VENTANA_GRAFICA_S)),
            limite=self.sim.p.t_max if e.proteccion else None,
            tangentes=self.controles.mostrar_tangentes(),
            ventana=ventana, eventos=tuple(self.eventos),
        )

    def pausar(self) -> None:
        self.activo = not self.activo
        self.controles.set_pausado(not self.activo)

    def reiniciar(self) -> None:
        e = self.controles.entradas()
        self.sim.reiniciar(e.ambiente)
        self.hist.limpiar()
        self.eventos.clear()
        self._demostracion = None
        self._ajustes = self._entradas()
        self._registrar(self._ajustes)
        self._dibujar()

    def exposicion(self) -> None:
        self._exposicion = not self._exposicion
        self.master.attributes('-fullscreen', self._exposicion)
        self.indicadores.modo_exposicion(self._exposicion)
        if self._exposicion:
            self.controles.pack_forget()
            self.herramientas.pack_forget()
            self.panel_demo.pack(fill='x', padx=16, before=self.indicadores)
        else:
            self.panel_demo.pack_forget()
            self.controles.pack(fill='x', padx=16, before=self.indicadores)
            self.herramientas.pack(fill='x', padx=16, before=self.indicadores)

    def _salir_exposicion(self) -> None:
        if self._exposicion:
            self.exposicion()

    def iniciar_demo(self) -> None:
        nombre = self.demo.get()
        self.ventilacion_auto.set(False)
        self._modo_ventilador()
        self.controles.activar_proteccion()
        self.controles.aplicar_escenario('Videojuego' if nombre == 'Enfriamiento'
                                         else 'Ventilador averiado')
        self.reiniciar()
        if nombre == 'Enfriamiento':
            self.sim.t_cpu, self.sim.t_disipador = 85.0, 65.0
            self.controles.ajustar(carga=5, ventilador=100)
            self.hist.limpiar()
            self._ajustes = self._entradas()
            self._registrar(self._ajustes)
        self._demostracion = nombre
        self.zoom.set('60' if nombre != 'Ventilador averiado' else '180')
        self.mensaje_demo.configure(text={
            'Enfriamiento': 'Observa cómo bajan las dos temperaturas.',
            'Ventilador averiado': 'Observa la reducción de potencia y el apagado.',
            'Recuperación': 'Al llegar a 75 °C, el ventilador subirá al 100 %.',
        }[nombre])
        if not self.activo:
            self.pausar()

    def _actualizar_demo(self) -> None:
        demo = self._demostracion
        if demo == 'Recuperación' and self.sim.t_cpu >= 75 and self._entradas().ventilador == 0:
            self.controles.ajustar(ventilador=100)
            self.eventos.append((self.sim.tiempo, 'Ventilador al 100 %'))
            self.mensaje_demo.configure(text='Ventilador al 100 %. Observa el cambio de pendiente.')
        if (demo == 'Ventilador averiado' and self.sim.apagado
                or demo in ('Enfriamiento', 'Recuperación') and self.sim.tiempo >= 55):
            self._demostracion = None
            self.mensaje_demo.configure(text='Ensayo terminado. Revisa la gráfica.')
            if self.activo:
                self.pausar()

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
