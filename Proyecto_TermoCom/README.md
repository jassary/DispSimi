# Laboratorio térmico
## Termodinámica en la computadora

Simulador de física para observar cómo cambia la temperatura de un procesador según la carga, la ventilación y la temperatura ambiente. Diseño de laboratorio inspirado en la Universidad Nacional de Ingeniería de Nicaragua. Los parámetros son didácticos.

### Abrir en Windows

1. Extrae el ZIP completo.
2. Abre la carpeta `Laboratorio_Termico` y haz doble clic en `Iniciar.bat`.
3. Selecciona un escenario y pulsa **Ejecutar**.

Se requiere Python 3.10 o superior con Tkinter. En otros sistemas, abre una terminal en esta carpeta y ejecuta `python3 main.py`. En Linux, instala el paquete de Tkinter de tu distribución si hace falta.

### Herramientas de laboratorio

- **Comparar A/B** simula dos ensayos de 120 s con la carga, ambiente y protección seleccionados. Las dos curvas parten de la temperatura ambiente. El ventilador funciona al 30 % en A y al 80 % en B.
- **Ventilador automático** aplica 20 % hasta 45 °C y sube dos puntos porcentuales por cada grado adicional, hasta 100 % a 85 °C. El indicador muestra la velocidad efectiva.
- **Zoom** cambia la ventana de la gráfica a 30, 60 o 180 s. Pasa el puntero por un rombo para consultar el evento.
- **F11** abre el modo exposición. Elige Enfriamiento, Ventilador averiado o Recuperación e inicia la demostración. **Esc** vuelve al panel de control.
- El balance muestra la energía generada, la cedida al aire y la almacenada respecto al inicio del ensayo.

### Experimento rápido

1. Selecciona **Ventilador averiado**. Pulsa **Reiniciar** para partir de la temperatura ambiente y luego **Ejecutar**.
2. Usa velocidad 5×. Antes del apagado, sube el ventilador al 100 % y observa el cambio de pendiente. El botón **Paso +0,05 s** pausa el ensayo y avanza un paso de Euler.
3. Pasa el puntero sobre la gráfica para leer una muestra. Pulsa **Exportar CSV** para guardar el historial.
4. Repite el escenario con ventilador al 0 % para observar la reducción de potencia a 95 °C y el apagado a 105 °C. Tras el apagado, **Reiniciar** devuelve el sistema al estado inicial.

### Modelo

- La CPU genera potencia térmica `P = 10 + 0,9 × carga` en vatios. Cede `Q = G × (Tcpu − Tdis)` al disipador.
- El disipador cede `S = H × (Tdis − Tamb)` al aire. El coeficiente `H = 0,4 + 0,026 × ventilador` está en W/°C.
- Las pendientes son `(P − Q)/Ccpu` y `(Q − S)/Cdis`. Euler actualiza cada temperatura sumando su pendiente multiplicada por 0,05 s.
- Con carga y ventilación constantes y sin protección, el estado estacionario cumple `P = Q = S`. La interfaz muestra esa referencia para los ajustes actuales.
- La energía generada y la transferida al aire se acumulan por separado. Su diferencia es la energía almacenada en la CPU y el disipador respecto al inicio.

### Código y pruebas

`main.py` abre la interfaz. `config.py` define la paleta y los escenarios. `modelo/` contiene las ecuaciones, `IU/` la interfaz y `datos/` el historial.

Desde esta carpeta ejecuta `python -B tests/test_modelo.py`.


### Crédito del logotipo

[Logo UNI (1).png](https://commons.wikimedia.org/wiki/File:Logo_UNI_(1).png),
Flaviomondragon, [CC BY-SA 3.0](https://creativecommons.org/licenses/by-sa/3.0/).
El archivo se incluye tal como se descargó y se muestra a tamaño reducido.
