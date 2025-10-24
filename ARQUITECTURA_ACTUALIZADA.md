# Sistema IoT de Asistencia - Arquitectura Cliente-Servidor Optimizada

## 📋 Cambios Principales

### Arquitectura Anterior vs Nueva

**ANTES:**
- Pi: Captura video + Reconocimiento facial + Control LED + POST a API
- Servidor: Solo recibe registros y sirve datos

**AHORA:**
- **Pi (Edge):** Solo captura frames y los envía por WiFi al servidor
- **Servidor (Procesamiento):** Recibe frames, ejecuta reconocimiento facial, controla LEDs remotamente, registra en MySQL
- **Cliente Web:** Consume la API REST para mostrar asistencia

---

## 🏗️ Arquitectura del Sistema

```
┌─────────────────┐         WiFi          ┌──────────────────────┐
│  RASPBERRY PI   │◄─────────────────────►│      SERVIDOR        │
│                 │    (Frames JPEG)      │   (Procesamiento)    │
│ - Captura video │                       │ - Face Recognition   │
│ - Envía frames  │◄──────────────────────│ - Control LED remoto │
│ - Control LED   │   (Comandos GPIO)     │ - MySQL INSERT       │
└─────────────────┘                       └──────────────────────┘
                                                     │
                                                     │ HTTP
                                                     ▼
                                          ┌──────────────────────┐
                                          │    CLIENTE WEB       │
                                          │ - Lista estudiantes  │
                                          │ - Asistencia hoy     │
                                          └──────────────────────┘
```

---

## 🔧 Stack Tecnológico

### Raspberry Pi (Cliente Edge)
- **OS:** Raspberry Pi OS Lite
- **Lenguaje:** Python 3
- **Librerías:**
  - `picamera2` (captura optimizada)
  - `flask` (API ligera para recibir comandos GPIO)
  - `RPi.GPIO` (control de LEDs)
  - `requests` (envío de frames)

### Servidor (Procesamiento Central)
- **Lenguaje:** Python 3
- **Framework:** FastAPI
- **Librerías:**
  - `opencv-python`
  - `face-recognition`
  - `mysql-connector-python`
  - `uvicorn`
  - `pillow`
- **Base de Datos:** MySQL 8.0+

### Cliente Web
- HTML5 + CSS3 + JavaScript (Vanilla)
- Fetch API para consumir endpoints REST

---

## 📊 Esquema de Base de Datos (MySQL)

```sql
-- Base de datos
CREATE DATABASE IF NOT EXISTS asistencia_db 
CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;

USE asistencia_db;

-- Tabla de estudiantes
CREATE TABLE estudiantes (
    id_estudiante INT AUTO_INCREMENT PRIMARY KEY,
    nombre_completo VARCHAR(100) NOT NULL,
    rut VARCHAR(12) UNIQUE,
    path_foto_referencia VARCHAR(255) NOT NULL,
    fecha_creacion TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    INDEX idx_nombre (nombre_completo)
) ENGINE=InnoDB;

-- Tabla de asistencia
CREATE TABLE asistencia (
    id_asistencia INT AUTO_INCREMENT PRIMARY KEY,
    id_estudiante INT NOT NULL,
    hora_ingreso TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    fecha_registro DATE NOT NULL,
    dispositivo_id VARCHAR(50),
    FOREIGN KEY (id_estudiante) REFERENCES estudiantes(id_estudiante) 
        ON DELETE CASCADE,
    UNIQUE KEY uq_estudiante_fecha (id_estudiante, fecha_registro),
    INDEX idx_fecha (fecha_registro)
) ENGINE=InnoDB;

-- Tabla de configuración de dispositivos
CREATE TABLE dispositivos (
    id_dispositivo INT AUTO_INCREMENT PRIMARY KEY,
    nombre VARCHAR(50) NOT NULL,
    ip_address VARCHAR(15),
    ultimo_ping TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    activo BOOLEAN DEFAULT TRUE
) ENGINE=InnoDB;
```

---

## 🚀 Flujo de Datos

### 1. Captura y Transmisión (Pi → Servidor)
```
1. Pi captura frame cada 500ms
2. Comprime frame a JPEG (calidad 70%)
3. POST a http://SERVIDOR:8000/api/procesar-frame
   Headers: {'X-Device-ID': 'pi-aula-101'}
   Body: {image: base64_jpeg}
4. Espera respuesta del servidor
```

### 2. Procesamiento (Servidor)
```
1. Recibe frame en base64
2. Decodifica a imagen numpy
3. Detecta rostros (face_recognition.face_locations)
4. Genera encodings (face_recognition.face_encodings)
5. Compara con base de datos de rostros conocidos
6. Si hay match:
   - INSERT en tabla asistencia (ON DUPLICATE KEY UPDATE)
   - Envía comando a Pi para LED verde
   - Retorna: {status: "recognized", nombre: "Juan Pérez"}
7. Si no hay match:
   - Envía comando a Pi para LED rojo
   - Retorna: {status: "unknown"}
```

