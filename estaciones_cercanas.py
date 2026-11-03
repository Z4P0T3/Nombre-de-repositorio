"""
Estaciones cercanas a RCC: cálculo reproducible.

Fuente de coordenadas: servicio FDSN de IRIS/EarthScope, red CW,
consulta de estaciones y canales para 2023-10-15 00:00-02:00 UTC.
Si tienes ObsPy instalado, puedes re-verificar las coordenadas con
client.get_stations(network="CW", level="station"); la tabla de abajo
es la copia verificada de esa consulta, para que el cálculo funcione
también sin conexión.

Criterio (todas las condiciones, en este orden):
  1. Red CW.
  2. Canales HHZ, HHN y HHE activos en la ventana de trabajo.
  3. Distancia haversine desde RCC, de menor a mayor; se toman las 3
     primeras.

Por qué no vale solo "la IA me dijo cuáles son": la distancia se
calcula, no se afirma. Con este criterio, MOAC queda fuera: está a
107.4 km y en esa ventana no tiene HH (tiene EH y HN). TGU y CEN no
aparecen como códigos CW en esa consulta FDSN.

Uso:
    python estaciones_cercanas.py
Escribe data/estaciones_cercanas_RCC.csv con el ranking completo.
"""

import math
from pathlib import Path
import pandas as pd

# (código, latitud, longitud, lugar) - estaciones HH activas 2023-10-15.
RCC = ("RCC", 19.995001, -75.696503, "Río Carpintero, Santiago de Cuba")
ESTACIONES_HH = [
    ("MARV", 20.005285, -75.906555, "Mar Verde, Santiago de Cuba"),
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


def haversine_km(lat1, lon1, lat2, lon2):
    """Distancia de gran círculo entre dos puntos (lat/lon en grados)."""
    radio = 6371.0
    p1, p2 = math.radians(lat1), math.radians(lat2)
    dphi = math.radians(lat2 - lat1)
    dlambda = math.radians(lon2 - lon1)
    a = math.sin(dphi / 2) ** 2 + math.cos(p1) * math.cos(p2) * math.sin(dlambda / 2) ** 2
    return 2 * radio * math.asin(math.sqrt(a))


def ranking_cercanas(n=3):
    """Devuelve el ranking completo y las n estaciones más cercanas."""
    filas = []
    for codigo, lat, lon, lugar in ESTACIONES_HH:
        filas.append(
            {
                "estacion": codigo,
                "latitud": lat,
                "longitud": lon,
                "lugar": lugar,
                "distancia_km_desde_RCC": round(
                    haversine_km(RCC[1], RCC[2], lat, lon), 1
                ),
            }
        )
    df = pd.DataFrame(filas).sort_values("distancia_km_desde_RCC").reset_index(drop=True)
    df["posicion"] = df.index + 1
    return df, df.head(n)


if __name__ == "__main__":
    ranking, cercanas = ranking_cercanas(3)
    print("Estación principal: RCC (Río Carpintero)")
    print(ranking.to_string(index=False))
    print("\n3 más cercanas con HH activas:")
    print(cercanas[["estacion", "distancia_km_desde_RCC"]].to_string(index=False))
    salida = Path("data/estaciones_cercanas_RCC.csv")
    salida.parent.mkdir(parents=True, exist_ok=True)
    ranking.to_csv(salida, index=False)
    print(f"\nRanking guardado en {salida}")
