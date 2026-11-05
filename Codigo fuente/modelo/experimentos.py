"""Ensayos reproducibles y control de ventilación."""
from dataclasses import dataclass

from config import DT_SIMULACION
from modelo.simulador import Entradas, Simulador


def ventilacion_automatica(temperatura: float) -> float:
    """20 % a 45 °C, 100 % a 85 °C y rampa lineal entre ambos."""
    return min(100.0, max(20.0, 20.0 + 2.0 * (temperatura - 45.0)))


@dataclass(frozen=True)
class Ensayo:
    muestras: tuple[tuple[float, float], ...]
    maxima: float


def ensayar(carga: float, ambiente: float, ventilador: float, proteccion: bool) -> Ensayo:
    simulador = Simulador(t_inicial=ambiente)
    entradas = Entradas(carga, ventilador, ambiente, proteccion)
    por_segundo = round(1 / DT_SIMULACION)
    muestras = [(0.0, ambiente)]
    maxima = ambiente
    for segundo in range(1, 121):
        for _ in range(por_segundo):
            simulador.avanzar(entradas, DT_SIMULACION)
            maxima = max(maxima, simulador.t_cpu)
        muestras.append((segundo, simulador.t_cpu))
    return Ensayo(tuple(muestras), maxima)
