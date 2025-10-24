# 📚 Sistema IoT de Asistencia por Reconocimiento Facial

## Índice de Documentación

¡Bienvenido al proyecto! Esta es tu guía para navegar por toda la documentación.

---

## 🚀 Para Empezar Rápido

1. **[INICIO_RAPIDO.md](INICIO_RAPIDO.md)** ⚡
   - Guía de 5 minutos para poner el sistema en marcha
   - Comandos esenciales
   - Verificación rápida

2. **[CHECKLIST_IMPLEMENTACION.md](CHECKLIST_IMPLEMENTACION.md)** ✅
   - Lista de verificación paso a paso
   - Nada se te escapará
   - Seguimiento de progreso

---

## 📖 Documentación Completa

### Arquitectura y Diseño

- **[ARQUITECTURA_ACTUALIZADA.md](ARQUITECTURA_ACTUALIZADA.md)** 🏗️
  - Visión general del sistema
  - Cambios vs versión original
  - Flujos de datos
  - Ventajas de la arquitectura

- **[DIAGRAMAS.md](DIAGRAMAS.md)** 📊
  - Diagramas visuales (Mermaid)
  - Flujo de reconocimiento
  - Arquitectura de red
  - Modelo de datos
  - Máquinas de estado

### Hardware

- **[GUIA_HARDWARE.md](GUIA_HARDWARE.md)** 🔧
  - Lista completa de materiales (BOM)
  - Especificaciones técnicas
  - Conexiones GPIO
  - Dónde comprar en Chile
  - Presupuestos
  - Cálculo de consumo eléctrico

### Implementación

- **[proyecto-asistencia/README.md](proyecto-asistencia/README.md)** 📘
  - Documentación técnica completa
  - Instalación detallada
  - Configuración avanzada
  - Solución de problemas
  - Monitoreo y mantenimiento
  - Seguridad y backups

---

## 💻 Código Fuente

### Raspberry Pi (Cliente Edge)
```
proyecto-asistencia/raspberry-pi/
├── captura_cliente.py          # Script principal de captura
├── control_gpio_api.py         # API para control de LEDs
├── config.py                   # Configuración
└── requirements.txt            # Dependencias
```

### Servidor (Procesamiento Central)
```
proyecto-asistencia/servidor/
├── main.py                     # API FastAPI principal
├── database.py                 # Conexión MySQL
├── face_processor.py           # Reconocimiento facial
├── generate_encodings.py       # Generador de encodings
├── config.py                   # Configuración
├── schema.sql                  # Esquema de BD
├── datos_ejemplo.sql           # Datos de prueba
└── requirements.txt            # Dependencias
```

### Cliente Web (Frontend)
```
proyecto-asistencia/cliente-web/
├── index.html                  # Página principal
├── css/styles.css              # Estilos
└── js/app.js                   # Lógica JavaScript
```

### Utilidades
```
proyecto-asistencia/
├── test_sistema.py             # Script de pruebas
└── .gitignore                  # Archivos a ignorar en Git
```

---

## 🎯 Guías por Rol

### Si eres el Responsable de Hardware
1. Leer **GUIA_HARDWARE.md** para comprar componentes
2. Revisar **CHECKLIST_IMPLEMENTACION.md** (Fase 1)
3. Seguir sección de ensamblaje

### Si eres el Responsable del Servidor
1. Leer **ARQUITECTURA_ACTUALIZADA.md** para entender el sistema
2. Seguir **INICIO_RAPIDO.md** sección "Servidor"
3. Revisar **proyecto-asistencia/README.md** para detalles

### Si eres el Responsable de Base de Datos
1. Revisar **DIAGRAMAS.md** para ver modelo de datos
2. Ejecutar **schema.sql**
3. Poblar con **datos_ejemplo.sql**

