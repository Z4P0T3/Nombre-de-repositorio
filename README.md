Dataset de Ondas P — Red Sísmica Cubana (CW)
Herramientas y scripts para la descarga, procesamiento y estructuración de registros de ondas P utilizando datos de estaciones sismológicas de la red cubana (CW) a través de FDSN y SeisBench.
📁 Estructura del Proyecto
dataset-ondas-p-cw/
├── config/             # Archivos de configuración (JSON)
├── data/               # Datos brutos y procesados (fases, trazas)
├── docs/               # Documentación y notas técnicas
├── notebooks/          # Notebooks de Jupyter / Google Colab
├── resultados/         # Gráficas, métricas y salidas de modelos
├── src/                # Código fuente principal (scripts de Python)
├── tests/              # Pruebas unitarias y de integración
├── INFORME_FINAL.md    # Reporte y conclusiones del proyecto
├── README.md           # Este archivo
└── requirements.txt    # Dependencias del proyecto

⚙️ Configuración (config/configuracion.json)
El proyecto utiliza un archivo de configuración centralizado para definir los parámetros de extracción y procesamiento:
 * Estación principal: RCC (Río Carpintero, Santiago de Cuba)
 * Estaciones prioritarias: ['RCC', 'QMBU', 'MARV', 'LMGC', 'CHIV', 'GTMO']
 * Frecuencia de muestreo: Estandarizada a 100 Hz
 * Límites de ventana temporal: Configurables por corrida (por defecto para pruebas en rangos específicos de alta sismicidad).
🚀 Instalación y Uso
 * Clonar el repositorio:
   git clone https://github.com/tu-usuario/dataset-ondas-p-cw.git
cd dataset-ondas-p-cw

 * Instalar las dependencias:
   Se recomienda utilizar un entorno virtual de Python (versión 3.10 o superior).
   pip install -r requirements.txt

 * Ejecución en Google Colab / Local:
   Puedes abrir y ejecutar el flujo completo de extracción en el notebook ubicado en notebooks/dataset_eqt_colab.ipynb, el cual gestiona automáticamente la conexión con FDSN (EarthScope/IRIS) y el almacenamiento estructurado en Google Drive.
🛠️ Dependencias Principales
 * ObsPy (>= 1.5.0) — Procesamiento de datos sismológicos y manejo de metadatos SEED/FDSN.
 * SeisBench (>= 0.12.0) — Herramientas de aprendizaje automático para sismología.
 * Pandas / NumPy — Manipulación y análisis de datos tabulares y numéricos.
