"""
Clasificación ruido / sismo: criterio explícito, separado de la descarga.

Problema que corrige: descarga_sismologia.py extrae los 3 canales,
pero eso no clasifica nada. La etiqueta NO sale de la forma de onda
sola y NO se deduce de la amplitud.

Criterio (la etiqueta viene del dataset, es decir, del catálogo y de
la llegada P, no del script de descarga):

  * "sismo": la ventana contiene la llegada de la onda P de un evento
    registrado en el catálogo para esa estación. En la práctica: hay
    un evento en el catálogo y su tiempo de llegada P (observado, o
    calculado a partir del tiempo origen y la distancia epicentral)
    cae dentro de la ventana.
  * "ruido": la ventana NO contiene ninguna llegada P y, además, no
    hay ningún evento del catálogo dentro de una zona de seguridad
    alrededor de la ventana (por defecto, 60 minutos antes y después),
    para no etiquetar como ruido la coda de un sismo ni su preámbulo.
    Las ventanas de ruido deben tomarse, en lo posible, en la misma
    estación y con los mismos canales que las de sismo, para que el
    modelo no aprenda a distinguir estaciones en vez de fenómenos.
  * "sin_etiqueta": no hay catálogo ni llegada P que respalde ninguna
    de las dos etiquetas. No se inventa una etiqueta: esa ventana no
    entra al entrenamiento hasta tener evidencia.

Qué hay que entregar junto a cada etiqueta para que sea revisable:
  - identificador del evento del catálogo (o "ninguno"),
  - tiempo origen, magnitud y distancia epicentral si es sismo,
  - tiempo de llegada P usado,
  - inicio y fin de la ventana y estación/canal.

Esta función es el contrato de etiquetado. El catálogo concreto
(CENAIN / FDSN event service u otro) se pasa como lista de eventos;
este archivo no inventa eventos para el 2023-10-15.
"""

from dataclasses import dataclass
from datetime import datetime, timedelta
from typing import Optional


@dataclass
class EventoCatalogo:
    """Un evento del catálogo, con su llegada P en la estación."""

    id_evento: str
    tiempo_origen: datetime
    llegada_p: datetime
    magnitud: Optional[float] = None
    distancia_km: Optional[float] = None


def clasificar_ventana(
    inicio_ventana: datetime,
    fin_ventana: datetime,
    eventos: list,
    zona_seguridad_min: int = 60,
) -> str:
    """
    Devuelve "sismo", "ruido" o "sin_etiqueta".

    - sismo: alguna llegada P cae dentro de [inicio, fin].
    - ruido: ningún evento cae dentro de la ventana ampliada con la
      zona de seguridad, Y la lista de eventos no está vacía (es decir,
      sí se consultó un catálogo; una lista vacía no prueba nada).
    - sin_etiqueta: no se consultó catálogo (eventos vacíos) o no hay
      evidencia suficiente.
    """
    if inicio_ventana >= fin_ventana:
        raise ValueError("La ventana debe tener inicio anterior al fin.")

    for ev in eventos:
        if inicio_ventana <= ev.llegada_p <= fin_ventana:
            return "sismo"

    if not eventos:
        # Sin catálogo no se puede afirmar que sea ruido.
        return "sin_etiqueta"

    ampliado_inicio = inicio_ventana - timedelta(minutes=zona_seguridad_min)
    ampliado_fin = fin_ventana + timedelta(minutes=zona_seguridad_min)
    for ev in eventos:
        if ampliado_inicio <= ev.tiempo_origen <= ampliado_fin:
            # Demasiado cerca de un evento: no es ruido seguro.
            return "sin_etiqueta"

    return "ruido"


if __name__ == "__main__":
    # Ejemplo mínimo, solo para mostrar el contrato (no son datos reales
    # del dataset: el catálogo real debe sustituir esta lista).
    evento = EventoCatalogo(
        id_evento="ejemplo",
        tiempo_origen=datetime(2023, 10, 15, 1, 0, 0),
        llegada_p=datetime(2023, 10, 15, 1, 0, 30),
    )
    print(clasificar_ventana(
        datetime(2023, 10, 15, 0, 59, 0),
        datetime(2023, 10, 15, 1, 2, 0),
        [evento],
    ))  # -> sismo
    print(clasificar_ventana(
        datetime(2023, 10, 15, 3, 0, 0),
        datetime(2023, 10, 15, 3, 2, 0),
        [evento],
    ))  # -> ruido
    print(clasificar_ventana(
        datetime(2023, 10, 15, 3, 0, 0),
        datetime(2023, 10, 15, 3, 2, 0),
        [],
    ))  # -> sin_etiqueta