### Si eres el Responsable del Frontend
1. Entender endpoints en **ARQUITECTURA_ACTUALIZADA.md**
2. Personalizar **cliente-web/**
3. Ajustar estilos según necesidad

### Si eres el Profesor/Usuario Final
1. Leer sección "Uso" en **proyecto-asistencia/README.md**
2. Conocer interfaz web
3. Reportar problemas al equipo técnico

---

## 📂 Estructura del Proyecto

```
.
├── INICIO_RAPIDO.md                    # ⚡ Empieza aquí
├── CHECKLIST_IMPLEMENTACION.md         # ✅ Lista de verificación
├── ARQUITECTURA_ACTUALIZADA.md         # 🏗️ Diseño del sistema
├── DIAGRAMAS.md                        # 📊 Visualizaciones
├── GUIA_HARDWARE.md                    # 🔧 Componentes
├── INDEX.md                            # 📚 Este archivo
│
└── proyecto-asistencia/                # 💻 Código fuente
    ├── README.md                       # 📘 Documentación técnica
    ├── test_sistema.py                 # 🧪 Script de pruebas
    ├── .gitignore
    │
    ├── raspberry-pi/                   # 🎥 Cliente Raspberry Pi
    │   ├── captura_cliente.py
    │   ├── control_gpio_api.py
    │   ├── config.py
    │   └── requirements.txt
    │
    ├── servidor/                       # 🖥️ Servidor de procesamiento
    │   ├── main.py
    │   ├── database.py
    │   ├── face_processor.py
    │   ├── generate_encodings.py
    │   ├── config.py
    │   ├── schema.sql
    │   ├── datos_ejemplo.sql
    │   ├── requirements.txt
    │   └── fotos_conocidas/           # 📸 Fotos de referencia
    │
    └── cliente-web/                    # 🌐 Interfaz web
        ├── index.html
        ├── css/
        │   └── styles.css
        └── js/
            └── app.js
```

---

## 🎓 Flujo de Trabajo Recomendado

### Primera Vez (Implementación Completa)
```
1. GUIA_HARDWARE.md          → Comprar componentes
2. CHECKLIST_IMPLEMENTACION  → Seguir paso a paso
3. INICIO_RAPIDO.md          → Configurar rápidamente
4. test_sistema.py           → Verificar funcionamiento
5. README.md                 → Configuración avanzada
```

### Mantenimiento Regular
```
1. Revisar logs diarios
2. Backup de base de datos semanal
3. Actualizar encodings cuando se agreguen estudiantes
4. Monitorear métricas de rendimiento
```

### Solución de Problemas
```
1. Identificar componente con problema
2. Revisar logs específicos
3. Ejecutar test_sistema.py
4. Consultar sección "Solución de Problemas" en README.md
5. Verificar CHECKLIST_IMPLEMENTACION.md
```

---

## 🔍 Búsqueda Rápida

### ¿Cómo hacer...?

**Agregar un nuevo estudiante:**
→ README.md, sección "Contribuciones"

**Cambiar configuración del servidor:**
→ servidor/config.py

**Ajustar sensibilidad del reconocimiento:**
→ servidor/config.py, variable `FACE_TOLERANCE`

**Ver la asistencia de hoy:**
→ Cliente web o `curl http://SERVIDOR:8000/api/asistencia/hoy`

**Reiniciar servicios:**
→ README.md, sección "Configuración Avanzada"

**Probar el sistema:**
→ test_sistema.py

**Conectar LEDs:**
→ GUIA_HARDWARE.md, sección "Diagrama de Conexión GPIO"

**Ver costos:**
→ GUIA_HARDWARE.md, sección "Lista de Materiales"

**Entender el flujo de datos:**
→ DIAGRAMAS.md

**Instalar dependencias:**
→ requirements.txt en cada carpeta

---

## 📊 Características del Sistema

### ✅ Lo que hace
- ✅ Captura automática de video
- ✅ Reconocimiento facial en tiempo real
- ✅ Registro automático de asistencia
- ✅ Feedback visual (LEDs)
- ✅ Interfaz web en tiempo real
- ✅ Base de datos MySQL
- ✅ Arquitectura escalable
- ✅ Cooldown anti-duplicados

### ⚠️ Lo que NO hace (pero podría)
- ❌ Reconocimiento de múltiples personas simultáneas (solo 1 por vez)
- ❌ Detección de máscaras/lentes
- ❌ Login de profesores
- ❌ Generación de reportes PDF
- ❌ Notificaciones por email/SMS
- ❌ Integración con sistemas externos

---

## 🔮 Roadmap Futuro

### Versión 2.1 (Mejoras Menores)
- [ ] Soporte para múltiples personas por frame
- [ ] Dashboard de estadísticas
- [ ] Exportación de reportes

### Versión 3.0 (Mejoras Mayores)
- [ ] Panel de administración web
- [ ] Sistema de notificaciones
- [ ] Integración con sistemas institucionales
- [ ] App móvil

---

## 🤝 Contribuciones

Si mejoras el sistema:

1. Documenta tus cambios
2. Actualiza README.md
3. Agrega tests si es posible
4. Comparte con la comunidad

---

## 📞 Soporte

### Antes de Preguntar
1. ✅ Leíste INICIO_RAPIDO.md?
2. ✅ Consultaste el CHECKLIST?
3. ✅ Ejecutaste test_sistema.py?
4. ✅ Revisaste logs?

### Si Necesitas Ayuda
- 📧 Email del equipo: _________
- 💬 Slack/Discord: _________
- 📝 Issues: _________

---

## 📄 Licencia

Proyecto de código abierto para fines educativos.

---

## 🎉 ¡Comienza Ahora!

**Paso 1:** Lee [INICIO_RAPIDO.md](INICIO_RAPIDO.md)  
**Paso 2:** Sigue [CHECKLIST_IMPLEMENTACION.md](CHECKLIST_IMPLEMENTACION.md)  
**Paso 3:** ¡Disfruta tu sistema funcionando! 🚀

---

*Última actualización: Octubre 2025*