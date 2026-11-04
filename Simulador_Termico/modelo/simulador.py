"""Modelo térmico de dos nodos: CPU y disipador.

Ecuaciones diferenciales (balance de energía, 1.ª ley):
    Cc · dTc/dt = P − G·(Tc − Td)
    Cd · dTd/dt = G·(Tc − Td) − H·(Td − Ta)

Se integran con el método de Euler explícito, que es la definición de
derivada despejada:   T(t + Δt) ≈ T(t) + Δt · dT/dt

Este módulo NO depende de Tkinter: se puede probar por separado (ver tests/).
"""
from __future__ import annotations

from dataclasses import dataclass

from .parametros import Parametros


@dataclass(frozen=True)
class Entradas:
    carga: float              
    ventilador: float         
    ambiente: float         
    proteccion: bool = True   


@dataclass(frozen=True)
class Balance:
    potencia: float     
    conduccion: float   
    salida: float      
    dtc_dt: float      
    dtd_dt: float       
    throttling: bool
    apagado: bool


class Simulador:
    def __init__(self, params: Parametros | None = None, t_inicial: float = 28.0):
        self.p = params or Parametros()
        self.reiniciar(t_inicial)

    def reiniciar(self, t_inicial: float) -> None:
        self.t_cpu = self.t_disipador = t_inicial
        self.tiempo = 0.0
        self.energia_j = 0.0      
        self.throttling = False
        self.apagado = False      

    
    def potencia(self, e: Entradas) -> float:
        if self.apagado:
            return 0.0
        base = self.p.potencia(e.carga)
        return base * self.p.factor_throttling if self.throttling else base

    def balance(self, e: Entradas) -> Balance:
        """Única fuente de verdad para P, flujos y derivadas. No modifica el estado."""
        p = self.potencia(e)
        q = self.p.g_conduccion * (self.t_cpu - self.t_disipador)
        s = self.p.h(e.ventilador) * (self.t_disipador - e.ambiente)
        return Balance(
            potencia=p, conduccion=q, salida=s,
            dtc_dt=(p - q) / self.p.c_cpu,
            dtd_dt=(q - s) / self.p.c_disipador,
            throttling=self.throttling, apagado=self.apagado,
        )

    def equilibrio(self, e: Entradas) -> tuple[float, float]:
        """(Tc, Td) cuando dTc/dt = dTd/dt = 0, sin protección térmica."""
        p = self.p.potencia(e.carga)
        td = e.ambiente + p / self.p.h(e.ventilador)
        return td + p / self.p.g_conduccion, td

    def constante_tiempo_disipador(self, ventilador: float) -> float:
        """τ = Cd / H: tiempo en que el disipador recorre ~63 % del cambio."""
        return self.p.c_disipador / self.p.h(ventilador)

    def avanzar(self, e: Entradas, dt: float = 0.05) -> Balance:
        self._actualizar_proteccion(e.proteccion)
        b = self.balance(e)
        self.t_cpu += dt * b.dtc_dt          
        self.t_disipador += dt * b.dtd_dt
        self.energia_j += b.potencia * dt    
        self.tiempo += dt
        return b

    def _actualizar_proteccion(self, activa: bool) -> None:
        if not activa:
            self.throttling = False
            return
        if self.t_cpu >= self.p.t_apagado:
            self.apagado = True
        
        if self.t_cpu >= self.p.t_max:
            self.throttling = True
        elif self.t_cpu <= self.p.t_max - self.p.t_histeresis:
            self.throttling = False
