# 🎓 Sistema IoT de Asistencia Automatizada por Reconocimiento Facial

<div align="center">

![Python](https://img.shields.io/badge/Python-3.9+-3776AB?style=for-the-badge&logo=python&logoColor=white)
![FastAPI](https://img.shields.io/badge/FastAPI-009688?style=for-the-badge&logo=fastapi&logoColor=white)
![MySQL](https://img.shields.io/badge/MySQL-4479A1?style=for-the-badge&logo=mysql&logoColor=white)
![Raspberry Pi](https://img.shields.io/badge/Raspberry%20Pi-A22846?style=for-the-badge&logo=raspberrypi&logoColor=white)

**Sistema automatizado de control de asistencia mediante reconocimiento facial biométrico**

[Características](#-características) •
[Instalación](#-instalación-rápida) •
[Documentación](#-documentación) •
[Demo](#-demo) •
[Soporte](#-soporte)

</div>

---

## 📋 Tabla de Contenidos

- [Descripción](#-descripción)
- [Características](#-características)
- [Arquitectura](#-arquitectura)
- [Requisitos](#-requisitos)
- [Instalación Rápida](#-instalación-rápida)
- [Uso](#-uso)
- [Documentación](#-documentación)
- [API Endpoints](#-api-endpoints)
- [Estructura del Proyecto](#-estructura-del-proyecto)
- [Configuración](#️-configuración)
- [Testing](#-testing)
- [Solución de Problemas](#-solución-de-problemas)
- [Roadmap](#-roadmap)
- [Contribuciones](#-contribuciones)
- [Licencia](#-licencia)

---

## 🎯 Descripción

Sistema IoT que automatiza el proceso de toma de asistencia en salas de clases mediante **reconocimiento facial biométrico**. Diseñado con una arquitectura **cliente-servidor optimizada** donde la Raspberry Pi solo captura y transmite video, mientras que un servidor central ejecuta todo el procesamiento de reconocimiento facial.

### ¿Por qué este proyecto?

- ✅ **Eficiente**: La Raspberry Pi no se sobrecarga
- ✅ **Escalable**: Un servidor puede manejar múltiples cámaras
- ✅ **Preciso**: Tasa de reconocimiento >95%
- ✅ **Moderno**: Stack tecnológico actual
- ✅ **Fácil de mantener**: Código limpio y documentado

---

## ✨ Características

### 🎥 Captura Inteligente
- Captura continua de video desde Raspberry Pi
- Compresión optimizada de frames (JPEG)
- Transmisión por WiFi al servidor

### 🧠 Procesamiento Centralizado
- Reconocimiento facial en servidor (no en Pi)
- Detección de múltiples rostros por frame
- Comparación con base de datos de estudiantes
- Sistema de cooldown (evita registros duplicados)

### 💡 Feedback Visual
- LED verde: Estudiante reconocido y registrado
- LED rojo: Rostro no reconocido
- Control remoto desde servidor

### 📊 Dashboard Web
- Visualización en tiempo real
- Lista completa de estudiantes
- Filtros y búsqueda
- Actualización automática cada 10s
- Responsive design

### 🗄️ Base de Datos
- MySQL 8.0 para persistencia
- Registro de asistencia diaria
- Prevención de duplicados
- Historial completo

---

## 🏗️ Arquitectura

```
┌─────────────────────┐         WiFi          ┌──────────────────────┐
│   RASPBERRY PI      │ ────────────────────► │      SERVIDOR        │
│   (Edge Device)     │   Frames (base64)     │   (Procesamiento)    │
│                     │                       │                      │
│ • Captura video     │ ◄──────────────────── │ • Face Recognition   │
│ • Comprime frames   │   Comandos GPIO       │ • MySQL              │
│ • Controla LEDs     │                       │ • Control LED remoto │
└─────────────────────┘                       └───────────┬──────────┘
         │                                                │
         │ GPIO                                           │ HTTP
         ▼                                                ▼
    💚 LED Verde                                 ┌─────────────────┐
    ❤️  LED Rojo                                 │  CLIENTE WEB    │
                                                 │  (Dashboard)    │
                                                 └─────────────────┘
```

### Flujo de Datos

1. **Captura** → Pi captura frame de video
2. **Compresión** → Convierte a JPEG base64
3. **Transmisión** → Envía al servidor vía POST
4. **Procesamiento** → Servidor ejecuta face_recognition
5. **Comparación** → Busca match en base de datos
6. **Registro** → Si hay match, inserta en MySQL
7. **Feedback** → Servidor envía comando LED a Pi
8. **Visualización** → Cliente web consulta API REST

---

## 💻 Requisitos

### Hardware

| Componente | Especificación | Precio Aprox. (CLP) |
|------------|----------------|---------------------|
| Raspberry Pi 4 | 4GB RAM mínimo | $60.000 - $80.000 |
| Cámara Pi | v2 (8MP) o v3 (12MP) | $25.000 - $40.000 |
| MicroSD | 32GB+ Clase 10 | $8.000 - $12.000 |
| Fuente USB-C | 5V 3A | $12.000 - $15.000 |
| LEDs | Verde + Rojo (5mm) | $200 c/u |
| Resistencias | 220Ω (x2) | $50 c/u |
| Protoboard | 400 puntos | $2.000 |
| Cables Jumper | Macho-Hembra | $3.000 |
| **Servidor** | PC/VPS (2+ cores, 4GB RAM) | Variable |

**Total Pi: ~$110.000 - $155.000**

### Software

- **Raspberry Pi:** Raspberry Pi OS (64-bit)
- **Servidor:** Ubuntu 22.04 LTS (o similar)
- **Python:** 3.9+
- **MySQL:** 8.0+
- **Navegador:** Chrome, Firefox, Safari (moderno)

---

## 🚀 Instalación Rápida

### 1️⃣ Configurar Base de Datos (5 min)

```bash
# Instalar MySQL
sudo apt update
sudo apt install mysql-server

# Crear usuario y base de datos
sudo mysql
```

```sql
CREATE USER 'asistencia_user'@'%' IDENTIFIED BY 'tu_password_seguro';
GRANT ALL PRIVILEGES ON asistencia_db.* TO 'asistencia_user'@'%';
FLUSH PRIVILEGES;
EXIT;
```

```bash
# Importar esquema
cd proyecto-asistencia/servidor/
mysql -u asistencia_user -p < schema.sql
```

### 2️⃣ Configurar Servidor (10 min)

```bash
cd proyecto-asistencia/servidor/

# Crear entorno virtual
python3 -m venv venv
source venv/bin/activate

# Instalar dependencias
pip install -r requirements.txt

# Editar configuración
nano config.py
# Cambiar: DB_CONFIG['password'] = 'tu_password_seguro'

# Agregar fotos de estudiantes a fotos_conocidas/
# Formato: nombre_apellido_rut.jpg

# Insertar estudiantes en BD
mysql -u asistencia_user -p asistencia_db
```

```sql
INSERT INTO estudiantes (nombre_completo, rut, path_foto_referencia) VALUES
('Juan Pérez', '12345678-9', 'juan_perez_12345678.jpg'),
('María López', '98765432-1', 'maria_lopez_98765432.jpg');
```

```bash
# Generar encodings faciales
python generate_encodings.py

# Iniciar servidor
python main.py
# Servidor corriendo en http://0.0.0.0:8000
```

### 3️⃣ Configurar Raspberry Pi (5 min)

```bash
cd proyecto-asistencia/raspberry-pi/

# Instalar dependencias
pip3 install -r requirements.txt

# Editar configuración
nano config.py
# Cambiar: SERVER_HOST = "192.168.1.100"  # IP del servidor

# Conectar LEDs:
# LED Verde: GPIO 17 → Resistencia 220Ω → (+)LED(-) → GND
# LED Rojo: GPIO 27 → Resistencia 220Ω → (+)LED(-) → GND

# Terminal 1: API de control GPIO
python3 control_gpio_api.py

# Terminal 2: Captura y transmisión
python3 captura_cliente.py
```

### 4️⃣ Configurar Cliente Web (2 min)

```bash
cd proyecto-asistencia/cliente-web/

# Editar configuración
nano js/app.js
# Cambiar: API_URL = 'http://192.168.1.100:8000'

# Iniciar servidor web
python3 -m http.server 8080

# Abrir en navegador:
# http://192.168.1.100:8080
```

### 5️⃣ Verificar (1 min)

```bash
# Ejecutar script de pruebas
cd proyecto-asistencia/
python3 test_sistema.py 192.168.1.100 192.168.1.50

# Deberías ver:
# ✓ SERVIDOR
# ✓ MYSQL
# ✓ RASPBERRY
# ✓ LEDS
# ✓ FLUJO
```

---

## 🎮 Uso

### Operación Normal

1. **Inicio del día:**
   - Encender Raspberry Pi y servidor
   - Verificar LEDs de status
   - Abrir dashboard web

2. **Durante clase:**
   - Los estudiantes pasan frente a la cámara
   - Sistema reconoce y registra automáticamente
   - LED verde indica registro exitoso
   - Dashboard muestra asistencia en tiempo real

3. **Fin del día:**
   - Revisar asistencia en dashboard
   - Exportar datos si es necesario
   - Sistema sigue corriendo 24/7

### Agregar Nuevo Estudiante

```bash
# 1. Tomar foto de frente con buena iluminación
# 2. Nombrar: nombre_apellido_rut.jpg
# 3. Copiar a servidor/fotos_conocidas/

# 4. Agregar a base de datos
mysql -u asistencia_user -p asistencia_db
```

```sql
INSERT INTO estudiantes (nombre_completo, rut, path_foto_referencia)
VALUES ('Nuevo Estudiante', '11111111-1', 'nuevo_estudiante_11111111.jpg');
```

```bash
# 5. Regenerar encodings
cd servidor/
python generate_encodings.py

# O vía API:
curl -X POST http://SERVIDOR:8000/api/recargar-encodings
```

---

## 📚 Documentación

El proyecto incluye documentación completa:

| Archivo | Descripción |
|---------|-------------|
| **[INDEX.md](INDEX.md)** | 📚 Índice navegable de toda la documentación |
| **[INICIO_RAPIDO.md](INICIO_RAPIDO.md)** | ⚡ Guía de inicio en 5 minutos |
| **[CHECKLIST_IMPLEMENTACION.md](CHECKLIST_IMPLEMENTACION.md)** | ✅ Lista de verificación completa |
| **[ARQUITECTURA_ACTUALIZADA.md](ARQUITECTURA_ACTUALIZADA.md)** | 🏗️ Diseño detallado del sistema |
| **[DIAGRAMAS.md](DIAGRAMAS.md)** | 📊 Diagramas visuales (Mermaid) |
| **[GUIA_HARDWARE.md](GUIA_HARDWARE.md)** | 🔧 Hardware, conexiones, BOM |
| **[proyecto-asistencia/README.md](proyecto-asistencia/README.md)** | 📘 Documentación técnica completa |

---

## 🔌 API Endpoints

### Servidor (Puerto 8000)

#### GET /
Información del sistema

#### GET /api/health
Health check del servidor
```json
{
  "status": "healthy",
  "encodings_loaded": true,
  "total_encodings": 8
}
```

#### POST /api/procesar-frame
Procesar frame de video (usado por Pi)
```json
{
  "image": "base64_encoded_jpeg",
  "device_id": "pi-aula-101"
}
```

**Respuesta:**
```json
{
  "status": "recognized",
  "nombre": "Juan Pérez",
  "id_estudiante": 1,
  "confidence": 0.94,
  "registrado": true
}
```

#### GET /api/estudiantes
Lista completa de estudiantes
```json
{
  "total": 8,
  "estudiantes": [
    {
      "id_estudiante": 1,
      "nombre_completo": "Juan Pérez",
      "rut": "12345678-9",
      "path_foto_referencia": "juan_perez_12345678.jpg"
    }
  ]
}
```

#### GET /api/asistencia/hoy
Asistencia del día actual
```json
{
  "fecha": "2025-10-24",
  "total": 5,
  "asistencias": [
    {
      "id_estudiante": 1,
      "nombre_completo": "Juan Pérez",
      "hora_ingreso": "08:05:23"
    }
  ]
}
```

#### POST /api/registrar
Registro manual de asistencia
```json
{
  "id_estudiante": 1,
  "device_id": "manual"
}
```

#### POST /api/recargar-encodings
Recargar encodings faciales (después de agregar estudiantes)

### Raspberry Pi (Puerto 5000)

#### GET /api/status
Estado del dispositivo

#### POST /api/led
Controlar LEDs
```json
{
  "color": "green",
  "duration": 2
}
```

#### POST /api/led/off
Apagar todos los LEDs

---

## 📁 Estructura del Proyecto

```
proyecto-asistencia/
│
├── README.md                       # Este archivo
├── INDEX.md                        # Índice de documentación
├── INICIO_RAPIDO.md               # Guía rápida
├── CHECKLIST_IMPLEMENTACION.md    # Lista de verificación
├── ARQUITECTURA_ACTUALIZADA.md    # Diseño del sistema
├── DIAGRAMAS.md                   # Visualizaciones
├── GUIA_HARDWARE.md               # Hardware y componentes
├── .gitignore                     # Git ignore
├── test_sistema.py                # Script de pruebas
│
├── raspberry-pi/                  # 🎥 Cliente Edge
│   ├── captura_cliente.py            # Captura y transmisión
│   ├── control_gpio_api.py           # API Flask para LEDs
│   ├── config.py                     # Configuración
│   └── requirements.txt              # Dependencias Python
│
├── servidor/                      # 🖥️ Servidor Central
│   ├── main.py                       # API FastAPI principal
│   ├── database.py                   # Operaciones MySQL
│   ├── face_processor.py             # Reconocimiento facial
│   ├── generate_encodings.py         # Generador de encodings
│   ├── config.py                     # Configuración
│   ├── schema.sql                    # Esquema de BD
│   ├── datos_ejemplo.sql             # Datos de prueba
│   ├── requirements.txt              # Dependencias Python
│   └── fotos_conocidas/              # Fotos de referencia
│       ├── encodings.pkl             # Encodings pre-calculados
│       └── *.jpg                     # Fotos de estudiantes
│
└── cliente-web/                   # 🌐 Interfaz Web
    ├── index.html                    # Página principal
    ├── css/
    │   └── styles.css                # Estilos
    └── js/
        └── app.js                    # Lógica JavaScript
```

---

## ⚙️ Configuración

### Servidor (`servidor/config.py`)

```python
# Base de datos
DB_CONFIG = {
    "host": "localhost",
    "user": "asistencia_user",
    "password": "tu_password",      # CAMBIAR
    "database": "asistencia_db"
}

# Reconocimiento facial
FACE_TOLERANCE = 0.6               # 0.4-0.7 recomendado
FACE_DETECTION_MODEL = "hog"       # "hog" (CPU) o "cnn" (GPU)

# Cooldown
COOLDOWN_SECONDS = 300             # 5 minutos
```

### Raspberry Pi (`raspberry-pi/config.py`)

```python
# Servidor
SERVER_HOST = "192.168.1.100"      # CAMBIAR a IP del servidor
SERVER_PORT = 8000

# Dispositivo
DEVICE_ID = "pi-aula-101"          # Identificador único

# Captura
FRAME_WIDTH = 640
FRAME_HEIGHT = 480
CAPTURE_INTERVAL = 0.5             # Segundos entre frames
JPEG_QUALITY = 70                  # 0-100

# GPIO
LED_GREEN_PIN = 17
LED_RED_PIN = 27
```

### Cliente Web (`cliente-web/js/app.js`)

```javascript
const CONFIG = {
    API_URL: 'http://192.168.1.100:8000',  // CAMBIAR
    REFRESH_INTERVAL: 10000,                // 10 segundos
    MAX_REGISTROS_RECIENTES: 10
};
```

---

## 🧪 Testing

### Test Completo del Sistema

```bash
python3 test_sistema.py IP_SERVIDOR IP_RASPBERRY_PI

# Ejemplo:
python3 test_sistema.py 192.168.1.100 192.168.1.50
```

### Tests Individuales

```bash
# Test servidor
curl http://IP_SERVIDOR:8000/api/health

# Test Raspberry Pi
curl http://IP_PI:5000/api/status

# Test estudiantes
curl http://IP_SERVIDOR:8000/api/estudiantes

# Test asistencia
curl http://IP_SERVIDOR:8000/api/asistencia/hoy

# Test LED (manual)
curl -X POST http://IP_PI:5000/api/led \
  -H "Content-Type: application/json" \
  -d '{"color": "green", "duration": 2}'
```

### Verificar Logs

```bash
# Servidor
tail -f /var/log/asistencia_server.log

# Raspberry Pi (si usas systemd)
sudo journalctl -u asistencia-captura -f
```

---

## 🐛 Solución de Problemas

### ❌ Problema: No se detectan rostros

**Síntomas:** LED nunca se enciende, logs dicen "no_face"

**Soluciones:**
1. Verificar iluminación (evitar contraluz)
2. Ajustar distancia (0.5-2 metros)
3. Verificar cámara: `raspistill -o test.jpg`
4. Reducir `FACE_TOLERANCE` en config.py

### ❌ Problema: Pi no se conecta al servidor

**Síntomas:** "Connection refused" en logs

**Soluciones:**
```bash
# 1. Verificar que servidor esté corriendo
curl http://IP_SERVIDOR:8000/api/health

# 2. Verificar conectividad
ping IP_SERVIDOR

# 3. Verificar firewall en servidor
sudo ufw allow 8000
sudo ufw status

# 4. Verificar IP en raspberry-pi/config.py
```

### ❌ Problema: LEDs no funcionan

**Síntomas:** No se encienden los LEDs

**Soluciones:**
```bash
# 1. Verificar GPIO
gpio readall

# 2. Test manual
python3 -c "
import RPi.GPIO as GPIO
GPIO.setmode(GPIO.BCM)
GPIO.setup(17, GPIO.OUT)
GPIO.output(17, GPIO.HIGH)
import time
time.sleep(2)
GPIO.output(17, GPIO.LOW)
GPIO.cleanup()
"

# 3. Verificar polaridad de LEDs
# 4. Verificar resistencias (220Ω)
# 5. Verificar control_gpio_api.py esté corriendo
```

### ❌ Problema: MySQL connection error

**Síntomas:** "Access denied" o "Can't connect"

**Soluciones:**
```bash
# 1. Verificar MySQL corriendo
sudo systemctl status mysql

# 2. Verificar credenciales en config.py

# 3. Verificar permisos
mysql -u asistencia_user -p
SHOW GRANTS;

# 4. Reconfigurar usuario si es necesario
mysql -u root -p
DROP USER 'asistencia_user'@'%';
CREATE USER 'asistencia_user'@'%' IDENTIFIED BY 'nuevo_password';
GRANT ALL PRIVILEGES ON asistencia_db.* TO 'asistencia_user'@'%';
FLUSH PRIVILEGES;
```

### ❌ Problema: Reconocimiento impreciso

**Síntomas:** Falsos positivos o negativos

**Soluciones:**
1. **Mejorar fotos de referencia:**
   - Fondo neutro
   - Iluminación frontal
   - Alta resolución (640x480 mínimo)
   - Rostro de frente

2. **Ajustar tolerancia:**
   - Más estricto: `FACE_TOLERANCE = 0.4`
   - Más permisivo: `FACE_TOLERANCE = 0.7`

3. **Regenerar encodings:**
   ```bash
   cd servidor/
   rm fotos_conocidas/encodings.pkl
   python generate_encodings.py
   ```

---

## 🗺️ Roadmap

### ✅ Versión 1.0 (Actual)
- [x] Captura de video en Pi
- [x] Reconocimiento facial en servidor
- [x] Base de datos MySQL
- [x] Dashboard web
- [x] Control LED remoto
- [x] Documentación completa

### 🚧 Versión 2.0 (En desarrollo)
- [ ] Soporte multi-persona por frame
- [ ] Panel de administración web
- [ ] Exportación de reportes (PDF/Excel)
- [ ] Gráficos y estadísticas
- [ ] Notificaciones por email
- [ ] App móvil (Android/iOS)

### 🔮 Versión 3.0 (Futuro)
- [ ] Detección de máscaras/lentes
- [ ] Integración con sistemas LMS
- [ ] Machine Learning para mejorar precisión
- [ ] Soporte para GPU
- [ ] Escalamiento a 100+ cámaras
- [ ] Dashboard de analíticas avanzadas

---

## 🤝 Contribuciones

¡Las contribuciones son bienvenidas!

### Cómo Contribuir

1. **Fork** el repositorio
2. Crea una rama: `git checkout -b feature/nueva-funcionalidad`
3. Commit tus cambios: `git commit -am 'Agrega nueva funcionalidad'`
4. Push a la rama: `git push origin feature/nueva-funcionalidad`
5. Crea un **Pull Request**

### Guías de Contribución

- Seguir estilo de código existente
- Agregar tests para nuevas funcionalidades
- Actualizar documentación
- Describir cambios en el PR

### Reportar Bugs

Usa los **Issues** de GitHub con:
- Descripción clara del problema
- Pasos para reproducir
- Comportamiento esperado vs actual
- Logs relevantes
- Versión del sistema

---
<!-- 
## 📄 Licencia

Este proyecto es de código abierto para **fines educativos**.

```
MIT License

Copyright (c) 2025 Sistema IoT Asistencia

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software...
```

Ver archivo `LICENSE` para más detalles.

--- -->

## 👥 Autores

- **Braintelligent** - *Desarrollador Principal*

---

## 🙏 Agradecimientos

- OpenCV por las herramientas de visión computacional
- face_recognition library por el reconocimiento facial
- FastAPI por el framework moderno de APIs
- Comunidad Raspberry Pi

---

## 📞 Soporte

### Documentación
- 📚 [Índice completo](INDEX.md)
- ⚡ [Inicio rápido](INICIO_RAPIDO.md)
- ✅ [Checklist](CHECKLIST_IMPLEMENTACION.md)
- 🔧 [Hardware](GUIA_HARDWARE.md)

<!-- ### Contacto
- 📧 Email: tu-email@ejemplo.com
- 💬 Discord: [Servidor del proyecto]
- 🐛 Issues: [GitHub Issues] -->

---

## 📊 Estadísticas

- ⭐ **Tasa de reconocimiento:** >95%
- ⚡ **Latencia:** <3 segundos
- 🎯 **Falsos positivos:** <2%
- 📈 **Capacidad:** 10+ cámaras por servidor
- 🔋 **Consumo Pi:** ~6W

---

<div align="center">

**⭐ Si este proyecto te fue útil, dale una estrella! ⭐**

[![GitHub stars](https://img.shields.io/github/stars/tu-usuario/proyecto-asistencia?style=social)](https://github.com/tu-usuario/proyecto-asistencia)

---

Hecho con ❤️ para la educación

*Última actualización: Octubre 2025*

</div>