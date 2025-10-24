# 🚀 Guía de Inicio Rápido

## Pasos para poner en marcha el sistema

### 1️⃣ Servidor (5 minutos)

```bash
# Instalar MySQL y crear base de datos
sudo apt install mysql-server
sudo mysql < servidor/schema.sql

# Configurar Python
cd servidor/
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt

# Editar configuración
nano config.py  # Cambiar password de MySQL

# Agregar fotos a fotos_conocidas/ con formato: nombre_rut.jpg
# Agregar estudiantes a la BD:
mysql -u asistencia_user -p asistencia_db
# INSERT INTO estudiantes (nombre_completo, rut, path_foto_referencia) VALUES (...)

# Generar encodings
python generate_encodings.py

# Iniciar servidor
python main.py
```

### 2️⃣ Raspberry Pi (3 minutos)

```bash
# Instalar dependencias
cd raspberry-pi/
pip3 install -r requirements.txt

# Editar configuración
nano config.py  # Cambiar SERVER_HOST a IP del servidor

# Conectar LEDs:
# LED Verde: GPIO 17 → Resistencia 220Ω → (+) LED (-) → GND
# LED Rojo: GPIO 27 → Resistencia 220Ω → (+) LED (-) → GND

# Terminal 1: API de control GPIO
python3 control_gpio_api.py

# Terminal 2: Captura y transmisión
python3 captura_cliente.py
```

### 3️⃣ Cliente Web (1 minuto)

```bash
cd cliente-web/

# Editar configuración
nano js/app.js  # Cambiar API_URL a IP del servidor

# Iniciar servidor web
python3 -m http.server 8080

# Abrir navegador en: http://IP_SERVIDOR:8080
```

### 4️⃣ Verificar (30 segundos)

```bash
# Ejecutar script de prueba
python3 test_sistema.py IP_SERVIDOR IP_RASPBERRY_PI
```

---

## ⚡ Comandos útiles

### Ver logs del servidor
```bash
tail -f /var/log/asistencia_server.log
```

### Agregar nuevo estudiante
```sql
USE asistencia_db;
INSERT INTO estudiantes (nombre_completo, rut, path_foto_referencia)
VALUES ('Nuevo Estudiante', '11111111-1', 'nuevo_estudiante_11111111.jpg');
```

### Regenerar encodings
```bash
cd servidor/
python generate_encodings.py
# O vía API:
curl -X POST http://IP_SERVIDOR:8000/api/recargar-encodings
```

### Reiniciar servicios
```bash
# En servidor
sudo systemctl restart asistencia-server

# En Raspberry Pi
sudo systemctl restart asistencia-gpio
sudo systemctl restart asistencia-captura
```

---

## 📊 Endpoints principales

| URL | Descripción |
|-----|-------------|
| `http://IP_SERVIDOR:8000/api/health` | Estado del servidor |
| `http://IP_SERVIDOR:8000/api/estudiantes` | Lista de estudiantes |
| `http://IP_SERVIDOR:8000/api/asistencia/hoy` | Asistencia de hoy |
| `http://IP_PI:5000/api/status` | Estado de la Pi |
| `http://IP_SERVIDOR:8080` | Interfaz web |

---

## 🐛 Problemas comunes

**"No se detectan rostros"**
→ Verificar iluminación, ajustar FACE_TOLERANCE en config.py

**"Connection refused al servidor"**
→ Verificar que main.py esté corriendo, revisar firewall

**"LEDs no funcionan"**
→ Verificar conexiones GPIO, probar con `gpio readall`

**"Error de MySQL"**
→ Verificar credenciales en config.py, permisos del usuario

---

## 📞 Siguiente paso

Lee el **README.md** completo para configuración avanzada, auto-inicio, seguridad y optimizaciones.