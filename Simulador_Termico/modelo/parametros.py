"""Constantes físicas del modelo (valores didácticos, no de un equipo real)."""
from dataclasses import dataclass


@dataclass(frozen=True)
class Parametros:
    c_cpu: float = 12.0            
    c_disipador: float = 60.0      
    g_conduccion: float = 4.0      
    h_natural: float = 0.4         
    h_forzada: float = 0.026      
    p_reposo: float = 10.0         
    p_carga: float = 0.9          
    t_max: float = 95.0            
    t_histeresis: float = 5.0     
    factor_throttling: float = 0.5 
    t_apagado: float = 105.0       

    def potencia(self, carga: float) -> float:
        """P(carga) en W, sin protección térmica."""
        return self.p_reposo + self.p_carga * carga

    def h(self, ventilador: float) -> float:
        """Coeficiente global de intercambio con el aire H(ventilador) en W/°C."""
        return self.h_natural + self.h_forzada * ventilador
