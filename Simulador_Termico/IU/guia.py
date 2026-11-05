"""Texto de apoyo para exponer en la feria."""
from tkinter import messagebox

TEXTO_GUIA = (
    '1. Reinicia (tecla R) con ambiente de 28 °C.\n'
    '2. Elige el escenario «Ventilador averiado». Usa velocidad 5×.\n'
    '3. Observa la recta tangente de la CPU: al inicio es muy empinada\n'
    '   (dT/dt grande) y se va aplanando.\n'
    '4. Sube el ventilador al 100 % SIN reiniciar.\n'
    '5. La tangente del disipador se inclina hacia abajo (dT/dt < 0)\n'
    '   y después baja la CPU.\n'
    '6. Con la protección activa, la CPU reduce su potencia a 95 °C y\n'
    '   se apaga a 105 °C si no basta, como un equipo real.\n\n'
    'Física: energía eléctrica → energía interna (1.ª ley); el calor va\n'
    'de lo caliente a lo frío (2.ª ley); conducción hacia el disipador y\n'
    'convección hacia el aire.\n\n'
    'Matemática:\n'
    '  Ccpu·dTcpu/dt = P − G·(Tcpu − Tdis)\n'
    '  Cdis·dTdis/dt = G·(Tcpu − Tdis) − H·(Tdis − Tamb)\n'
    '  Euler: T(t+Δt) ≈ T(t) + Δt·dT/dt\n'
    '  dT/dt = 0  →  equilibrio térmico\n'
    '  E = ∫ P dt  →  energía convertida en calor\n\n'
    'Valores ilustrativos. No pruebes bloqueando el ventilador real.'
)


def mostrar_guia(parent=None) -> None:
    messagebox.showinfo('Guía para la feria', TEXTO_GUIA, parent=parent)
