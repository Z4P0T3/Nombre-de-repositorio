"""
Script de descarga y procesamiento para la red sísmica CW.
Estación principal: RCC
Estaciones cercanas de soporte: MOAC, TGU, CEN
Propósito: Descarga FDSN y estructuración de datos para diferenciación de sismos y ruido.
"""

from obspy import UTCDateTime
from obspy.clients.fdsn import Client
from pathlib import Path
import pandas as pd

def ejecutar_pipeline_sismologia():
    # Configuración de cliente FDSN y directorios de salida
    client = Client("EARTHSCOPE", timeout=60)
    dir_salida = Path("data/raw")
    dir_salida.mkdir(parents=True, exist_ok=True)
    
    red = "CW"
    estacion_principal = "RCC"
    estaciones_cercanas = ["MOAC", "TGU", "CEN"]
    todas_estaciones = [estacion_principal] + estaciones_cercanas
    
    # Canales sísmicos de banda ancha
    canales = "HHZ,HHN,HHE"
    
    # Intervalo de análisis definido para el taller
    inicio = UTCDateTime("2023-10-15T00:00:00")
    fin = UTCDateTime("2023-10-15T02:00:00")
    
    print(f"Iniciando descarga multiestación para la red {red}...")
    
    registros_log = []
    
    for est in todas_estaciones:
        print(f"Descargando estación: {red}.{est}...")
        try:
            st = client.get_waveforms(
                network=red,
                station=est,
                location="*",
                channel=canales,
                starttime=inicio,
                endtime=fin
            )
            
            # Guardar en formato MiniSEED
            nombre_archivo = dir_salida / f"{red}.{est}.mseed"
            st.write(str(nombre_archivo), format="MSEED")
            print(f"  -> Guardado exitoso: {nombre_archivo.name}")
            
            registros_log.append({
                "estacion": est,
                "estado": "Exitoso",
                "archivo": str(nombre_archivo)
            })
        except Exception as e:
            print(f"  -> Error al descargar {est}: {e}")
            registros_log.append({
                "estacion": est,
                "estado": f"Error: {str(e)}",
                "archivo": None
            })
            
    # Registro de metadatos para la separación posterior de sismos vs ruido ambiental
    df_log = pd.DataFrame(registros_log)
    df_log.to_csv("data/resumen_estaciones.csv", index=False)
    print("\nProceso finalizado. Resumen de estaciones guardado en CSV.")

if __name__ == "__main__":
    ejecutar_pipeline_sismologia()
