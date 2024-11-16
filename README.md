# Sistema de optimización biomecánica de la bicicleta mediante análisis por cámaras para su adaptación al ciclista profesional de ruta
Codigo base para la implementacion de un Sistema de optimización biomecánica de la bicicleta mediante análisis por cámaras para su adaptación al ciclista profesional de ruta.
Este proyecto implementa un sistema basado en visión artificial para analizar el movimiento del ciclista en los planos sagital y posterior.

## Requisitos de Instalación

Antes de ejecutar el código, asegúrese de tener instaladas las siguientes librerías:

- `cv2` (OpenCV)
- `numpy`
- `pandas`

Puede instalarlas utilizando pip:
pip install opencv-python numpy pandas

Preparación
1. Organización de Archivos: Guarde todos los archivos del proyecto en una misma carpeta. Esto es esencial para que el sistema funcione correctamente.
2. Ejecutar el Sistema: Ejecute el código a través de Main.py
3. Configuración de Cámaras:
    - Por defecto, el sistema utiliza una sola cámara para el análisis.
    - Si desea utilizar dos cámaras (una para cada plano), modifique la fuente de video en BackPartAnalysis.py. Cambie video_source de 0 a 1

Interacción con el Sistema
1. Para avanzar entre los pasos del sistema, presione la tecla Enter.
2. Durante la calibración inicial, coloque el objeto marcador dentro del recuadro visible y presione Enter tres veces para completar la calibración.
3. El sistema comenzará automáticamente solo si detecta la cantidad requerida de marcas en el entorno y si se cumplen las condiciones lógicas para el análisis.

Consideraciones Finales
Este sistema ha sido diseñado para trabajar en entornos controlados. Asegúrese de que la cámara esté correctamente posicionada para capturar los planos sagital y posterior según los requisitos del análisis.
