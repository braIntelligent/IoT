# config.py - Configuración del Servidor

# Configuración de Base de Datos MySQL
DB_CONFIG = {
    "host": "localhost",
    "user": "asistencia_user",
    "password": "password_seguro",  # CAMBIAR EN PRODUCCIÓN
    "database": "asistencia_db",
    "port": 3306
}

# Configuración del servidor
SERVER_HOST = "0.0.0.0"
SERVER_PORT = 8000

# Rutas de archivos
FOTOS_DIR = "fotos_conocidas"
ENCODINGS_FILE = "fotos_conocidas/encodings.pkl"

# Configuración de reconocimiento facial
FACE_TOLERANCE = 0.6  # Menor = más estricto (0.4-0.7 recomendado)
FACE_DETECTION_MODEL = "hog"  # "hog" (rápido, CPU) o "cnn" (preciso, GPU)

# Configuración de procesamiento de imágenes
FRAME_RESIZE_WIDTH = 480  # Redimensionar frame para procesamiento más rápido
MAX_FRAME_SIZE_MB = 5  # Tamaño máximo del frame en MB

# Cooldown para evitar registros duplicados
COOLDOWN_SECONDS = 300  # 5 minutos entre registros del mismo estudiante

# Configuración de LEDs remotos
LED_CONTROL_TIMEOUT = 2  # Timeout para llamadas a API de GPIO

# Logging
LOG_FILE = "/var/log/asistencia_server.log"
LOG_LEVEL = "INFO"  # DEBUG, INFO, WARNING, ERROR

# CORS (opcional para frontend en otro dominio)
CORS_ORIGINS = ["*"]  # En producción, especificar dominios exactos