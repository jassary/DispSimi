"""Punto de entrada del simulador térmico.

Ejecutar desde cualquier carpeta:   python main.py
(Windows: py main.py · Linux: si falta tkinter, instale python3-tk)
"""
import os
import sys
import tkinter as tk

# Permite ejecutar main.py desde cualquier carpeta: los imports
# (config, modelo, datos, IU) se resuelven respecto a este archivo.
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from IU.app import AplicacionSimulador  # noqa: E402


def main() -> None:
    root = tk.Tk()
    AplicacionSimulador(root).pack(fill='both', expand=True)
    root.mainloop()


if __name__ == '__main__':
    main()
