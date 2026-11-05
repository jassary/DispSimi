# tests/test_modelo.py
"""Pruebas del modelo físico.

Con pytest:      python -m pytest tests
Sin instalar nada: python tests/test_modelo.py
"""
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from modelo.simulador import Entradas, Simulador  # noqa: E402

DT = 0.05


def simular(sim, e, segundos, dt=DT):
    for _ in range(int(segundos / dt)):
        sim.avanzar(e, dt)


# ---------- física ----------
def test_regimen_estacionario_conserva_energia():
    s = Simulador()
    e = Entradas(carga=50, ventilador=100, ambiente=28, proteccion=False)
    simular(s, e, 2000)
    b = s.balance(e)
    assert abs(b.potencia - b.conduccion) < 0.01
    assert abs(b.conduccion - b.salida) < 0.01      # P = Q = salida


def test_mas_ventilador_enfria():
    def t_final(vent):
        s = Simulador()
        simular(s, Entradas(80, vent, 28, proteccion=False), 2000)
        return s.t_cpu
    assert t_final(100) < t_final(0)


def test_temperatura_nunca_baja_del_ambiente():
    s = Simulador(t_inicial=28)
    e = Entradas(carga=0, ventilador=100, ambiente=28)
    for _ in range(20_000):
        s.avanzar(e, DT)
        assert s.t_cpu >= e.ambiente - 1e-9
        assert s.t_disipador >= e.ambiente - 1e-9


def test_throttling_limita_temperatura():
    s = Simulador()
    e = Entradas(carga=100, ventilador=30, ambiente=28, proteccion=True)
    maximo = 0.0
    for _ in range(int(1500 / DT)):
        s.avanzar(e, DT)
        maximo = max(maximo, s.t_cpu)
    assert maximo < s.p.t_apagado
    assert not s.apagado


def test_apagado_de_emergencia_con_ventilador_averiado():
    s = Simulador()
    simular(s, Entradas(carga=100, ventilador=0, ambiente=28, proteccion=True), 1500)
    assert s.apagado
    assert s.t_cpu < s.p.t_max          # tras apagarse se enfría


def test_alcanza_equilibrio_teorico():
    s = Simulador()
    e = Entradas(carga=100, ventilador=100, ambiente=28, proteccion=False)
    simular(s, e, 2000)
    tc_eq, td_eq = s.equilibrio(e)
    assert abs(s.t_cpu - tc_eq) < 0.1
    assert abs(s.t_disipador - td_eq) < 0.1

def test_derivada_coincide_con_diferencia_central():
    """dT/dt del modelo ≈ [T(t+h) − T(t−h)] / 2h medido sobre la trayectoria."""
    dt = 0.001
    s = Simulador()
    e = Entradas(carga=100, ventilador=50, ambiente=28, proteccion=False)
    simular(s, e, 10, dt)
    t_antes = s.t_cpu
    s.avanzar(e, dt)
    derivada_modelo = s.balance(e).dtc_dt
    s.avanzar(e, dt)
    diferencia_central = (s.t_cpu - t_antes) / (2 * dt)
    assert abs(derivada_modelo - diferencia_central) < 1e-3


def test_derivada_inicial_es_potencia_entre_capacidad():
    s = Simulador(t_inicial=28)
    b = s.balance(Entradas(carga=100, ventilador=0, ambiente=28))
    assert abs(b.dtc_dt - 100 / 12) < 1e-9   
    assert b.dtd_dt == 0                       


def test_derivada_nula_en_equilibrio():
    s = Simulador()
    e = Entradas(carga=60, ventilador=100, ambiente=28, proteccion=False)
    simular(s, e, 2000)
    b = s.balance(e)
    assert abs(b.dtc_dt) < 1e-3 and abs(b.dtd_dt) < 1e-3


def test_energia_es_integral_de_la_potencia():
    s = Simulador()
    e = Entradas(carga=50, ventilador=50, ambiente=28, proteccion=False)
    simular(s, e, 100)
    assert abs(s.energia_j - s.p.potencia(50) * s.tiempo) < 1e-6


if __name__ == '__main__':
    pruebas = [f for n, f in sorted(globals().items()) if n.startswith('test_')]
    for prueba in pruebas:
        prueba()
        print(f'OK  {prueba.__name__}')
    print(f'\n{len(pruebas)} pruebas superadas')
