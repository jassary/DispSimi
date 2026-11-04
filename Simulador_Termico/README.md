# Simulador térmico: Termodinámica en la computadora

Simulación educativa de la **generación y disipación del calor en la placa madre**
para una feria científica. Python 3 + Tkinter, sin dependencias externas.
No usa sensores ni controla el equipo real.

## Ejecutar

```bash
python main.py
```

En Windows también funciona `py main.py`. En Linux, si falta tkinter, instale `python3-tk`.

## Pruebas

```bash
python tests/test_modelo.py     # sin instalar nada
python -m pytest tests          # si tiene pytest
```

## Estructura

```
Simulador_Termico/
├── main.py              Punto de entrada
├── config.py            Colores, tiempos y escenarios
├── modelo/              Física (no depende de Tkinter)
│   ├── parametros.py    Constantes: capacidades, G, H, potencia, umbrales
│   └── simulador.py     Ecuaciones diferenciales, Euler, derivadas, equilibrio
├── datos/
│   └── historial.py     Registro de la simulación y exportación CSV (;)
├── IU/                  Interfaz gráfica
│   ├── app.py           Ventana principal: conecta todo
│   ├── controles.py     Sliders, botones, escenarios, opciones
│   ├── indicadores.py   Temperaturas, estado, dT/dt, equilibrio, energía
│   ├── esquema.py       Diagrama CPU → disipador → aire
│   ├── grafica.py       Curvas T(t) y rectas tangentes
│   └── guia.py          Texto de apoyo para exponer
└── tests/
    └── test_modelo.py   Pruebas de física y matemática
```

## Modelo

```
Ccpu · dTcpu/dt = P − G·(Tcpu − Tdis)
Cdis · dTdis/dt = G·(Tcpu − Tdis) − H·(Tdis − Tamb)
```

| Símbolo | Significado | Valor |
|---|---|---|
| P | potencia térmica de la CPU | 10 + 0,9·carga W |
| G | conducción CPU → disipador | 4 W/°C |
| H | convección disipador → aire | 0,4 + 0,026·ventilador W/°C |
| Ccpu, Cdis | capacidades térmicas | 12 y 60 J/°C |

- **Euler:** `T(t+Δt) ≈ T(t) + Δt·dT/dt` con Δt = 0,05 s.
- **Equilibrio:** `dT/dt = 0` → `Tdis = Tamb + P/H`, `Tcpu = Tdis + P/G`.
- **Energía:** `E = ∫ P dt`.
- **Protección:** throttling a 95 °C (histéresis de 5 °C) y apagado a 105 °C.

Los valores son ilustrativos, no están calibrados para una computadora particular.
