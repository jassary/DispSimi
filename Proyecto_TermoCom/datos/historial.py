"""Registro de la simulación y exportación a CSV."""
from __future__ import annotations

import csv
from collections import deque
from typing import NamedTuple


class Registro(NamedTuple):
    tiempo_s: float
    cpu_C: float
    disipador_C: float
    ambiente_C: float
    carga: float
    ventilador: float
    potencia_W: float
    dtc_dt: float
    dtd_dt: float
    throttling: int
    apagado: int


class Historial:
    ENCABEZADO = ['tiempo_s', 'cpu_C', 'disipador_C', 'ambiente_C', 'carga_%',
                  'ventilador_%', 'potencia_W', 'dTcpu_dt_C_s', 'dTdis_dt_C_s',
                  'throttling', 'apagado']

    def __init__(self, max_registros: int = 100_000):
        self._datos: deque[Registro] = deque(maxlen=max_registros)

    def __len__(self) -> int:
        return len(self._datos)

    def agregar(self, r: Registro) -> None:
        self._datos.append(r)

    def limpiar(self) -> None:
        self._datos.clear()

    def ultimos(self, segundos: float) -> list[Registro]:
        """Registros de los últimos `segundos` simulados (recorre desde el final)."""
        if not self._datos:
            return []
        inicio = self._datos[-1].tiempo_s - segundos
        seleccion = []
        for r in reversed(self._datos):
            if r.tiempo_s < inicio:
                break
            seleccion.append(r)
        seleccion.reverse()
        return seleccion

    def exportar_csv(self, ruta: str, separador: str = ';') -> None:
        """';' para que Excel en español separe bien las columnas."""
        with open(ruta, 'w', newline='', encoding='utf-8-sig') as f:
            w = csv.writer(f, delimiter=separador)
            w.writerow(self.ENCABEZADO)
            for r in self._datos:
                w.writerow([round(v, 4) if isinstance(v, float) else v for v in r])
