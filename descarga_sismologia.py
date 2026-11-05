"""
Descarga y procesamiento para la red sísmica CW.

Estación principal: MARV (Mar Verde, Santiago de Cuba).

IMPORTANTE - Qué hace y qué NO hace este script:
- SÍ descarga formas de onda de 3 componentes (HHZ, HHN, HHE) y las
  guarda en MiniSEED, con un resumen en CSV.
- NO clasifica si una ventana es ruido o sismo. La descarga, por sí sola,
  no puede clasificar: una amplitud alta no es prueba de sismo y una
  amplitud baja no es prueba de ruido. La etiqueta se asigna después,
  en un paso separado, con el criterio documentado en
  clasificacion_ruido_sismo.py (ventana con llegada P de un evento del
  catálogo = sismo; ventana sin evento cercano en el catálogo = ruido;
  sin evidencia de catálogo ni de llegada P = sin_etiqueta).

Catálogo (actualización 2026-11-05): la etiqueta usa el catálogo
NEIC/USGS por FDSN, no el servicio de eventos de EarthScope,
retirado el 1 de junio de 2026. Las formas de onda de este
script siguen descargándose de EarthScope, red CW.

Estaciones cercanas - criterio verificado (no copiado sin revisar):
Una estación cuenta como "cercana" solo si cumple TODAS estas
condiciones para la ventana de trabajo (aquí, 2023-10-15):
  1. Pertenece a la red CW en el servicio FDSN de IRIS/EarthScope.
  2. Tiene los 3 canales de banda ancha HHZ, HHN y HHE activos.
  3. Se ordena por distancia haversine (gran círculo, R = 6371 km)
     desde MARV y se toman las 3 primeras.
  4. La estación debe entregar ondas reales en EarthScope
     (dataselect). Sin datos, no entra, aunque esté cerca.

Resultado verificado (2026-11-05):
  CHIV  53.2 km - Chivirico, Guamá, Santiago de Cuba
  NMDO  114.4 km - Presa Nuevo Mundo, Moa, Holguín
  QMBU  116.3 km - Quimbuelo, San Antonio del Sur, Guantánamo

Excluidas por falta de datos en EarthScope, aunque tengan HH:
RCC (22.0 km desde MARV, sin datos en 2016-2025), HLG
(107.4 km) y LMGC (114.9 km).

Corrección respecto a la versión anterior: la lista anterior
(MOAC, TGU, CEN) no cumple ese criterio en FDSN/CW para esa fecha.
MOAC está a 107.4 km de RCC y en esa ventana solo ofrece canales EH
(corto periodo) y HN, no HH; TGU y CEN no aparecen como códigos de
estación CW en la consulta FDSN para esa fecha. Por eso se sustituyen
por CHIV, NMDO y QMBU. El cálculo reproducible está en
estaciones_cercanas.py y el mapa en docs/mapa_estaciones_cercanas.svg.
"""

from obspy import UTCDateTime
from obspy.clients.fdsn import Client
from pathlib import Path
import pandas as pd


# Coordenadas verificadas en IRIS FDSN (red CW, 2023-10-15).
ESTACION_PRINCIPAL = "MARV"
ESTACIONES_CERCANAS = ["CHIV", "NMDO", "QMBU"]  # Ver criterio arriba.


def ejecutar_pipeline_sismologia():
    # Configuración de cliente FDSN y directorios de salida
    client = Client("EARTHSCOPE", timeout=60)
    dir_salida = Path("data/raw")
    dir_salida.mkdir(parents=True, exist_ok=True)

    red = "CW"
    todas_estaciones = [ESTACION_PRINCIPAL] + ESTACIONES_CERCANAS

    # Canales sísmicos de banda ancha (los 3 componentes).
    canales = "HHZ,HHN,HHE"

    # Intervalo de análisis definido para el taller.
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
                endtime=fin,
            )

            # Guardar en formato MiniSEED
            nombre_archivo = dir_salida / f"{red}.{est}.mseed"
            st.write(str(nombre_archivo), format="MSEED")
            print(f"  -> Guardado exitoso: {nombre_archivo.name}")

            registros_log.append(
                {
                    "estacion": est,
                    "estado": "Exitoso",
                    "archivo": str(nombre_archivo),
                }
            )
        except Exception as e:
            print(f"  -> Error al descargar {est}: {e}")
            registros_log.append(
                {
                    "estacion": est,
                    "estado": f"Error: {str(e)}",
                    "archivo": None,
                }
            )

    # Registro de metadatos. OJO: este CSV solo dice si la descarga
    # funcionó; NO es la etiqueta ruido/sismo. Esa etiqueta se crea
    # aparte, con clasificacion_ruido_sismo.py.
    df_log = pd.DataFrame(registros_log)
    df_log.to_csv("data/resumen_estaciones.csv", index=False)
    print("\nProceso finalizado. Resumen de estaciones guardado en CSV.")


if __name__ == "__main__":
    ejecutar_pipeline_sismologia()