### 3. Control de LEDs (Servidor → Pi)
```
1. Servidor hace POST a http://PI_IP:5000/api/led
   Body: {color: "green"/"red", duration: 2}
2. Pi enciende LED correspondiente
3. Pi responde con {status: "ok"}
```

### 4. Consulta Web (Cliente → Servidor)
```
1. GET /api/estudiantes → Lista completa
2. GET /api/asistencia/hoy → Registros del día
3. JavaScript combina datos y renderiza tabla
```

---

## 📁 Estructura de Archivos

```
proyecto-asistencia/
│
├── raspberry-pi/                  # Código para la Pi
│   ├── captura_cliente.py         # Script principal de captura
│   ├── control_gpio_api.py        # API Flask para control LED
│   ├── config.py                  # Configuración (IP servidor, etc)
│   └── requirements.txt
│
├── servidor/                      # Código del servidor
│   ├── main.py                    # API FastAPI principal
│   ├── database.py                # Conexión MySQL
│   ├── models.py                  # Modelos de datos
│   ├── face_processor.py          # Lógica de reconocimiento facial
│   ├── fotos_conocidas/           # Fotos de referencia
│   │   ├── encodings.pkl          # Encodings pre-calculados
│   │   └── *.jpg                  # Fotos individuales
│   ├── config.py
│   └── requirements.txt
│
└── cliente-web/                   # Frontend
    ├── index.html
    ├── css/
    │   └── styles.css
    └── js/
        └── app.js
```

---

## ⚙️ Configuración Paso a Paso

### PASO 1: Configurar MySQL

```bash
# Instalar MySQL
sudo apt install mysql-server

# Configurar usuario
sudo mysql
CREATE USER 'asistencia_user'@'%' IDENTIFIED BY 'password_seguro';
GRANT ALL PRIVILEGES ON asistencia_db.* TO 'asistencia_user'@'%';
FLUSH PRIVILEGES;

# Crear esquema
mysql -u asistencia_user -p < schema.sql
```

### PASO 2: Preparar Servidor

```bash
cd servidor/
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt

# Poblar fotos conocidas
mkdir -p fotos_conocidas
# Copiar fotos de estudiantes: juan_perez_12345678.jpg

# Generar encodings
python generate_encodings.py

# Iniciar servidor
uvicorn main:app --host 0.0.0.0 --port 8000
```

### PASO 3: Configurar Raspberry Pi

```bash
cd raspberry-pi/

# Instalar dependencias
pip3 install -r requirements.txt

# Editar config.py con IP del servidor
nano config.py

# Iniciar API de control GPIO (en segundo plano)
python3 control_gpio_api.py &

# Iniciar captura
python3 captura_cliente.py
```

### PASO 4: Desplegar Cliente Web

```bash
# Opción 1: Servidor web simple
cd cliente-web/
python3 -m http.server 8080

# Opción 2: Nginx (producción)
sudo cp -r cliente-web/* /var/www/html/asistencia/
```

---

## 🔒 Mejoras de Seguridad

1. **API Key:** Agregar header `X-API-Key` en todas las peticiones
2. **HTTPS:** Usar certificados SSL/TLS (Let's Encrypt)
3. **Rate Limiting:** Limitar peticiones por dispositivo
4. **Validación:** Validar formato de frames antes de procesar
5. **Logging:** Registrar todos los accesos y errores

---

## 📈 Optimizaciones de Rendimiento

### En la Raspberry Pi:
- Capturar a 640x480 (no full HD)
- Comprimir JPEG a calidad 70%
- Enviar solo si hay cambios significativos (diferencia de frames)

### En el Servidor:
- Cache de encodings en memoria (Redis opcional)
- Pool de conexiones MySQL
- Procesamiento asíncrono con `asyncio`
- Redimensionar frames a 480x360 antes de procesar

### En la Red:
- Usar protocolo HTTP/2
- Comprimir respuestas con gzip
- WebSocket para actualizaciones en tiempo real (opcional)

---

## 🧪 Testing

```bash
# Test 1: Verificar captura de Pi
curl -X GET http://PI_IP:5000/api/status

# Test 2: Enviar frame de prueba al servidor
curl -X POST http://SERVIDOR:8000/api/procesar-frame \
  -H "Content-Type: application/json" \
  -d '{"image": "base64_string", "device_id": "test"}'

# Test 3: Consultar API
curl http://SERVIDOR:8000/api/estudiantes
curl http://SERVIDOR:8000/api/asistencia/hoy
```

---

## 📊 Monitoreo

- **Pi:** Logs en `/var/log/asistencia_pi.log`
- **Servidor:** Logs en `/var/log/asistencia_server.log`
- **Métricas:** CPU, RAM, latencia de red, tasa de reconocimiento

---

## 🎯 Ventajas de esta Arquitectura

1. **Escalabilidad:** Un servidor puede manejar múltiples Pis
2. **Rendimiento:** Pi no se sobrecarga con procesamiento pesado
3. **Mantenimiento:** Actualizar algoritmo solo requiere modificar servidor
4. **Centralización:** Todos los encodings y lógica en un solo lugar
5. **Flexibilidad:** Fácil agregar nuevas aulas o funcionalidades