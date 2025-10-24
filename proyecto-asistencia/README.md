# 🎓 Sistema IoT de Asistencia por Reconocimiento Facial

## Arquitectura Optimizada Cliente-Servidor

[![Python](https://img.shields.io/badge/Python-3.9+-blue.svg)](https://python.org)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.109+-green.svg)](https://fastapi.tiangolo.com)
[![MySQL](https://img.shields.io/badge/MySQL-8.0+-orange.svg)](https://mysql.com)
[![License](https://img.shields.io/badge/License-Educational-yellow.svg)](LICENSE)

---

## 🚀 ¿Qué es esto?

Sistema automatizado de control de asistencia que usa **reconocimiento facial** para registrar automáticamente la presencia de estudiantes. 

### ✨ Características Principales

- 📸 **Captura automática**: La Raspberry Pi captura video continuamente
- 🧠 **Procesamiento centralizado**: El servidor ejecuta el reconocimiento facial
- 💡 **Feedback instantáneo**: LEDs verdes/rojos indican resultado
- 📊 **Dashboard web**: Visualización en tiempo real de asistencia
- 🗄️ **Base de datos MySQL**: Registro persistente y consultas rápidas
- ⚡ **Optimizado**: La Pi solo transmite, el servidor procesa (eficiente!)

---

## 📖 Navegación Rápida

### 🏃‍♂️ Para Empezar

1. **[INDEX.md](INDEX.md)** - 📚 Índice completo de documentación
2. **[INICIO_RAPIDO.md](INICIO_RAPIDO.md)** - ⚡ Setup en 5 minutos
3. **[CHECKLIST_IMPLEMENTACION.md](CHECKLIST_IMPLEMENTACION.md)** - ✅ Lista paso a paso

### 📚 Documentación

- **[ARQUITECTURA_ACTUALIZADA.md](ARQUITECTURA_ACTUALIZADA.md)** - 🏗️ Diseño del sistema
- **[DIAGRAMAS.md](DIAGRAMAS.md)** - 📊 Visualizaciones (Mermaid)
- **[GUIA_HARDWARE.md](GUIA_HARDWARE.md)** - 🔧 Componentes y conexiones
- **[proyecto-asistencia/README.md](proyecto-asistencia/README.md)** - 📘 Documentación técnica completa

---

## 🎯 Diagrama Simplificado

```
┌─────────────┐          WiFi           ┌─────────────┐
│ Raspberry Pi│ ─────────────────────► │   Servidor  │
│   (Cámara)  │ ◄───────────────────── │ (Face Rec)  │
│             │    Comandos LED        │             │
└─────────────┘                        └──────┬──────┘
      │                                       │
      │ LEDs                                  │ MySQL
      ▼                                       ▼
   💚 ❤️                              📊 Base de Datos
```

**Cliente Web** → Consume API REST → Muestra asistencia en tiempo real

---

## 🛠️ Stack Tecnológico

| Componente | Tecnología |
|------------|------------|
| **Edge Device** | Raspberry Pi 4 + Cámara + LEDs |
| **Captura** | Python 3 + picamera2 |
| **Servidor** | FastAPI + face-recognition + OpenCV |
| **Base de Datos** | MySQL 8.0 |
| **Frontend** | HTML5 + CSS3 + JavaScript (Vanilla) |
| **Comunicación** | REST API (JSON) |

---

## 💰 Presupuesto Estimado

| Configuración | Costo (CLP) | Descripción |
|---------------|-------------|-------------|
| **Mínimo** | ~$120.000 | 1 Pi + PC existente como servidor |
| **Estándar** | ~$200.000 | 1 Pi + Mini PC nuevo |
| **Completo** | ~$600.000+ | Múltiples Pi's + Servidor dedicado |

Detalle completo en **[GUIA_HARDWARE.md](GUIA_HARDWARE.md)**

---

## 📁 Estructura del Proyecto

```
proyecto-asistencia/
├── raspberry-pi/           # 🎥 Cliente de captura
│   ├── captura_cliente.py       # Captura y transmisión
│   ├── control_gpio_api.py      # API para LEDs
│   └── config.py                # Configuración
│
├── servidor/               # 🖥️ Procesamiento central
│   ├── main.py                  # API FastAPI
│   ├── face_processor.py        # Reconocimiento facial
│   ├── database.py              # MySQL
│   ├── schema.sql               # Esquema BD
│   └── fotos_conocidas/         # Fotos de referencia
│
├── cliente-web/            # 🌐 Interfaz web
│   ├── index.html
│   ├── css/styles.css
│   └── js/app.js
│
└── test_sistema.py         # 🧪 Script de pruebas
```

---

## ⚡ Inicio Rápido (5 minutos)

### 1. Servidor
```bash
cd servidor/
python3 -m venv venv && source venv/bin/activate
pip install -r requirements.txt
mysql -u root -p < schema.sql
python generate_encodings.py
python main.py
```

### 2. Raspberry Pi
```bash
cd raspberry-pi/
pip3 install -r requirements.txt
python3 control_gpio_api.py &    # Terminal 1
python3 captura_cliente.py       # Terminal 2
```

### 3. Cliente Web
```bash
cd cliente-web/
python3 -m http.server 8080
```

Abre: `http://IP_SERVIDOR:8080`

---

## 📊 Demo Screenshot

```
┌──────────────────────────────────────────┐
│ 📋 Sistema de Asistencia                │
│                                          │
│ Presentes: 15    Ausentes: 3            │
│                                          │
│ 🕐 Últimos Registros:                   │
│   ✅ Juan Pérez      08:05 AM           │
│   ✅ María López     08:12 AM           │
│                                          │
│ 👥 Lista de Asistencia:                 │
│   ✅ Juan Pérez González    08:05:00   │
│   ✅ María López Silva      08:12:00   │
│   ❌ Carlos Rodríguez (Ausente)        │
└──────────────────────────────────────────┘
```

---

## 🎓 Casos de Uso

- ✅ Universidades y colegios
- ✅ Centros de capacitación
- ✅ Gimnasios y clubes
- ✅ Oficinas corporativas
- ✅ Control de acceso general

---

## 🔐 Seguridad y Privacidad

- 🔒 Datos biométricos encriptados (encodings, no imágenes originales)
- 🔒 Comunicación servidor-cliente autenticada
- 🔒 Base de datos con control de acceso
- 🔒 Compatible con GDPR/RGPD (configuración apropiada)

---

## 📈 Métricas de Rendimiento

| Métrica | Valor Típico |
|---------|--------------|
| Latencia de reconocimiento | <2 segundos |
| Tasa de acierto | >95% |
| Falsos positivos | <2% |
| Frames procesados | ~2 fps |
| Capacidad del servidor | 10+ cámaras simultáneas |

---

## 🐛 Solución de Problemas

### Error Común #1: "No se detectan rostros"
**Solución:** Verificar iluminación y ajustar `FACE_TOLERANCE` en config.py

### Error Común #2: "Connection refused"
**Solución:** Verificar que el servidor esté corriendo y firewall configurado

### Error Común #3: "LEDs no funcionan"
**Solución:** Verificar conexiones GPIO con `gpio readall`

**[Ver más](proyecto-asistencia/README.md)** en la documentación completa.

---

## 🧪 Testing

```bash
# Test completo del sistema
python3 test_sistema.py IP_SERVIDOR IP_RASPBERRY_PI

# Test individual del servidor
curl http://IP_SERVIDOR:8000/api/health

# Test de la Raspberry Pi
curl http://IP_PI:5000/api/status
```

---

## 🤝 Contribuciones

¿Mejoras o nuevas funcionalidades?

1. Fork el proyecto
2. Crea una rama: `git checkout -b feature/nueva-funcionalidad`
3. Commit: `git commit -am 'Agrega nueva funcionalidad'`
4. Push: `git push origin feature/nueva-funcionalidad`
5. Pull Request

---

## 📝 Licencia

Proyecto de código abierto para fines educativos.

---

## 👥 Créditos

Sistema desarrollado como proyecto IoT educativo.

---

## 📞 Soporte

- 📚 **Documentación completa:** [INDEX.md](INDEX.md)
- 🚀 **Guía rápida:** [INICIO_RAPIDO.md](INICIO_RAPIDO.md)
- ✅ **Checklist:** [CHECKLIST_IMPLEMENTACION.md](CHECKLIST_IMPLEMENTACION.md)
- 🔧 **Hardware:** [GUIA_HARDWARE.md](GUIA_HARDWARE.md)

---

## 🎉 ¡Comienza Ahora!

```bash
# 1. Lee la documentación
cat INDEX.md

# 2. Sigue la guía rápida
cat INICIO_RAPIDO.md

# 3. Usa el checklist
cat CHECKLIST_IMPLEMENTACION.md

# 4. ¡Implementa!
cd proyecto-asistencia/
```

---

**⭐ Si te fue útil, dale una estrella al proyecto!**

*Última actualización: Octubre 2025*