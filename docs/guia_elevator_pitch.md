# Guía del Elevator Pitch — Dataset de Ondas P, Red CW

Guía de trabajo, no resultados inventados. Cada frase debe poder
sostenerse con un archivo de este repositorio o con una métrica real
cuando el modelo esté entrenado y evaluado. Si un número no existe
todavía, se dice "pendiente", no se estima.

## Estructura (60-90 segundos)

1. **Problema (15 s):** distinguir, en registros de la red cubana,
   una ventana con onda P de un sismo de una ventana de ruido.
2. **Datos (20 s):** red CW, estación principal MARV y las 3 cercanas
   verificadas con datos (CHIV 53.2 km, NMDO 114.4 km, QMBU 116.3 km), 3 canales
   HHZ/HHN/HHE a 100 Hz. La etiqueta no sale de la descarga: viene
   del catálogo y de la llegada P (ver `clasificacion_ruido_sismo.py`).
3. **Método (20 s):** descarga FDSN, ventanas etiquetadas, división
   por evento (no por ventana suelta, para no filtrar el mismo sismo
   en entrenamiento y prueba), entrenamiento y evaluación.
4. **Resultado y siguiente paso (15-20 s):** métricas reales cuando
   existan (exactitud, precisión, recall, F1 y matriz de confusión) y
   qué se haría después para mejorarlo.

## Evaluación: reglas que hay que cumplir antes de presentar números

- Dividir por evento, no mezclar ventanas del mismo evento en
  entrenamiento y prueba.
- Reportar la matriz de confusión, no solo la exactitud: un modelo
  puede acertar mucho y fallar justo en los sismos.
- Comparar contra una línea base simple antes de afirmar que un
  modelo complejo "funciona".
- Guardar qué ventanas, qué catálogo y qué llegada P respaldan cada
  etiqueta, para poder responder "¿por qué esta ventana es sismo?".

## Preguntas probables en la revisión (y dónde está la respuesta)

- "¿Cómo clasificas ruido o sismo?" → `clasificacion_ruido_sismo.py`.
- "¿Por qué esas 3 estaciones son las cercanas?" →
  `estaciones_cercanas.py` y el mapa en `docs/mapa_estaciones_cercanas.svg`.
- "¿Dónde metes la mano y por qué?" → en el criterio de etiquetado,
  en la división por evento y en los umbrales; cada cambio debe
  quedar registrado con su motivo, no solo con su resultado.
