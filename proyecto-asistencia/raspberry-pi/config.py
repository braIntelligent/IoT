# config.py - Configuración Raspberry Pi

# Configuración del Servidor
SERVER_HOST = "192.168.1.100"  # Cambiar por IP del servidor
SERVER_PORT = 8000
SERVER_URL = f"http://{SERVER_HOST}:{SERVER_PORT}"

# Identificación del dispositivo
DEVICE_ID = "pi-aula-101"  # Identificador único de esta Pi

# Configuración de captura
FRAME_WIDTH = 640
FRAME_HEIGHT = 480
CAPTURE_INTERVAL = 0.5  # Segundos entre capturas
JPEG_QUALITY = 70  # Calidad de compresión (0-100)

# Configuración GPIO
LED_GREEN_PIN = 17  # GPIO para LED verde
LED_RED_PIN = 27    # GPIO para LED rojo
LED_DURATION = 2    # Segundos que permanece encendido el LED

# Puerto para API de control local
GPIO_API_PORT = 5000

# Timeout de conexión
REQUEST_TIMEOUT = 5  # Segundos