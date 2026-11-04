# Permite que pytest encuentre los paquetes modelo/, datos/, IU/ y config.py
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
