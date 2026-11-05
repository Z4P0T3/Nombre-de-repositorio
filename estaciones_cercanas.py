"""
Estaciones cercanas a MARV: cálculo reproducible.

Fuente de coordenadas: servicio FDSN de EarthScope, red CW,
consulta de estaciones y canales para 2023-10-15 00:00-02:00 UTC.
Si tienes ObsPy instalado, puedes re-verificar las coordenadas con
client.get_stations(network="CW", level="station"); la tabla de abajo
es la copia verificada de esa consulta, para que el cálculo funcione
también sin conexión.

Criterio (todas las condiciones, en este orden):
  1. Red CW.
  2. Canales HHZ, HHN y HHE activos en la ventana de trabajo.
  3. La estación entrega ondas reales en EarthScope (dataselect).
     Sin datos, no entra, aunque esté cerca y tenga HH.
  4. Distancia haversine desde MARV, de menor a mayor; se toman las 3
     primeras que cumplen 1-3.

Por qué ya no es RCC: RCC era la principal (19.995001, -75.696503),
pero no entrega ondas en EarthScope: en la corrida del cuaderno
fallaron sus 122 descargas por evento, y al probarla en 2016, 2018,
2019, 2020, 2021, 2023, 2024 y 2025 siempre respondió sin datos
(HTTP 204), también en su canal HN. HLG y LMGC tampoco entregan
ondas en las pruebas (204 en el evento 2022-05-09 y en la muestra
2023-10-15), por eso quedan fuera aunque estén más cerca que NMDO
y QMBU. Con este criterio, las 3 cercanas a MARV son CHIV, NMDO
y QMBU. La lista anterior (MOAC, TGU, CEN) tampoco cumplía el
criterio: MOAC está a 107.4 km de RCC y en esa ventana solo tiene
canales EH y HN, no HH; TGU y CEN no aparecen como códigos CW.

Uso:
    python estaciones_cercanas.py
Escribe data/estaciones_cercanas_MARV.csv con el ranking completo.
"""

import math
from pathlib import Path
import pandas as pd

# (código, latitud, longitud, lugar) - estaciones HH activas 2023-10-15.
MARV = ("MARV", 20.005285, -75.906555, "Mar Verde, Santiago de Cuba")
ESTACIONES_HH = [
    ("RCC", 19.995001, -75.696503, "Río Carpintero, Santiago de Cuba"),
    ("CHIV", 19.97648, -76.415131, "Chivirico, Guamá, Santiago de Cuba"),
    ("QMBU", 20.19887, -74.811867, "Quimbuelo, San Antonio del Sur, Guantánamo"),
    ("NMDO", 20.559826, -74.982674, "Presa Nuevo Mundo, Moa, Holguín"),
    ("HLG", 20.920046, -76.236176, "El Paraíso, Holguín"),
    ("GNEO", 20.3274, -74.592934, "Los Guineos, Baracoa, Guantánamo"),
    ("LMGC", 20.0646, -77.004501, "Las Mercedes, Granma"),
    ("MASC", 20.175501, -74.231201, "Maisí, Guantánamo"),
    ("PILO", 19.91395, -77.408806, "El Mamey, Pilón, Granma"),
    ("CCCC", 21.193399, -77.417297, "Cascorro, Camagüey"),
]

# Datos reales en EarthScope (dataselect), verificado 2026-11-05:
# True = devuelve ondas (HTTP 200), False = sin datos (HTTP 204).
DATOS_EARTHSCOPE = {
    "RCC": False,   # sin datos en 2016-2025, también en HN
    "CHIV": True,   # por evento sí, muestra inicial 2023-10-15 no
    "NMDO": True,
    "QMBU": True,
    "HLG": False,
    "LMGC": False,
    # GNEO, MASC, PILO, CCCC: no se comprobó su dataselect; no entran
    # en las 3 primeras por distancia, así que no afectan al resultado.
}


def haversine_km(lat1, lon1, lat2, lon2):
    """Distancia de gran círculo entre dos puntos (lat/lon en grados)."""
    radio = 6371.0
    p1, p2 = math.radians(lat1), math.radians(lat2)
    dphi = math.radians(lat2 - lat1)
    dlambda = math.radians(lon2 - lon1)
    a = math.sin(dphi / 2) ** 2 + math.cos(p1) * math.cos(p2) * math.sin(dlambda / 2) ** 2
    return 2 * radio * math.asin(math.sqrt(a))


def ranking_cercanas(n=3):
    """Devuelve el ranking completo y las n estaciones más cercanas con datos."""
    filas = []
    for codigo, lat, lon, lugar in ESTACIONES_HH:
        filas.append(
            {
                "estacion": codigo,
                "latitud": lat,
                "longitud": lon,
                "lugar": lugar,
                "distancia_km_desde_MARV": round(
                    haversine_km(MARV[1], MARV[2], lat, lon), 1
                ),
                "con_datos_earthscope": DATOS_EARTHSCOPE.get(codigo, "sin comprobar"),
            }
        )
    df = pd.DataFrame(filas).sort_values("distancia_km_desde_MARV").reset_index(drop=True)
    df["posicion"] = df.index + 1
    con_datos = df[df["con_datos_earthscope"] == True].head(n)
    return df, con_datos


if __name__ == "__main__":
    ranking, cercanas = ranking_cercanas(3)
    print("Estación principal: MARV (Mar Verde)")
    print(ranking.to_string(index=False))
    print("\n3 más cercanas con HH activas y con datos:")
    print(cercanas[["estacion", "distancia_km_desde_MARV"]].to_string(index=False))
    salida = Path("data/estaciones_cercanas_MARV.csv")
    salida.parent.mkdir(parents=True, exist_ok=True)
    ranking.to_csv(salida, index=False)
    print(f"\nRanking guardado en {salida}")
