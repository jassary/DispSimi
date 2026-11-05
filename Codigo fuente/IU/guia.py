"""Guía breve para el ensayo de ventilación."""
from tkinter import messagebox


def mostrar_guia(parent=None) -> None:
    texto = (
        '1. Elige «Ventilador averiado» y pulsa Reiniciar.\n'
        '2. Ejecuta a 5×. Observa las temperaturas y sus pendientes.\n'
        '3. Antes del apagado, sube el ventilador al 100 % y observa\n'
        '    cómo cambia la transferencia de calor al aire.\n'
        '4. Pausa y usa Paso +0,05 s para ver una actualización de Euler.\n'
        '5. Mueve el puntero por la gráfica para leer los datos.\n\n'
        'La CPU genera calor. El disipador lo recibe por conducción\n'
        'y lo transfiere al aire por convección. Una flecha invertida\n'
        'indica que el flujo cambió de sentido.\n\n'
        'En estado estacionario, la potencia generada y la cedida al\n'
        'aire coinciden aunque CPU, disipador y aire estén a distinta\n'
        'temperatura. La referencia se calcula sin protección térmica.'
    )
    messagebox.showinfo('Guía de laboratorio', texto, parent=parent)
